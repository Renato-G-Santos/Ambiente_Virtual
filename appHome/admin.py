from django.contrib import admin
from .models import Usuario, Produto, Categoria

# Register your models here.


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", )

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", )

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Usuario)
admin.site.register(Produto, ProdutoAdmin)




