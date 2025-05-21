from . import views
from django.urls import path   

urlpatterns = [
    path('', views.appHome, name='appHome'),
    path('excluir_usuario/<int:id_usuario>/', views.excluir_usuario, name='excluir_usuario'),
    path('add_usuario', views.add_usuario, name='add_usuario'),
    path('editar_usuario/<int:id_usuario>/', views.editar_usuario, name='editar_usuario'),
    path('cadastar_produto', views.cadastar_produto, name='cadastar_produto'),
    path('lista_produtos', views.lista_produtos, name='lista_produtos'),
    path('produtos', views.produtos, name='produtos'),
    path('usuario_lista', views.usuario_lista, name='usuario_lista'),
    path('fazerlogin/', views.fazerlogin, name='fazerlogin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('excluir_produto/<int:id_produto>/', views.excluir_produto, name='excluir_produto'),
    path('editar_produto/<int:id_produto>/', views.editar_produto, name='editar_produto'),
    path('api', views.viacep, name='viacep'),
]

