from __future__ import absolute_import, unicode_literals

import logging

from django.conf import settings
from kombu import BrokerConnection
from kombu.mixins import ConsumerMixin
from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace

from .queues import notifications_queue


@namespace('/notifications')
class NotificationsNamespace(BaseNamespace):
    def __init__(self, *args, **kwargs):
        super(NotificationsNamespace, self).__init__(*args, **kwargs)

    def get_initial_acl(self):
        return ['recv_connect']

    def recv_connect(self):
        if self.request.user.is_authenticated():
            self.lift_acl_restrictions()
            self.spawn(self._dispatch)
        else:
            self.disconnect(silent=True)

    def _dispatch(self):
        with BrokerConnection(settings.AMPQ_URL) as connection:
            NotificationsConsumer(connection, self.socket, self.ns_name).run()


class NotificationsConsumer(ConsumerMixin):
    def __init__(self, connection, socket, ns_name):
        self.connection = connection
        self.socket = socket
        self.ns_name = ns_name

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[notifications_queue], callbacks=[self.process_notification])]

    def process_notification(self, body, message):
        self.socket.send_packet(dict(
            type='event',
            name='notification',
            args=(body,),
            endpoint=self.ns_name
        ))
        message.ack()