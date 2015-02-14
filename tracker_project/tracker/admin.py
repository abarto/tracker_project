from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import AreaOfInterest, Incident


admin.site.register(AreaOfInterest)
admin.site.register(Incident)
