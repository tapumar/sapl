import re
import json
import logging
import socket
from urllib.parse import urlparse

from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http
from channels.security.websockets import AllowedHostsOnlyOriginValidator
from channels.sessions import channel_session

from django.conf import settings
from django.http.request import validate_host
from django.dispatch import receiver
from django.db.models.signals import post_save

from sapl.painel.views import get_dados
from sapl.sessao.models import (ExpedienteMateria, OrdemDia, PresencaOrdemDia,
                                RegistroVotacao, SessaoPlenaria,
                                SessaoPlenariaPresenca, VotoParlamentar)

log = logging.getLogger(__name__)


# Decorator para restringir o acesso a conexão web sockets
class ChannelAllowedHosts(AllowedHostsOnlyOriginValidator):
    def validate_origin(self, message, origin):
        allowed_hosts = settings.ALLOWED_HOSTS
        if settings.DEBUG:
            allowed_hosts = ['localhost', '127.0.0.1', '[::1]']
        else:
            allowed_hosts = [socket.getfqdn()]

        origin_hostname = urlparse(origin).hostname
        valid = (origin_hostname and
                 validate_host(origin_hostname, allowed_hosts))
        return valid


allowed_hosts_only = AllowedHostsOnlyOriginValidator


# Função genérica que envia um JSON para o template do painel com as
# informações atualizadas
def painel_update(pk):
    Group("painel-%s" % pk).send({
        "text": json.dumps(get_dados(pk))
    })


##################### Signals ##########################

# Tabelas que, quando os dados sofrem alterações, podem
# modificar as informações mostradas no painel.
# Sendo assim, quando algum dado nelas é atualizado, o
# painel também é

@receiver(post_save, sender=RegistroVotacao)
def send_update_votacao(sender, instance, **kwargs):
    if instance.ordem:
        pk = instance.ordem.sessao_plenaria_id
    else:
        pk = instance.expediente.sessao_plenaria_id
    painel_update(pk)


@receiver(post_save, sender=VotoParlamentar)
def send_update_voto_parlamentar(sender, instance, **kwargs):
    if instance.ordem:
        pk = instance.ordem.sessao_plenaria_id
    else:
        pk = instance.expediente.sessao_plenaria_id
    painel_update(pk)


@receiver(post_save, sender=OrdemDia)
def send_update_ordem(sender, instance, **kwargs):
    painel_update(instance.sessao_plenaria_id)


@receiver(post_save, sender=ExpedienteMateria)
def send_update_expediente(sender, instance, **kwargs):
    painel_update(instance.sessao_plenaria_id)


@receiver(post_save, sender=SessaoPlenaria)
def send_update_sessao(sender, instance, **kwargs):
    painel_update(instance.id)


# TODO Utilizar signals para atualizar as presenças
# @receiver(post_save, sender=SessaoPlenariaPresenca)
# def send_update_presenca_sessao(sender, instance, **kwargs):
#     painel_update(instance.sessao_plenaria_id)
#
#
# @receiver(post_save, sender=PresencaOrdemDia)
# def send_update_presenca_ordem(sender, instance, **kwargs):
#     painel_update(instance.sessao_plenaria_id)


##### Ao abrir o painel no browser, este método é chamado #######
@allowed_hosts_only
@channel_session_user_from_http
def ws_connect(message):
    '''
    Cria uma conexão entre o painel(cliente) e o servidor, por meio de um
    grupo identificado pela PK da Sessão a qual aquele Painel pertence
    '''

    # Ao acessar o painel, ele abre uma conexão web sockets e envia sua url
    url = message.get('path', None)
    if url:
        url = url.split('/')
        # Dentro desta url contém a pk da sessão
        sessao_pk = url[len(url) - 1]

        if SessaoPlenaria.objects.filter(id=int(sessao_pk)).exists():
            # Add to reader group
            Group('painel-%s' % sessao_pk,
                  channel_layer=message.channel_layer).add(message.reply_channel)
            sessao_pk = int(sessao_pk)
            # Accept the connection request
            message.reply_channel.send({"accept": True})
            message.channel_session['painel'] = sessao_pk

            # Ao completar a conexão, os dados do painel são enviados ao template
            Group("painel-%s" % sessao_pk).send({
                "text": json.dumps(get_dados(sessao_pk))
            })


# Ao fechar o painel no browser, a conexão é fechada
@channel_session_user_from_http
def ws_disconnect(message):
    '''
    Remove o grupo quando o painel é fechado no browser
    '''
    try:
        pk = message.channel_session['painel']
        sessao = SessaoPlenaria.objects.get(id=int(pk))
        Group('painel-%s' % pk, channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, SessaoPlenaria.DoesNotExist):
        pass