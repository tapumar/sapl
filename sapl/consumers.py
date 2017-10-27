import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from django.dispatch import receiver
from django.db.models.signals import post_save

from sapl.painel.views import get_dados
from sapl.sessao.models import (ExpedienteMateria, OrdemDia,
                                RegistroVotacao, SessaoPlenaria, VotoParlamentar)

log = logging.getLogger(__name__)


def painel_update(pk):
    Group("painel-%s" % pk).send({
        "text": json.dumps(get_dados(pk))
    })


@receiver(post_save, sender=RegistroVotacao)
def send_update(sender, instance, **kwargs):
    if instance.ordem:
        pk = instance.ordem.sessao_plenaria_id
    else:
        pk = instance.expediente.sessao_plenaria_id
    painel_update(pk)


@receiver(post_save, sender=VotoParlamentar)
def send_update(sender, instance, **kwargs):
    if instance.ordem:
        pk = instance.ordem.sessao_plenaria_id
    else:
        pk = instance.expediente.sessao_plenaria_id
    painel_update(pk)


@receiver(post_save, sender=OrdemDia)
def send_update(sender, instance, **kwargs):
    painel_update(instance.sessao_plenaria_id)


@receiver(post_save, sender=ExpedienteMateria)
def send_update(sender, instance, **kwargs):
    painel_update(instance.sessao_plenaria_id)


@channel_session
def ws_connect(message):
    url = message.get('path', None)
    if url:
        url = url.split('/')
        sessao_pk = url[len(url) - 1]

        if SessaoPlenaria.objects.filter(id=int(sessao_pk)).exists():
            # Add to reader group
            Group('painel-' + sessao_pk, channel_layer=message.channel_layer).add(message.reply_channel)
            sessao_pk = int(sessao_pk)
            # Accept the connection request
            message.reply_channel.send({"accept": True})
            message.channel_session['painel'] = sessao_pk

            Group("painel-%s" % sessao_pk).send({
                "text": json.dumps(get_dados(sessao_pk))
            })


# Connected to websocket.disconnect
def ws_disconnect(message):
    # Remove from reader group on clean disconnect
    try:
        pk = message.channel_session['painel']
        sessao = SessaoPlenaria.objects.get(id=int(pk))
        Group('painel-%s' % pk, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, SessaoPlenaria.DoesNotExist):
        pass