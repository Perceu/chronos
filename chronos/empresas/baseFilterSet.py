import django_filters

from chronos.core.context import get_empresa

class EmpresaFilterSet(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", get_empresa())
        super().__init__(*args, **kwargs)
        if not empresa:
            return
        for name, filtro in self.filters.items():
            if hasattr(filtro, "queryset") and filtro.queryset is not None:
                model = filtro.queryset.model
                if hasattr(model, "empresa"):
                    filtro.queryset = filtro.queryset.filter(
                        empresa=empresa
                    )