from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
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

    ALERT_SEVERITIES = {
        URGENT: (URGENT, HIGH, MEDIUM, LOW, INFO),
        HIGH: (HIGH, MEDIUM, LOW, INFO),
        MEDIUM: (MEDIUM, LOW, INFO),
        LOW: (LOW, INFO),
        INFO: (INFO,),
    }

    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    severity = models.CharField(max_length=2, choices=SEVERITY_CHOICES, default=MEDIUM)
    closed = models.BooleanField(default=False)
    location = models.PointField()
    created = models.DateTimeField(editable=False, auto_now_add=True)

    @property
    def alert_severities(self):
        return Incident.ALERT_SEVERITIES[self.severity]

    @property
    def geojson_feature(self):
        return Feature(
            geometry=loads(self.location.geojson),
            id='Incident:{pk}'.format(pk=self.pk),
            properties={
                'name': self.name,
                'description': self.description,
                'severity': self.get_severity_display(),
                'created': str(self.created),
                'closed': self.closed,
                'model': 'Incident',
                'pk': self.pk,
                'url': reverse('tracker:incident-detail', kwargs={'pk': self.pk}),
            }
        )


class AreaOfInterest(models.Model):
    name = models.CharField(max_length=150)
    severity = models.CharField(max_length=2, choices=Incident.SEVERITY_CHOICES, default=Incident.MEDIUM)
    polygon = models.PolygonField()

    @property
    def path_expression(self):
        return '|'.join('{y},{x}'.format(x=x, y=y) for x, y in self.polygon[0])

    @property
    def geojson_feature(self):
        return Feature(
            geometry=loads(self.polygon.geojson),
            id='AreaOfInterest:{pk}'.format(pk=self.pk),
            properties={
                'name': self.name,
                'severity': self.get_severity_display(),
                'centroid': self.polygon.centroid.geojson,
                'model': 'AreaOfInterest',
                'pk': self.pk,
                'url': reverse('tracker:area-of-interest-detail', kwargs={'pk': self.pk}),
            }
        )