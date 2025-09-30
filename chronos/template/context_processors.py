from django.conf import settings

def version_context(request):
    return {
        'version':settings.VERSION
    }