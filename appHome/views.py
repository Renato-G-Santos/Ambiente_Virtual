from django.shortcuts import render, redirect
from django.http import HttpResponse 
# importa a função get_template() do módulo loader
from django.template import loader
from appHome.forms import FormUsuario, FormProduto, Usuario, Produto, FormLogin
from datetime import timedelta
import requests
from django.shortcuts import get_object_or_404

# Create your views here.

def appHome(request):
    email_do_usuario = request.session.get('email')

    context = {
        'email_do_usuario': email_do_usuario
    }

    return render(request, 'index.html', context)

def add_usuario(request):
    formUsuario = FormUsuario(request.POST or None)
    if request.method == 'POST':
        # Verifica se o formulário é válido
        # Se for, salva os dados no banco de dados
        # e redireciona para a página inicial

        if formUsuario.is_valid():
            usuario = formUsuario.save(commit=False)  # Não salva ainda no banco

            # Busca o endereço com base no CEP
            cep = formUsuario.cleaned_data['cep']
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            if response.status_code == 200:
                data = response.json()
                usuario.logradouro = data.get('logradouro', '')
                usuario.bairro = data.get('bairro', '')
                usuario.localidade = data.get('localidade', '')
                usuario.estado = data.get('uf', '')

            usuario.save() 
            
            # Redireciona para a página inicial após o cadastro
        return redirect('appHome')

    context = {
        'form': formUsuario
    }
    return render(request, 'add_usuario.html', context)

def excluir_usuario(request, id_usuario):
    # Verifica se o usuário existe
    
        usuario = Usuario.objects.get(id=id_usuario)
        # Se existir, exclui o usuário
        usuario.delete()
        return redirect('usuario_lista')

def editar_usuario(request, id_usuario):
     
    usuario = Usuario.objects.get(id=id_usuario)

    form = FormUsuario(request.POST or None, instance=usuario)
    
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('appHome')
   
    context = {
        'form': form
    }
    return render(request, 'editar_usuarios.html', context)

def criar_produto(request):
    formProduto = FormProduto(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # Verifica se o formulário é válido
        # Se for, salva os dados no banco de dados
        # e redireciona para a página inicial

        if formProduto.is_valid():

            formProduto.save()
            
            # Redireciona para a página inicial após o cadastro
            return redirect('appHome')

    context = {
        'form': formProduto
    }
    return render(request, 'cadastar_produto.html', context)

def lista_produtos(request):
    if request.session.get("email") is None:
        return redirect('appHome')
    # if request.session.get("email") is None:
    #     return redirect('fazerlogin')
    # Cria uma lista de produtos
    produtoList = Produto.objects.all()
    # Cria um dicionário com os dados a serem passados para o template
    context = {
        'produtos': produtoList
    }
    
    # Carrega o template home.html
    template = loader.get_template('lista_produtos.html')
    # Renderiza o template carregado
    return HttpResponse(template.render(context))

def produtos(request):
    # Cria uma lista de produtos
    produtoList = Produto.objects.all()
    # Cria um dicionário com os dados a serem passados para o template
    context = {
        'produtos': produtoList
    }
    
    # Carrega o template home.html
    template = loader.get_template('produtos.html')
    # Renderiza o template carregado
    return HttpResponse(template.render(context))

def cadastar_produto(request):
    if request.session.get("email") is None:
        return redirect('appHome')
    # if request.session.get("email") is None:
    #     return redirect('fazerlogin')
    formProduto = FormProduto(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        # Verifica se o formulário é válido
        # Se for, salva os dados no banco de dados
        # e redireciona para a página inicial

        if formProduto.is_valid():

            formProduto.save()
            
            # Redireciona para a página inicial após o cadastro
            return redirect('produtos')

    context = {
        'form': formProduto
    }
    return render(request, 'cadastar_produto.html', context)

def fazerlogin(request):
    formL = FormLogin(request. POST or None)
    if request.method == 'POST':
        if formL.is_valid():
            _email = formL.cleaned_data.get('email')
            _senha = formL.cleaned_data.get('senha')

            try:
                usuarioL = Usuario.objects.get(email=_email, senha = _senha)

                if usuarioL is not None:
                    #Define a duração da sessão como 30 segundos
                    request.session.set_expiry(timedelta(seconds=3600))
                    #Cria uma sessão com o email do usuário
                    request.session['email'] = _email
                    return redirect('appHome')
                
            except Usuario.DoesNotExist:
                return render(request, 'login.html', {'error_message':
                'Credenciais inválidas. Por favor, tente novamente.'})
    context = {
        'formLogin': formL
    }
    return render(request, 'login.html', context)

def usuario_lista(request):
    if request.session.get("email") is None:
        return redirect('appHome')
        # Cria uma lista de usuários
    userLits = Usuario.objects.all()

    # Cria um dicionário com os dados a serem passados para o template
    context = {
        'usuarios': userLits
    }
    
    # Carrega o template home.html
    template = loader.get_template('usuario_list.html')

    
    # Renderiza o template carregado
    return HttpResponse(template.render(context))

def dashboard(request):
    if request.session.get("email") is None:
        return redirect('appHome')
    # Carrega o template home.html
    template = loader.get_template('dashboard.html')
    # Renderiza o template carregado
    return HttpResponse(template.render())

def logout(request):
    # Remove a sessão do usuário
    del request.session['email']
    # Redireciona para a página inicial
    return redirect('appHome')

def excluir_produto(request, id_produto):
    # Verifica se o produto existe
    try:
        produto = Produto.objects.get(id=id_produto)
        # Se existir, exclui o produto
        produto.delete()
        return redirect('produtos')
    except Produto.DoesNotExist:
        return redirect('produtos')
    
def editar_produto(request, id_produto):
    # Verifica se o produto existe
    try:
        produto = Produto.objects.get(id=id_produto)
    except Produto.DoesNotExist:
        return redirect('produtos')

    form = FormProduto(request.POST or None, request.FILES or None, instance=produto)
    
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect('produtos')
   
    context = {
        'form': form
    }
    return render(request, 'editar_produto.html', context)


def checkout(request,id_produto ):
    if request.session.get("email") is None:
        return redirect('appHome')
    
    usuario = Usuario.objects.get(email=request.session['email'])
    email = request.session.get('email')
    produto = Produto.objects.get(id=id_produto)
    produto.nome = produto.nome
    produto.preco = produto.preco  
    nome = usuario.nome
    context = {
        'email': email,
        'nome': nome,
        'produto': produto.nome,
        'preco': produto.preco,

        }
    template = loader.get_template('checkout.html')
    return HttpResponse(template.render(context))

