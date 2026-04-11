from django.urls import path

from . import views

urlpatterns = [
    # Mantenimientos CRUD
    path('', views.lista_mantenimientos, name='lista_mantenimientos'),
    path('registrar/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    path('<int:pk>/editar/', views.editar_mantenimiento, name='editar_mantenimiento'),
    path('<int:pk>/eliminar/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),

    # QR / NFC — acceso público por token
    path('rapido/<uuid:token>/', views.mantenimiento_rapido, name='mantenimiento_rapido'),
    path('rapido/<uuid:token>/exito/', views.mantenimiento_rapido_exito, name='mantenimiento_rapido_exito'),

    # Destinatarios de reportes
    path('destinatarios/', views.lista_destinatarios, name='lista_destinatarios'),
    path('destinatarios/agregar/', views.agregar_destinatario, name='agregar_destinatario'),
    path('destinatarios/<int:pk>/eliminar/', views.eliminar_destinatario, name='eliminar_destinatario'),
    path('destinatarios/<int:pk>/toggle/', views.toggle_destinatario, name='toggle_destinatario'),
]
