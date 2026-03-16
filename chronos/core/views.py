from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

# Create your views here.
@login_required
def dashboard(request):
    return render(request, "dashboard.html")


class ChronosLoginView(LoginView):
    pass


class ChronosLogoutView(LogoutView):
    template_name="registration/my_logged_out.html"
    pass

