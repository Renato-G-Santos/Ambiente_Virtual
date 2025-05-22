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
    
# class Login(models.Model):
#     nome = models.CharField(max_length=255)
#     email = models.EmailField()
#     senha = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.nome