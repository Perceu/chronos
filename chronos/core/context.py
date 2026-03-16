# core/empresa_context.py

import threading

_thread_locals = threading.local()

def set_empresa(empresa):
    _thread_locals.empresa = empresa

def get_empresa():
    return getattr(_thread_locals, "empresa", None)