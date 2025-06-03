from django.contrib import admin
from .models import Usuario, Produto, Categoria, Venda

# Register your models here.


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", )

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", )

class VendaAdmin(admin.ModelAdmin):
    list_display = ("cliente", "produto", "preco_venda", "data_compra")
    

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Usuario)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Venda, VendaAdmin)




