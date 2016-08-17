from django import forms


class PesquisaLexmlForm(forms.Form):
    conteudo = forms.CharField(required=False, max_length='20')
