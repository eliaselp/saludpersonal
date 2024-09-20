from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views import View

from paciente import utils
from paciente import formu

from . import models
# Create your views here.
class Panel(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                return render(request,"administrador/index.html",{
                    "cantidad_doctores":len(User.objects.filter(tipo="medico")),
                    'cantidad_pacientes':len(User.objects.filter(tipo="paciente")),
                    "total_usuarios":len(User.objects.filter(tipo="medico"))+len(User.objects.filter(tipo="paciente")),
                })
        return redirect("../../../../../../../../../../../../../")


from paciente.formu import validate_name
class Lista_Doctores(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                return render(request,'administrador/lista_doctores.html',{
                    "lista_doctores":models.Doctor.objects.all()
                })
        return redirect("../../../../../../../../../../../../../")

    def post(self,request):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                nombre = str(request.POST.get("nombre")).strip().title()
                especialidad = str(request.POST.get("especialidad")).strip().capitalize()
                email = str(request.POST.get("email")).strip()
                username=str(request.POST.get("username")).strip()
                telefono = str(request.POST.get('telefono')).strip()
                password1 = request.POST.get("password1")
                password2 = request.POST.get("password2")
                if "" in [nombre,especialidad,email,telefono,password1,password2,username]:
                    return utils.alerta_registrar_doctor(request=request,Error="Todos los campos son obligatorios")

                if not formu.validate_username(username):
                    return utils.alerta_registrar_doctor(request=request,Error="Nombre de usuario invalido")

                if User.objects.filter(username=username).exists():
                    return utils.alerta_registrar_doctor(request=request,Error="Nombre de usuario en uso")

                if not validate_name(nombre):
                    return utils.alerta_registrar_doctor(request=request,Error="Nombre Invalido")

                if not formu.validar_correo(email,if_existe=True):
                    return utils.alerta_registrar_doctor(request=request,Error="Formato de correo Invalido")

                vp=formu.validar_password(password1,password2)
                if vp!="OK":
                    return utils.alerta_registrar_doctor(request=request,Error=vp)
                print(f"===>>{vp}")
                print(request.POST)
                nu = User(username=username,email=email,tipo="medico")
                nu.set_password(password1)
                nu.save()

                nd = models.Doctor(userid=nu,nombre_apellidos=nombre,especialidad=especialidad,telefono=telefono)
                nd.save()

                return utils.alerta_registrar_doctor(request=request,Success="Doctor Registrado con exito")
        return redirect("../../../../../../../../../../../../../")
            
    
class Eliminar_Doctor(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                try:
                    doc = models.Doctor.objects.get(id=id)
                    doc.userid.delete()
                    doc.delete()
                    return utils.alerta_lista_doctores(request=request,Success="Doctor eliminado correctamente")
                except Exception as e:
                    pass
                return utils.alerta_lista_doctores(request=request,Error="Acceso Denegado")
        return redirect("../../../../../../../../../../../../../")
    


class Modificar_Doctor(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                try:
                    doc = models.Doctor.objects.get(id=id)
                    return render(request,"administrador/modificardoctor.html",{
                        "doctor_id":id,
                        "doctor":doc
                    })
                except Exception as e:
                    print(str(e))
            return utils.alerta_lista_doctores(request=request,Error="Acceso denegado")
        return redirect("../../../../../../../../../../../../../")
    
    def post(self,request,id):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                nombre = str(request.POST.get("nombre")).strip().title()
                especialidad = str(request.POST.get("especialidad")).strip().capitalize()
                email = str(request.POST.get("email")).strip()
                telefono = str(request.POST.get('telefono')).strip()
                try:
                    doc = models.Doctor.objects.get(id=id)
                    if "" in [nombre,especialidad,email,telefono,]:
                        return utils.alerta_modificar_doctor(request=request,id=id,Error="Todos los campos son obligatorios")

                    if not validate_name(nombre):
                        return utils.alerta_modificar_doctor(request=request,id=id,Error="Nombre Invalido")

                    if email!=doc.userid.email and not formu.validar_correo(email,if_existe=False):
                        return utils.alerta_modificar_doctor(request=request,id=id,Error="Formato de correo Invalido")
                
                    doc.nombre_apellidos=nombre
                    doc.telefono = telefono
                    doc.userid.email = email
                    doc.especialidad = especialidad
                    doc.userid.save()
                    doc.save()
                    return utils.alerta_lista_doctores(request=request,Success="Doctor modificado correctamente")
                except Exception as e:
                    print(e)
                return utils.alerta_lista_doctores(request=request,Error="Acceso denegado")
            