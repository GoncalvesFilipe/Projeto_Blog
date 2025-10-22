from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Projeto, Postagem
from .forms import ProjetoForm, PostagemForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# PÁGINA INICIAL DO SITE
def index(request):
    return render(request, "app_Postagem/index.html")  # Renderiza o template da página inicial

# LISTAS OS PROJETOS CADASTRADOS
@login_required  # Garante que apenas usuários logados possam acessar
def projetos(request):
    projetos = Projeto.objects.order_by('data_cadastro')  # Ordena os projetos por data de cadastro
    context = {'projetos': projetos}  # Cria o contexto com a lista de projetos
    return render(request, 'app_Postagem/projetos.html', context)  # Renderiza a página de projetos

# EXIBE DETALHE DE UM PROJETO
@login_required
def projeto(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    
    # Garante se o projeto pertence ao usuário atual
    if projeto.owner != request.user:
        raise Http404
    
    postagens_list = projeto.postagens.filter(owner=request.user).all().order_by('-data_cadastro') # Filtra postagens do projeto
    paginator = Paginator(postagens_list, 2) # Paginação. Visualização de 2 postagens por página
    page_number = request.GET.get('page')
    postagens = paginator.get_page(page_number)

    contexto = {
        'projeto': projeto,
        'postagens': postagens,
    }
    return render(request, 'app_Postagem/projeto.html', contexto)


# MOSTRA DETALHES DE UM PROJETO COM AS POSTAGENS
@login_required
def detalhe_projeto(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    
    # Verifica se o projeto pertence ao usuário
    if projeto.owner != request.user:
        raise Http404
    
    # Pega apenas postagens do usuário logado
    postagens = projeto.postagem.filter(owner=request.user)
    return render(request, "app_postagem/detalhe_projeto.html", {"projeto": projeto, "postagens": postagens})

# CRIA UM NOVO PROJETO
@login_required
def novo_projeto(request):
    form = ProjetoForm()  # Inicializa o formulário vazio

    if request.method == 'POST':  # Se o formulário foi submetido
        form = ProjetoForm(request.POST)
        if form.is_valid():  # Valida os dados do formulário
            projeto = form.save(commit=False)  # Cria o objeto sem salvar ainda
            projeto.owner = request.user  # Define o autor como o usuário logado
            projeto.save()  # Salva no banco
            return HttpResponseRedirect(reverse('projetos'))  # Redireciona para a lista de projetos

    context = {'form': form}  # Contexto enviado ao template
    return render(request, 'app_Postagem/novo_projeto.html', context)

# EDITAR PROJETO
@login_required
def editar_projeto(request):
    """
    Permite ao usuário selecionar um projeto e editar suas informações
    (título e descrição). O projeto é escolhido via formulário (GET),
    e os dados são atualizados via POST.
    """

    # Lista apenas os projetos do usuário autenticado
    projetos = Projeto.objects.filter(owner=request.user)
    projeto = None
    form = None

    # Obtém o projeto selecionado (via GET ou POST)
    projeto_id = request.GET.get('projeto_id') or request.POST.get('projeto_id')

    if projeto_id:
        projeto = Projeto.objects.get(id=projeto_id, owner=request.user)

        if request.method == 'POST':
            form = ProjetoForm(request.POST, instance=projeto)
            if form.is_valid():
                form.save()
                return redirect('projetos')
        else:
            form = ProjetoForm(instance=projeto)

    context = {
        'projetos': projetos,
        'projeto': projeto,
        'form': form
    }
    return render(request, 'app_Postagem/editar_projeto.html', context)

# SELEÇÃO DE PROJETO PARA EXCLUSÃO   
@login_required
def confirmar_exclusao_projeto_selecao(request):
    """Exibe lista de projetos para escolher qual excluir."""
    projetos = Projeto.objects.filter(owner=request.user)

    if request.method == "GET" and "projeto_id" in request.GET:
        projeto_id = request.GET["projeto_id"]
        return redirect("confirmar_exclusao_projeto", projeto_id=projeto_id)

    return render(request, "app_Postagem/confirmar_exclusao_projeto.html", {"projetos": projetos})

# CONFIRMAÇÃO DE EXCLUSÃO DE PROJETO 
@login_required
def confirmar_exclusao_projeto(request, projeto_id):
    """Confirma e executa a exclusão do projeto escolhido."""
    projeto = Projeto.objects.get(id=projeto_id, owner=request.user)

    if request.method == "POST":
        projeto.delete()
        return redirect("projetos")

    return render(request, "app_Postagem/confirmar_exclusao_projeto.html", {"projeto": projeto})

# EXIBE POSTAGEM ESPECIFICA
@login_required
def postagem(request, postagem_id):
    postagem = Postagem.objects.get(id=postagem_id)
    
    # Garante que o projeto pertence ao usuário
    if projeto.owner != request.user:
        raise Http404
    
    context = {
        'postagem': postagem,
        'projeto': postagem.projeto,  # Passa também o projeto relacionado
    }
    return render(request, 'app_Postagem/postagem.html', context)

# LISTA AS POSTAGENS
@login_required
def lista_postagens(request, projeto_id=None):
    if projeto_id:
        projeto = Projeto.objects.get(id=projeto_id)
        
        # Garante que o projeto pertence ao usuário
        if projeto.owner != request.user:
            raise Http404
        
        postagens = Postagem.objects.filter(projeto=projeto, owner=request.user)
    else:
        projeto = None
        postagens = Postagem.objects.filter(owner=request.user)

    # PAGINAÇÃO — Mostra 7 postagens por página
    paginator = Paginator(postagens.order_by('-data_cadastro'), 7)
    page_number = request.GET.get('page')
    postagens_paginadas = paginator.get_page(page_number)

    return render(request, 'app_Postagem/postagens.html', {
        'postagens': postagens_paginadas,
        'projeto': projeto
    })

# CRIA NOVA POSTAGEM DENTRO DO PROJETO
@login_required
def nova_postagem(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id, owner=request.user)# Garante que o usuário só possa acessar projetos que são dele.

    if request.method == "POST":
        form = PostagemForm(request.POST, request.FILES)
        if form.is_valid():
            postagem = form.save(commit=False)
            postagem.projeto = projeto
            # Não precisa definir postagem.owner: o save() no model já faz isso
            postagem.save()
            return redirect("projeto", projeto_id=projeto.id)
    else:
        form = PostagemForm()

    return render(request,"app_Postagem/nova_postagem.html", {"form": form, "projeto": projeto})

# DETALHE DE POSTAGEM
@login_required
def detalhe_postagem(request, postagem_id):
    postagem = Postagem.objects.get(id=postagem_id)

    # Protege contra acesso indevido
    if postagem.projeto.owner != request.user:
        raise Http404("Você não tem permissão para visualizar esta postagem.")

    return render(request, 'app_Postagem/detalhe_postagem.html', {'postagem': postagem})


# EDITA POSTAGEM (apenas o autor pode editar)
@login_required
def editar_postagem(request, postagem_id):
    # Busca a postagem e garante que o autor seja o usuário logado
    postagem = Postagem.objects.get(id=postagem_id, owner=request.user)
    projeto = postagem.projeto # Obtém o projeto relacionado à postagem

    # Garante que o projeto pertence ao usuário atual
    if projeto.owner != request.user:
        raise Http404("Você não tem permissão para editar postagens deste projeto.")

    if request.method == 'POST':
        # Atualiza os dados da postagem com as informações do formulário
        form = PostagemForm(request.POST, instance=postagem)
        if form.is_valid():
            form.save()
            # Redireciona de volta para a página do projeto
            return HttpResponseRedirect(reverse('projeto', args=[projeto.id]))
    else:
        form = PostagemForm(instance=postagem)# Exibe o formulário preenchido com os dados atuais da postagem

    context = {'form': form, 'postagem': postagem, 'projeto': projeto}
    return render(request, 'app_Postagem/editar_postagem.html', context)

# EXCLUIR POSTAGEM
@login_required
def excluir_postagem(request, postagem_id):
    postagem = Postagem.objects.get(id=postagem_id, owner=request.user)

    if request.method == "POST":
        postagem.delete()
        return redirect("postagens")

    return render(request, "app_Postagem/confirmar_exclusao.html", {"postagem": postagem})

# PÁGINA "SOBRE MIM"
@login_required
def sobre(request):
    return render(request, "app_Postagem/sobre.html")

# PÁGINA "CONTATO"
@login_required
def contato(request):
    return render(request, "app_Postagem/contato.html")