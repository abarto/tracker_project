from __future__ import absolute_import, unicode_literals

from django.contrib.gis.db import models
from geojson import Feature, loads


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

    @property
    def geojson_feature(self):
        return Feature(
            geometry=loads(self.location.geojson),
            id='Incident:{id}'.format(id=self.id),
            properties={
                'name': self.name,
                'description': self.description,
                'severity': self.get_severity_display(),
                'created': str(self.created),
                'closed': self.closed
            }
        )


class AreaOfInterest(models.Model):
    name = models.CharField(max_length=150)
    severity = models.CharField(max_length=2, choices=Incident.SEVERITY_CHOICES, default=Incident.MEDIUM)
    polygon = models.PolygonField()

    @property
    def geojson_feature(self):
        return Feature(
            geometry=loads(self.polygon.geojson),
            id='AreaOfInterest:{id}'.format(id=self.id),
            properties={
                'name': self.name,
                'severity': self.get_severity_display()
            }
        )