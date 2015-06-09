from django.db import models

from materia.models import MateriaLegislativa
from parlamentares.models import CargoMesa, Parlamentar, SessaoLegislativa, Legislatura


class TipoSessaoPlenaria(models.Model):
    nome_sessao = models.CharField(max_length=30)
    numero_minimo = models.IntegerField()


class SessaoPlenaria(models.Model):
    cod_andamento_sessao = models.IntegerField(blank=True, null=True)  # TODO lixo??? parece que era FK
    # andamento_sessao = models.ForeignKey(AndamentoSessao, blank=True, null=True)
    tipo = models.ForeignKey(TipoSessaoPlenaria)
    sessao_leg = models.ForeignKey(SessaoLegislativa)
    legislatura = models.ForeignKey(Legislatura)
    tipo_expediente = models.CharField(max_length=10)
    data_inicio_sessao = models.DateField()
    dia_sessao = models.CharField(max_length=15)
    hr_inicio_sessao = models.CharField(max_length=5)
    hr_fim_sessao = models.CharField(max_length=5, blank=True, null=True)
    numero_sessao_plen = models.IntegerField()
    data_fim_sessao = models.DateField(blank=True, null=True)
    url_audio = models.CharField(max_length=150, blank=True, null=True)
    url_video = models.CharField(max_length=150, blank=True, null=True)


class ExpedienteMateria(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    materia = models.ForeignKey(MateriaLegislativa)
    data_ordem = models.DateField()
    txt_observacao = models.TextField(blank=True, null=True)
    numero_ordem = models.IntegerField()
    txt_resultado = models.TextField(blank=True, null=True)
    tipo_votacao = models.IntegerField()


class TipoExpediente(models.Model):
    nome_expediente = models.CharField(max_length=100)


class ExpedienteSessaoPlenaria(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    expediente = models.ForeignKey(TipoExpediente)
    txt_expediente = models.TextField(blank=True, null=True)


class MesaSessaoPlenaria(models.Model):
    cargo = models.ForeignKey(CargoMesa)
    sessao_leg = models.ForeignKey(SessaoLegislativa)
    parlamentar = models.ForeignKey(Parlamentar)
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    excluido = models.NullBooleanField(blank=True)


class Oradores(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    parlamentar = models.ForeignKey(Parlamentar)
    numero_ordem = models.IntegerField()
    url_discurso = models.CharField(max_length=150, blank=True, null=True)


class OradoresExpediente(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    parlamentar = models.ForeignKey(Parlamentar)
    numero_ordem = models.IntegerField()
    url_discurso = models.CharField(max_length=150, blank=True, null=True)


class OrdemDia(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    materia = models.ForeignKey(MateriaLegislativa)
    data_ordem = models.DateField()
    txt_observacao = models.TextField(blank=True, null=True)
    numero_ordem = models.IntegerField()
    txt_resultado = models.TextField(blank=True, null=True)
    tipo_votacao = models.IntegerField()


class OrdemDiaPresenca(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    parlamentar = models.ForeignKey(Parlamentar)
    data_ordem = models.DateField()


class TipoResultadoVotacao(models.Model):
    nome_resultado = models.CharField(max_length=100)


class RegistroVotacao(models.Model):
    tipo_resultado_votacao = models.ForeignKey(TipoResultadoVotacao)
    materia = models.ForeignKey(MateriaLegislativa)
    ordem = models.ForeignKey(OrdemDia)
    numero_votos_sim = models.IntegerField()
    numero_votos_nao = models.IntegerField()
    numero_abstencao = models.IntegerField()
    txt_observacao = models.TextField(blank=True, null=True)


class RegistroVotacaoParlamentar(models.Model):
    votacao = models.ForeignKey(RegistroVotacao)
    parlamentar = models.ForeignKey(Parlamentar)
    vot_parlamentar = models.CharField(max_length=10)


class SessaoPlenariaPresenca(models.Model):
    sessao_plen = models.ForeignKey(SessaoPlenaria)
    parlamentar = models.ForeignKey(Parlamentar)
    data_sessao = models.DateField(blank=True, null=True)
