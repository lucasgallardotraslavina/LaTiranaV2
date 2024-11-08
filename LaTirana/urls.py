from django.urls import path
from Aplicacion import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),

    path('dashboard/jefe-bodega/', views.jefe_bodega_dashboard, name='dashboard_jefe_bodega'),
    path('dashboard/bodeguero/', views.bodeguero_dashboard, name='dashboard_bodeguero'),

    path('libros_jefe/',views.listadoLibros_jefe, name='libros_jefe'),

    path('informes/', views.informes, name='informes'), 

    path('informes_guardados/', views.informes_guardados, name='informes_guardados'),

    path('register/', views.register, name='register'),
    path('libros/', views.libros, name='libros'),
    path('agregarLibro/', views.agregarLibro, name='agregarLibro'),
    path('actualizarLibro/<int:id>/', views.actualizarLibro, name='actualizarLibro'),
    path('eliminarLibro/<int:id>/', views.eliminarLibro, name='eliminarLibro'),
    path('generar_informe/', views.generar_informe, name='generar_informe'),
    path('ficcion/', views.ficcion, name='ficcion'),

    
    path('buscar/', views.catalogo_busqueda, name='catalogo_busqueda'),
]
