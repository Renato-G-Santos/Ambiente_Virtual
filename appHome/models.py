from django.db import models

# Create your models here.

class Categoria(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=255)
    cep = models.CharField(max_length=9, default='00000-000')
    numero_residencia = models.CharField(max_length=10)
    logradouro = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    localidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='imagens/')
    estoque = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.nome

# cliente (ForeignKey)
# produto (ForeignKey)
# preco_venda
# numero_cartao
# validade
# cvv
# data_compra

class Venda(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cartao = models.CharField(max_length=16)
    validade = models.DateField()
    cvv = models.CharField(max_length=3)
    data_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Venda de {self.produto.nome} para {self.cliente.nome}'


# class Login(models.Model):
#     nome = models.CharField(max_length=255)
#     email = models.EmailField()
#     senha = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.nome