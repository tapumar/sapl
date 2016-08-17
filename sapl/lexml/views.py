# from sapl.crud.base import CrudAux

# from .models import LexmlProvedor, LexmlPublicador
from django.shortcuts import render
from django.views.generic import FormView

from sapl.crud.base import Crud

from .forms import PesquisaLexmlForm
from .models import LexmlProvedor, LexmlPublicador

LexmlProvedorCrud = Crud.build(LexmlProvedor, 'lexml_provedor')
LexmlPublicadorCrud = Crud.build(LexmlPublicador, 'lexml_publicador')


class LexmlPesquisarView(FormView):
    template_name = 'lexml/resultado_pesquisa.html'
    form_class = PesquisaLexmlForm


def add_oai_server(request):
    template = 'lexml/add_SAPLOAIServer.html'
    return render(request, template, {})


def edit_oai_server(request):
    template = 'lexml/edit_SAPLOAIServer.html'
    return render(request, template, {})

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = PesquisaLexmlForm(request.POST)

        pesquisa = form.data['conteudo'].replace(' ', '+')
        url = 'http://www.lexml.gov.br/busca/search?keyword='
        url += pesquisa

        context['url'] = url
        return self.render_to_response(context)
