from django import forms
from Aplicacion.models import Libro
class FormLibro(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'

        
class InformeForm(forms.Form):
    titulo = forms.CharField(label="Título", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={'class': 'form-control'}))
    observaciones = forms.CharField(label="Observaciones", widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    destinatario = forms.EmailField(label="Correo del Destinatario", widget=forms.EmailInput(attrs={'class': 'form-control'}))
