import base64
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse
from chronos.core.context import set_empresa

class ActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        expiration = base64.b64decode(settings.EXPIRATION_DATE).decode('utf-8')
        datetime_object = datetime.strptime(expiration, "%d/%m/%Y")

        if datetime_object < datetime.now():
            return HttpResponse("""
            <center>
                Sua versão de teste acabou solicite suporte!
            </center>
        """, status=403)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

class EmpresaMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        empresa = None
        if request.user.is_authenticated:
            empresa = request.user.usuario.empresa

        request.empresa = empresa
        set_empresa(empresa)

        return self.get_response(request)