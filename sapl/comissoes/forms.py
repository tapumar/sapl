from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Reuniao

class ReuniaoForm(ModelForm):

    class Meta:
        model = Reuniao
        exclude = ['cod_andamento_sessao']

    def clean(self):
        super(ReuniaoForm, self).clean()

        if not self.is_valid():
            return self.cleaned_data

        instance = self.instance

        num = self.cleaned_data['numero']
        com = self.cleaned_data['comissao']
        tipo = self.cleaned_data['tipo']
        periodo = self.cleaned_data['periodo']

        error = ValidationError(
            "Número de Reunião já existente "
            "para a Comissão, Período e Tipo informados. "
            "Favor escolher um número distinto.")

        reunioes = Reuniao.objects.filter(numero=num,
                                                comissao=com,
                                                periodo=periodo,
                                                tipo=tipo).\
            values_list('id', flat=True)

        qtd_reunioes = len(reunioes)

        if qtd_reunioes > 0:
            if instance.pk:  # update
                if instance.pk not in reunioes or qtd_reunioes > 1:
                    raise error
            else:  # create
                raise error

        return self.cleaned_data
