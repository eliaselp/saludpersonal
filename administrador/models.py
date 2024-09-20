from django.db import models
from django.contrib.auth.models import User

# Create your models here.
User.add_to_class('tipo', models.TextField(null=False, default = "admin"))
User.add_to_class('nuevo', models.BooleanField(null=False,default=True))
User.add_to_class('tocken', models.TextField(null=True))
User.add_to_class('action_verify', models.BooleanField(null=False,default=True))
User.add_to_class('verificado', models.BooleanField(null=False,default=False))


class Doctor(models.Model):
    userid = models.OneToOneField(User,on_delete=models.CASCADE)
    nombre_apellidos = models.TextField(null=False,blank=False)
    especialidad = models.TextField(null=False,blank=False)
    telefono = models.TextField(null=False,blank=False)

class Paciente(models.Model):
    userid = models.OneToOneField(User,on_delete=models.CASCADE)
    nombre_apellidos = models.TextField(null=False,blank=False)
    telefono = models.TextField(null=False,blank=False)
