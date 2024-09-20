
from django.urls import path
from . import views



urlpatterns = [
    path('',views.Panel_Medico.as_view()),
]