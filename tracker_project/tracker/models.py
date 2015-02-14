from __future__ import absolute_import, unicode_literals

from django.contrib.gis.db import models


class Incident(models.Model):
    objects = models.GeoManager()

    URGENT = 'UR'
    HIGH = 'HI'
    MEDIUM = 'ME'
    LOW = 'LO'
    INFO = 'IN'

    SEVERITY_CHOICES = (
        (URGENT, 'Urgent'),
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
        (INFO, 'Info'),
    )

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    severity = models.CharField(max_length=2, choices=SEVERITY_CHOICES, default=MEDIUM)
    closed = models.BooleanField(default=False)
    location = models.PointField()
    created = models.DateTimeField(editable=False, auto_now_add=True)


class AreaOfInterest(models.Model):
    name = models.CharField(max_length=150)
    severity = models.CharField(max_length=2, choices=Incident.SEVERITY_CHOICES, default=Incident.MEDIUM)
    polygon = models.PolygonField()