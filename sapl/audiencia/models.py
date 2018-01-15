import reversion
from django.db import models
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

from sapl.materia.models import MateriaLegislativa
from sapl.parlamentares.models import (CargoMesa, Parlamentar)

from sapl.utils import (YES_NO_CHOICES, SaplGenericRelation,
                        restringe_tipos_de_arquivo_txt, texto_upload_path)

def get_audiencia_media_path(instance, subpath, filename):
    return './sapl/audiencia/%s/%s/%s' % (instance.numero, subpath, filename)


def pauta_upload_path(instance, filename):
    return texto_upload_path(
        instance, filename, subpath='pauta', pk_first=True)
    # return get_sessao_media_path(instance, 'pauta', filename)


def ata_upload_path(instance, filename):
    return texto_upload_path(instance, filename, subpath='ata', pk_first=True)
    # return get_sessao_media_path(instance, 'ata', filename)


def anexo_upload_path(instance, filename):
    return texto_upload_path(
        instance, filename, subpath='anexo', pk_first=True)
    # return get_sessao_media_path(instance, 'anexo', filename)


@reversion.register()
class AudienciaPublica(models.Model):
	materia = models.ForeignKey(
		MateriaLegislativa,
		on_delete=models.PROTECT,
		verbose_name=_(Matéria Legislativa))
	numero = models.PositiveIntegerField(verbose_name=_('Número'))
	nome = models.CharField(
	    max_length=100, verbose_name=_('Nome da Audiência Pública'))
	tema = models.CharField(
	    max_length=100, verbose_name=_('Tema da Audiência Pública'))
	data = models.DateField(verbose_name=_('Data'))
	hora_inicio = models.CharField(
	    max_length=5, verbose_name=_('Horário (hh:mm)'))
	hora_fim = models.CharField(
	    max_length=5, verbose_name=_('Horário (hh:mm)'))
	local_reuniao = models.CharField(
	    max_length=100, blank=True, verbose_name=_('Local da Audiência Pública'))
	observacao = models.CharField(
	    max_length=150, blank=True, verbose_name=_('Observação'))
	url_audio = models.URLField(
	    max_length=150, blank=True,
	    verbose_name=_('URL Arquivo Áudio (Formatos MP3 / AAC)'))
	url_video = models.URLField(
	    max_length=150, blank=True,
	    verbose_name=_('URL Arquivo Vídeo (Formatos MP4 / FLV / WebM)'))
	upload_pauta = models.FileField(
	    blank=True,
	    null=True,
	    upload_to=pauta_upload_path,
	    verbose_name=_('Pauta da Audiência Pública'),
	    validators=[restringe_tipos_de_arquivo_txt])
	upload_ata = models.FileField(
	    blank=True,
	    null=True,
	    upload_to=ata_upload_path,
	    verbose_name=_('Ata da Audiência Pública'),
	    validators=[restringe_tipos_de_arquivo_txt])
	upload_anexo = models.FileField(
	    blank=True,
	    null=True,
	    upload_to=anexo_upload_path,
	    verbose_name=_('Anexo da Audiência Pública'))

 	class Meta:
        verbose_name = _('Audiência Pública')
        verbose_name_plural = _('Audiências Públicas')

    def __str__(self):
        return self.nome

    def delete(self, using=None, keep_parents=False):
        if self.upload_pauta:
            self.upload_pauta.delete()

        if self.upload_ata:
            self.upload_ata.delete()

        if self.upload_anexo:
            self.upload_anexo.delete()

        return models.Model.delete(
            self, using=using, keep_parents=keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if not self.pk and (self.upload_pauta or self.upload_ata or
                            self.upload_anexo):
            upload_pauta = self.upload_pauta
            upload_ata = self.upload_ata
            upload_anexo = self.upload_anexo
            self.upload_pauta = None
            self.upload_ata = None
            self.upload_anexo = None
            models.Model.save(self, force_insert=force_insert,
                              force_update=force_update,
                              using=using,
                              update_fields=update_fields)

            self.upload_pauta = upload_pauta
            self.upload_ata = upload_ata
            self.upload_anexo = upload_anexo

        return models.Model.save(self, force_insert=force_insert,
                                 force_update=force_update,
                                 using=using,
                                 update_fields=update_fields)


@reversion.register()
class PresencaInterna(models.Model):  
    audiencia = models.ForeignKey(AudienciaPublica,
                                  on_delete=models.PROTECT,
                                  verbose_name=Audiência Pública)
    cargo = models.ForeignKey(CargoMesa, on_delete=models.PROTECT)
    parlamentar = models.ForeignKey(Parlamentar, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _('Presença Interna da Audiência Pública')
        verbose_name_plural = _('Presenças Interna da Audiência Pública')

    def __str__(self):
        return '%s - %s' % (self.cargo, self.parlamentar)


@reversion.register()
class PresencaExterna(models.Model):
	FEMININO = 'F'
    MASCULINO = 'M'
    SEXO_CHOICE = ((FEMININO, _('Feminino')),
                   (MASCULINO, _('Masculino')))
  	audiencia = models.ForeignKey(AudienciaPublica,
	                              on_delete=models.PROTECT,
	                              verbose_name=Audiência Pública)
  	nome_completo = models.CharField(
        max_length=50, verbose_name=_('Nome Completo'))
  	sexo = models.CharField(
        max_length=1, verbose_name=_('Sexo'), choices=SEXO_CHOICE)
    data_nascimento = models.DateField(
        blank=True, null=True, verbose_name=_('Data Nascimento'))
    cpf = models.CharField(
        max_length=14, blank=True, verbose_name=_('C.P.F'))
    rg = models.CharField(
        max_length=15, blank=True, verbose_name=_('R.G.'))
    titulo_eleitor = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_('Título de Eleitor'))
    telefone = models.CharField(
        max_length=50, blank=True, verbose_name=_('Telefone'))
    email = models.EmailField(
        max_length=100,
        blank=True,
        verbose_name=_('E-mail'))



