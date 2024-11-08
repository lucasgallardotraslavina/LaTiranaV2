from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Libro
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import Usuario, Credenciales
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from .forms import InformeForm
from .models import Informe
from Aplicacion.forms import FormLibro
from django.contrib.auth.decorators import login_required


# Vista para la página de inicio (opcional)
def index(request):
    return render(request, 'Aplicacion/index.html')

# Vista para la página de login

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Autenticación manual
        try:
            usuario = Usuario.objects.get(email=email)
            if usuario.verify_password(password):
                # Autenticar al usuario con el sistema de autenticación de Django
                user = authenticate(request, username=usuario.email, password=password)
                
                if user is None:
                    # Si el usuario no está en el sistema de Django, registrarlo temporalmente
                    user = Usuario.objects.create_user(
                        email=usuario.email, 
                        password=password
                    )
                
                # Iniciar sesión utilizando el método login de Django
                login(request, user)

                # Redireccionar según el rol
                if usuario.role == 'jefe_bodega':
                    return redirect('dashboard_jefe_bodega')
                elif usuario.role == 'bodeguero':
                    return redirect('dashboard_bodeguero')
            else:
                messages.error(request, 'Contraseña incorrecta.')
        except Usuario.DoesNotExist:
            messages.error(request, 'El correo no está registrado.')
    
    return render(request, 'Aplicacion/login.html')

def jefe_bodega_dashboard(request):
    return render(request, 'Aplicacion/index_jefe_bodega.html')

def bodeguero_dashboard(request):
    return render(request, 'Aplicacion/index_bodeguero.html')

def listadoLibros_jefe(request):
    libros = Libro.objects.all()
    data = {'libros': libros} 
    return render(request, 'Aplicacion/libros_jefe.html', data) 
# Vista para la página de registro
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        # Verificar si el usuario ya existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return redirect('register')

        # Crear usuario
        usuario = Usuario.objects.create_user(email=email, password=password, role=role)

        # Guardar en la tabla Credenciales
        credenciales = Credenciales.objects.create(usuario=usuario, role=role)

        messages.success(request, 'Usuario registrado correctamente.')
        return redirect('login')  # O la vista que desees redirigir
    
    return render(request, 'Aplicacion/register.html')
#===================================================
# Vista para la página de listado de libros
def libros(request):
    libros = Libro.objects.all()
    return render(request, 'Aplicacion/libros.html', {'libros': libros})

def listadoLibros_jefe(request):
    libros = Libro.objects.all()
    data = {'libros': libros} 
    return render(request, 'Aplicacion/libros_jefe.html', data) 

# Vista para agregar un libro
def agregarLibro(request):
    form = FormLibro()
    if request.method == 'POST':
        form = FormLibro(request.POST)
        if form.is_valid():
            form.save()
        return redirect('agregarLibro')  # Redirige en lugar de renderizar directamente la vista
    data = {'form': form}   
    return render(request, 'Aplicacion/agregarLibro.html', data)

def eliminarLibro(request, id):
    libro = Libro.objects.get(id=id)
    libro.delete()
    return redirect('/libros/') 

def actualizarLibro(request, id):
    libro = Libro.objects.get(id=id)
    form = FormLibro(instance=libro)
    if request.method == 'POST':
        form = FormLibro(request.POST, instance=libro)
        if form.is_valid():
            form.save()
        return redirect('/')  # Redirige en lugar de renderizar directamente la vista
    data = {'form': form}
    return render(request, 'Aplicacion/agregarLibro.html', data)

# Vista para generar informe
def generar_informe(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        destinatario = request.POST.get('destinatario')

        email = EmailMessage(
            titulo,
            contenido,
            settings.EMAIL_HOST_USER,
            [destinatario]
        )

        try:
            email.send()
            mensaje = "Informe enviado con éxito."

            # Verificar si el usuario está autenticado
            usuario = request.user if request.user.is_authenticated else None

            # Guardar el informe en la base de datos
            informe = Informe.objects.create(
                titulo=titulo,
                contenido=contenido,
                enviado_a=destinatario,
                usuario=usuario
            )
            informe.save()

        except Exception as e:
            mensaje = f"Error al enviar el correo: {e}"

        return render(request, 'Aplicacion/generar_informe.html', {'mensaje': mensaje})

    return redirect('informes')
    # Manejo de solicitud GET para mostrar el formulario
def informes(request):
    form = InformeForm()

    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            observaciones = form.cleaned_data.get('observaciones', '')
            destinatario = form.cleaned_data['destinatario']
            usuario = request.user  # El usuario actual que genera el informe

            # Envío de correo
            try:
                asunto = f"Informe: {titulo}"
                mensaje = f"Descripción: {descripcion}\n\nObservaciones: {observaciones}"
                email = EmailMessage(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [destinatario]
                )
                email.send()

                # Guardar el informe en la base de datos
                Informe.objects.create(
                    titulo=titulo,
                    contenido=descripcion,
                    enviado_a=destinatario,
                    observaciones=observaciones,
                    usuario=usuario
                )

                messages.success(request, "Informe enviado y guardado con éxito.")
                return redirect('informes')
            except Exception as e:
                messages.error(request, f"Error al enviar el correo: {e}")

    return render(request, 'Aplicacion/informes.html', {'form': form})


from .models import Informe

def listar_informes(request):
    informes = Informe.objects.filter(usuario=request.user)
    return render(request, 'Aplicacion/informes.html', {'informes': informes})


def informes_guardados(request):
    # Obtener todos los informes almacenados en la base de datos
    informes = Informe.objects.all()
    return render(request, 'Aplicacion/informes_guardados.html', {'informes': informes})

def ficcion(request):
    return render(request, 'Aplicacion/ficcion.html')


def catalogo_busqueda(request):
    query = request.GET.get('q', '')  # Obtén el término de búsqueda
    if query:
        libros = Libro.objects.filter(titulo__icontains=query)  # Filtra por título (o autor, descripción, etc.)
    else:
        libros = Libro.objects.all()  # Si no hay búsqueda, muestra todos los libros
    
    return render(request, 'catalogo.html', {'libros': libros})