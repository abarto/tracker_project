from __future__ import absolute_import, unicode_literals

from kombu import Exchange
from kombu.common import Broadcast

notifications_exchange = Exchange('notifications', type='fanout')
notifications_queue = Broadcast('notifications', notifications_exchange, routing_key='notifications')