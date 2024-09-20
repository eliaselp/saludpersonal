
from django.urls import path,include
from paciente import views


urlpatterns = [
    path('login/',views.Login.as_view()),
    path('register/',views.Register.as_view()),
    path('',views.Login.as_view()),
    path('dashboard/',views.Panel.as_view()),
    path('logout/',views.Logout.as_view()),
    path('verificacion/<str:email>/',views.Verificacion.as_view()),
    #path('dashboard/')
]