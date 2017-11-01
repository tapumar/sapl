from channels.staticfiles import StaticFilesConsumer
from . import consumers

channel_routing = {
    # Wire up websocket channels to our consumers:
    'websocket.connect': consumers.ws_connect,
    'websocket.disconnect': consumers.ws_disconnect,
}