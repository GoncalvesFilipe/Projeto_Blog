from django.db import models
from django.contrib.auth.models import User

# Modelo para Projetos
class Projeto(models.Model):
    titulo = models.CharField(max_length=50)  # Título do projeto.
    descricao = models.TextField(max_length=10000)  # Descrição do projeto.
    data_cadastro = models.DateTimeField(auto_now_add=True) # auto_now_add=True: registra automaticamente a data e hora de criação do projeto
    data_atualizacao = models.DateTimeField(auto_now=True) # auto_now=True: atualiza automaticamente a data e hora sempre que o objeto for salvo
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # O usuário que criou o projeto. Se deletado, o projeto também é.

    def __str__(self):
        return self.titulo  # Retorna o título do projeto como representação do objeto.
    
    class Meta:
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"
        ordering = ["-data_cadastro"]

# Modelo para Postagens dentro de um projeto
class Postagem(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='postagens')# Relaciona a postagem a um projeto. 'related_name' permite acessar postagens via projeto.postagens.all()
    
    titulo = models.CharField(max_length=200)  # Título da postagem
    descricao = models.TextField()  # Conteúdo da postagem
    data_cadastro = models.DateTimeField(auto_now_add=True)  # Data e hora de criação
    data_atualizacao = models.DateTimeField(auto_now=True)  # Atualiza automaticamente ao salvar
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # O autor da postagem é automaticamente o mesmo dono do projeto.
    # Essa relação é garantida no método save() abaixo.

    class Meta:
        verbose_name = "Postagem"
        verbose_name_plural = "Postagens"
        ordering = ["-data_cadastro"]


    def __str__(self):
        return self.titulo 
    
    def save(self, *args, **kwargs):
        """
        Garante que o dono da postagem seja sempre o mesmo do projeto.
        Mesmo que um usuário diferente tente atribuir uma postagem,
        o sistema corrige automaticamente para manter a consistência lógica.
        """
        self.owner = self.projeto.owner
        super().save(*args, **kwargs)

# Modelo para Contatos
class Contato(models.Model):
    nome = models.CharField(max_length=100)  # Nome do contato
    telefone = models.CharField(max_length=11)  # Telefone do contato
    email = models.EmailField(max_length=50)  # E-mail do contato
    texto = models.TextField(blank=True)  # Mensagem enviada pelo usuário
    data_cadastro = models.DateTimeField(auto_now_add=True)  
    # Data e hora em que o contato foi enviado

    def __str__(self):
        return self.nome  # Retorna o nome como representação do contato
        
    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"
        ordering = ["-data_cadastro"]
