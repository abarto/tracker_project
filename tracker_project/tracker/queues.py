from __future__ import absolute_import, unicode_literals

from kombu import Exchange

notifications_exchange = Exchange('notifications', type='fanout')