
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('',include('paciente.urls')),
    path('medico/',include('medico.urls')),
    path('admin/',include('administrador.urls')),
]

#static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


#from django.conf.urls import handler404
#from cliente.views import custom_404

#handler404 = custom_404