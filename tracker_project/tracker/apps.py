from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class TrackerAppConfig(AppConfig):
    name = 'tracker'
    verbose_name = 'Tracker'

    def ready(self):
        from . import signals