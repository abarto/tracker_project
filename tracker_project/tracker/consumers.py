import logging

from channels import Group
from channels.decorators import channel_session
from channels.auth import http_session_user, channel_session_user, transfer_user

logger = logging.getLogger(__name__)

# Connected to websocket.connect and websocket.keepalive
@http_session_user
@channel_session
def websocket_connect(message):
    logger.info('websocket_connect. message = %s', message)
    transfer_user(message.http_session, message.channel_session)
    Group("notifications").add(message.reply_channel)

# Connected to websocket.keepalive
@channel_session
def websocket_keepalive(message):
    logger.info('websocket_keepalive. message = %s', message)
    Group("notifications").add(message.reply_channel)


# Connected to websocket.disconnect
@channel_session_user
def websocket_disconnect(message):
    logger.info('websocket_disconnect. message = %s', message)
    Group("notifications").discard(message.reply_channel)
