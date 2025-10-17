from django import forms
from .models import Projeto, Postagem

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = ['titulo', 'descricao']
        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
                  }

class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        # apenas os campos que o usuário preenche
        fields = ['titulo', 'descricao']
        labels = {'descricao': ''}
        widgets = {
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Digite o conteúdo da postagem...'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o título da postagem'
            })
        }
