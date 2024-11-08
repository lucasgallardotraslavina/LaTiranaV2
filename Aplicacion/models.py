from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Libro(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=500)
    autor = models.CharField(max_length=200)
    editorial = models.CharField(max_length=200)
    genero = models.CharField(max_length=200)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Custom Manager para Usuario
class Usuario(models.Model):
    ROLES_CHOICES = [
        ('jefe_bodega', 'Jefe de Bodega'),
        ('bodeguero', 'Bodeguero'),
    ]
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLES_CHOICES)

    def save(self, *args, **kwargs):
        # Hashea la contraseña antes de guardarla en la base de datos
        if not self.id:  # Solo hash si es un usuario nuevo
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def verify_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.email} ({self.role})"


# Modelo Credenciales
class Credenciales(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)  # Relación uno a uno con el Usuario
    role = models.CharField(max_length=20, choices=Usuario.ROLES_CHOICES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario.email} - {self.role}'

    class Meta:
        db_table = 'credenciales'  # Nombre de la tabla en la base de datos


class Informe(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    enviado_a = models.EmailField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    observaciones = models.TextField(null=True, blank=True)  # Nuevo campo 'observaciones'

    def __str__(self):
        return self.titulo