import base64
from datetime import datetime

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect

from chronos.core.context import set_empresa


class ActiveMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        expiration = base64.b64decode(settings.EXPIRATION_DATE).decode("utf-8")
        datetime_object = datetime.strptime(expiration, "%d/%m/%Y")

        if datetime_object < datetime.now():
            return HttpResponse(
                """
                    <center>
                        Sua versão de teste acabou solicite suporte!
                    </center>
                """,
                status=403,
            )
        response = self.get_response(request)

        return response


class EmpresaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        empresa = None
        if request.user.is_authenticated:
            if hasattr(request.user, "usuario") and request.user.usuario is not None:
                empresa = request.user.usuario.empresa
            elif request.user.is_superuser:
                empresa = None
            else:
                logout(request)
                return HttpResponse(
                    """
                        <center>
                            Você não tem permissão para acessar o sistema, contate o suporte!
                        </center>
                    """,
                    status=403,
                )
        request.empresa = empresa
        set_empresa(empresa)

        return self.get_response(request)


class SuperuserAdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            is_admin_url = request.path.startswith("/admin")

            if request.user.is_superuser and not is_admin_url:
                return redirect("/admin/")

        return self.get_response(request)
