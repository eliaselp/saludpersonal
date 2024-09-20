from django.shortcuts import render

from django.views import View
# Create your views here.

class Panel_Medico(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.tipo == "paciente":
                return redirect("../../../../../../../../../../../dashboard/")
            elif request.user.tipo == "admin":
                return redirect("../../../../../../../../../../../admin/")
            elif request.user.tipo == "medico":
                return render(request,"medico/index.html")