from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    senha = models.CharField(max_length=255)
    cep = models.CharField(max_length=9, default='00000-000')
    numero_residencia = models.CharField(max_length=10, default='0')
    logradouro = models.CharField(max_length=255, default='Rua Exemplo')
    bairro = models.CharField(max_length=255, default='Bairro Exemplo')
    localidade = models.CharField(max_length=255, default='Cidade Exemplo')
    estado = models.CharField(max_length=2, default='EX')
    def __str__(self):
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField()
    foto = models.ImageField(upload_to='imagens/')
    estoque = models.IntegerField()
    def __str__(self):
        return self.nome
    
# class Login(models.Model):
#     nome = models.CharField(max_length=255)
#     email = models.EmailField()
#     senha = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.nome