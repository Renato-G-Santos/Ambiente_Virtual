from django.shortcuts import render, redirect
from django.http import HttpResponse 
# importa a função get_template() do módulo loader
from django.template import loader
from appHome.forms import FormUsuario, FormProduto, Usuario, Produto, FormLogin, FormVenda
from datetime import timedelta
import requests
from django.shortcuts import get_object_or_404
import base64, urllib, io
import matplotlib.pyplot as plt
from appHome.models import Categoria
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategoriaSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import logging




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

    response = requests.get('https://api.thecatapi.com/v1/images/search?limit=10')
    data = response.json()

    context = {
        'gatos': data,
        'produtos': produtoList
    }
    return render(request, 'produtos.html', context)

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

@csrf_exempt
def checkout(request,id_produto ):
    if request.session.get("email") is None:
        return redirect('appHome')

    usuario = Usuario.objects.get(email=request.session['email'])
    email = request.session.get('email')
    produto = Produto.objects.get(id=id_produto)
    produto.preco = produto.preco
    produto.nome = produto.nome
    
    formVenda = FormVenda(request.POST or None)
    if request.method == 'POST':
        if formVenda.is_valid():
            venda = formVenda.save(commit=False)
            venda.cliente = usuario
            venda.produto = produto
            venda.preco_venda = produto.preco
            venda.save()

    nome = usuario.nome
    context = {
        'email': email,
        'nome': nome,
        'produto': produto.nome,
        'preco': produto.preco,
        'form' : formVenda,
        'id_produto': id_produto
        }
    template = loader.get_template('test.html')
    return HttpResponse(template.render(context))

def grafico(request):
    produtos = Produto.objects.all()
    nome = [produto.nome for produto in produtos]
    estoque = [produto.estoque for produto in produtos]
    
    fig, ax = plt.subplots()
    ax.bar(nome, estoque)
    ax.set_ylabel('Produto')
    ax.set_xlabel('Estoque')
    ax.set_title('Produtos')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)

    return render(request, 'grafico.html', {'dados': uri})

@api_view(['GET', 'POST'])
def getCategoria(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def getCategoriaID(request, id_categoria):
    categoria = get_object_or_404(Categoria, id=id_categoria)

    try:
        categoria = Categoria.objects.get(id=id_categoria)
    except Categoria.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategoriaSerializer(categoria)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        categoria.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def quem_somos(request):

    return render(redirect, 'quem_somos.html')