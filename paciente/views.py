from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.views import View

from paciente import formu
from paciente import utils
from administrador.correo import enviar_correo
from administrador import models as admin_models
import base64

# Create your views here.
class Login(View):
    def get(self,request):
        if not request.user.is_authenticated:
            form_login = formu.LoginForm()
            return render(request,'index/login.html',{
                "form_login":form_login,
            })
        if request.user.tipo == "paciente":
            return redirect("../../../../../../../../../../../dashboard/")
        elif request.user.tipo == "medico":
            return redirect("../../../../../../../../../../../medico/")
        elif request.user.tipo == "admin":
            return redirect("../../../../../../../../../../admin/")

    def post(self,request):
        if not request.user.is_authenticated:
            form = formu.LoginForm(request.POST)
            if form.is_valid():
                # Extrae los datos del formulario
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                try:
                    u=authenticate(request,username=username, password=password)
                    if u is not None:
                        auth_login(request, u)
                        u.verificado = True
                        u.save()
                        if request.user.action_verify:
                            email_c = str(u.email).encode('utf-8')
                            email_c = base64.b64encode(email_c)
                            email_c = str(email_c.decode('utf-8'))
                            request.user.verificado=False
                            request.user.save()
                            return redirect(f"../../../../../../../../../../../../verificacion/{email_c}/")
                        if request.user.tipo == "admin":
                            return redirect("../../../../../../../../../../admin/")
                except Exception as e:
                    print(str(e))
                return utils.alerta_login(request=request,alerta="Nombre de usuario o contraseña incorrecto")
            else:
                return utils.alerta_login(request=request,alerta="Todos los campos son obligatorios.")
        else:
            return redirect("../../../../../../../../../../../../../")




class Register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request,'index/register.html',{
                "register_form":formu.Register_Form(),
            })
        if request.user.tipo == "paciente":
            return redirect("../../../../../../../../../../../dashboard/")
        elif request.user.tipo == "medico":
            return redirect("../../../../../../../../../../../medico/")
        elif request.user.tipo == "admin":
            return redirect("../../../../../../../../../admin/")

    def post(self,request):
        if not request.user.is_authenticated:
            register_form = formu.Register_Form(request.POST)
            if register_form.is_valid():
                fname=str(register_form.cleaned_data['fname']).strip().title()
                username=str(register_form.cleaned_data['username']).strip()
                email=str(register_form.cleaned_data['email']).strip()
                phone=str(register_form.cleaned_data['phone']).strip()
                password1=register_form.cleaned_data['password1']
                password2=register_form.cleaned_data['password2']
                if not formu.validate_name(fname):
                    return utils.alerta_register(request=request,Error="Los nombres solo admiten letras mayúsculas, minúsculas y caracter espacio.")
                    
                if not formu.validate_username(username):
                    return utils.alerta_register(request=request,Error="El username solo admite letras mayúsculas y minúsculas y numeros.")
                    
                if User.objects.filter(username=username).exists():
                    return utils.alerta_register(request=request,Error="El username esta en uso.")
                    
                if not formu.validar_correo(email):
                    return utils.alerta_register(request=request,Error="El correo electrónico esta en uso.")
                    
                    
                v = formu.validar_password(password1=password1,password2=password2)
                if v != "OK":
                    return utils.alerta_register(request=request,Error=v)
                try:
                    u=User(username=username,email=email,tipo="paciente")
                    u.set_password(password1)
                    u.nuevo = True
                    u.save()
                    nc=admin_models.Paciente(userid=u,nombre_apellidos=fname,telefono=phone)
                    nc.save()
                    u=authenticate(request,username=username, password=password1)
                    if u is not None:
                        auth_login(request, u)
                        email_c = str(email).encode('utf-8')
                        email_c = base64.b64encode(email_c)
                        email_c = str(email_c.decode('utf-8'))
                        request.user.nuevo=True
                        request.user.verificado = False
                        request.user.action_verify = True
                        request.user.save()
                        return redirect(f"../../../../../../../../../../../../verificacion/{email_c}/")
                except Exception as e:
                    print(e)
                    pass
            else:
                return utils.alerta_register(request=request,Error="Todos los campos son obligatorios")
                
        return redirect("../../../../../../../../../../../../../")





class Logout(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("../../../../../../../../../../../../../../")



class Verificacion(View):
    def get(self,request,email):
        email = email.encode('utf-8')
        email = base64.b64decode(email)
        email = str(email.decode('utf-8'))
        if formu.validar_correo(email,if_existe=False):
            if not User.objects.filter(email=email).exists():
                return redirect("../../../../../../../../../../../../../")
            tocken=utils.get_tocken()
            Asunto = None
            Mensaje = None
            if request.user.is_authenticated:
                if request.user.nuevo == True:
                    Asunto = "Confirmación de Registro"
                    Mensaje = f'''
                        Estimado {request.user.username}:

                        Usted se ha registrado en la plataforma de Monitoreo Salud Personal

                        Para completar el proceso de registro, por favor utilice el siguiente código de verificación:

                        {tocken}

                        Muchas gracias por elegirnos, será un placer atenderle.
                    '''
                elif request.user.nuevo == False:
                    Asunto = "Alerta de Inicio de sesión"
                    Mensaje = f'''
                        Estimado {request.user.username}:

                        Usted está autenticandose en la plataforma digital de
                        Monitoreo Salud Personal

                        Para completar el proceso de registro, por favor utilice el siguiente código de verificación:

                        {tocken}

                        Muchas gracias por elegirnos, será un placer atenderle.
                    '''
            else:
                Asunto = "Recuperacion de Clave"
                Mensaje = f'''
                    Estimado {request.user.username}:

                    Hemos recibido una solicitud para recuperar su clave en la plataforma 
                    digital DIBAX TAX LLC. 
                    Para completar el proceso, por favor utilice el siguiente código de verificación:

                    {tocken}
                    
                    Si no ha sido usted ignore este mensaje y no comparta este codigo con nadie.
                    Muchas gracias por elegirnos, será un placer atenderle.
                '''
            u=User.objects.get(email=email)
            u.tocken=str(tocken)
            u.save()
            print(tocken)
            enviar_correo(email=email,asunto=Asunto,mensaje=Mensaje)
            form = formu.TwoFactorForm()
            email_c = str(email).encode('utf-8')
            email_c = base64.b64encode(email_c)
            email_c = str(email_c.decode('utf-8'))
            return render(request,"index/verificacion.html",{
                "email":email,'form':form,'email_c':email_c,
                "action_form":f"../../../../../../../../verificacion/{email_c}/"
            })
        return redirect("../../../../../../../../../../../../")

    def post(self,request,email):
        forml=formu.TwoFactorForm(request.POST)
        email = email.encode('utf-8')
        email = base64.b64decode(email)
        email = str(email.decode('utf-8'))
        if forml.is_valid():
            if not formu.validar_correo(email,if_existe=False) or not User.objects.filter(email=email).exists():
                return redirect("../../../../../../../../../../../../")
            try:
                nums=[]
                for i in range(1,7):
                    nums.append(int(forml.cleaned_data[f"num{i}"]))
                u=User.objects.get(email=email)
                if str(nums) == str(u.tocken):
                    if request.user.is_authenticated:
                        u.tocken=""
                        u.nuevo=False
                        u.verificado = True
                        u.save()
                        if request.user.tipo == "admin":
                            return redirect("../../../../../../../../../../admin/")
                        elif request.user.tipo == "medico":
                            return redirect("../../../../../../../../../../medico/")
                        elif request.user.tipo == "paciente":
                            return redirect("../../../../../../../../../../dashboard/")
                    else:
                        encode=f"{str(nums)}{uuid.uuid4()}".encode('utf-8')
                        encode=base64.b64encode(encode)
                        encode=encode.decode('utf-8')
                        u.tocken=str(encode).strip()
                        u.save()
                        return redirect(f"../../../../../../../../../../../restore_pass/{u.tocken}/")
            except Exception as e:
                print(e)
        return utils.alerta_verificacion(request=request,email=email,alerta="Tocken Inválido")

class Panel(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.tipo == "medico":
                return redirect("../../../../../../../../../../../medico/")
            elif request.user.tipo == "admin":
                return redirect("../../../../../../../../../admin/")
            elif request.user.tipo == "paciente":
                return render(request,"paciente/index.html")