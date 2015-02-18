from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from kombu import Connection
from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace


@namespace('/notifications')
class NotificationsNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger(self.__class__.__name__)

        super(NotificationsNamespace, self).__init__(*args, **kwargs)

    def recv_connect(self):
        self.spawn(self._dispatch)

    def _dispatch(self):
        with Connection(settings.AMPQ_URL) as connection:
            notifications_queue = connection.SimpleQueue('notifications')

            while True:
                message = notifications_queue.get(block=True, timeout=None)
                message.ack()

                self.emit('notification', message.payload)