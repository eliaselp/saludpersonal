from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from paciente import formu
from administrador import models
import base64

import random
def get_tocken():
    lista = list([random.randint(0, 9) for _ in range(6)])
    random.shuffle(lista)
    for x in lista:
        x=str(x)
    return lista





##### ALERTAS ####
def alerta_login(request,alerta):
    if not request.user.is_authenticated:
        form_login = formu.LoginForm()
        return render(request,'index/login.html',{
            "form_login":form_login,
            "Alerta":alerta
        })
    return redirect("../../../../../../../../../../")


def alerta_verificacion(request,email,alerta):
    form = formu.TwoFactorForm()
    email_c = str(email).encode('utf-8')
    email_c = base64.b64encode(email_c)
    email_c = str(email_c.decode('utf-8'))
    return render(request,"index/verificacion.html",{
        "email":email,'form':form,'email_c':email_c,
        "action_form":f"../../../../../../../../verificacion/{email_c}/",
        "Alerta":alerta
    })



def alerta_lista_doctores(request,Error=None,Success=None):
    print("alerta_lista_doctores")
    return render(request,'administrador/lista_doctores.html',{
        "lista_doctores":models.Doctor.objects.all(),
        "Error":Error,"Success":Success
    })



def alerta_home_admin(request,Error=None,Success=None):
    print("alerta_home_admin")
    return render(request,"administrador/index.html",{
        "cantidad_doctores":len(User.objects.filter(tipo="medico")),
        'cantidad_pacientes':len(User.objects.filter(tipo="paciente")),
        "total_usuarios":len(User.objects.filter(tipo="medico"))+len(User.objects.filter(tipo="paciente")),
        "Error":Error,"Success":Success
    })



def alerta_registrar_doctor(request,Error=None,Success=None):
    print("alerta_registrar_doctor")
    referer = request.META.get('HTTP_REFERER')
    if referer.endswith("/admin/doctores/"):
        return alerta_lista_doctores(request=request,Error=Error,Success=Success)
    elif referer.endswith("/admin/"):
        return alerta_home_admin(request=request,Error=Error,Success=Success)
    else:
        return alerta_lista_doctores(request=request,Error=Error,Success=Success)
    
def alerta_modificar_doctor(request,id,Error=None,Success=None):
    doc = models.Doctor.objects.get(id=id)
    return render(request,"administrador/modificardoctor.html",{
        "doctor_id":id,
        "doctor":doc,
        "Error":Error,"Success":Success
    })

def alerta_register(request,Error=None):
    if not request.user.is_authenticated:
        return render(request,'index/register.html',{
            "register_form":formu.Register_Form(),
            "Error":Error
        })
    if request.user.tipo == "paciente":
        return redirect("../../../../../../../../../../../dashboard/")
    elif request.user.tipo == "medico":
        return redirect("../../../../../../../../../../../medico/")
    elif request.user.tipo == "admin":
        return redirect("../../../../../../../../../admin/")

