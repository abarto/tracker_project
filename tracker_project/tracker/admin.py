from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import Incident


admin.site.register(Incident)
