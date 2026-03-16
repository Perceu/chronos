from django import forms

from chronos.core.context import get_empresa


class EmpresaModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        empresa = kwargs.pop("empresa", get_empresa())
        super().__init__(*args, **kwargs)
        if not empresa:
            return

        for field in self.fields.values():
            if hasattr(field, "queryset"):
                model = field.queryset.model
                if hasattr(model, "empresa"):
                    field.queryset = field.queryset.filter(
                        empresa=empresa
                    )