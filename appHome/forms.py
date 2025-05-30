from django import forms
from appHome.models import Usuario, Produto, Venda

#formulário 

class FormUsuario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'cep', 'numero_residencia']
    widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control border border-success'}),
        'email': forms.EmailInput(attrs={'class': 'form-control border border-success', type: 'email'}),
        'senha': forms.PasswordInput(attrs={'class': 'form-control border border-success', type: 'password'}),
        'cep': forms.TextInput(attrs={'class': 'form-control border border-success'}),
        'numero_residencia': forms.TextInput(attrs={'class': 'form-control border border-success'}),
        }

class FormProduto(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'descricao', 'foto', 'estoque', 'categoria']
    widgets = {
        'descricao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        'foto': forms.FileInput(attrs={'accept': 'image/*'}),
        'estoque': forms.NumberInput(attrs={'min': 0}),
        'nome': forms.TextInput(attrs={'class': 'form-control border border-success'}),
        'preco': forms.NumberInput(attrs={'class': 'form-control border border-success'}),
        'categoria': forms.Select(attrs={'placeholder': 'Selecione uma categoria'}),
    }

class FormLogin(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'senha']

    widgets = {
        'email': forms.EmailInput(attrs={'class': 'form-control border border-success', type: 'email'}),
        'senha': forms.PasswordInput(attrs={'class': 'form-control border border-success', type: 'password'}),
    }

class FormsVenda(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [ 'numero_cartao', 'validade', 'cvv']
        widegts = {
            'numero_cartao': forms.TextInput(attrs={'class': 'form-control border border-success'}),
            'validade': forms.DateInput(attrs={'class': 'form-control border border-success', 'type': 'date'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control border border-success'}),
        }