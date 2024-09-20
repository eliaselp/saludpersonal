
from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.Panel.as_view()),
    path('doctores/',views.Lista_Doctores.as_view()),
    path('doctores/<int:id>/',views.Modificar_Doctor.as_view()),
    path('doctores/eliminar/<int:id>/',views.Eliminar_Doctor.as_view()),
]