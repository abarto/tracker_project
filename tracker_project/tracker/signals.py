from __future__ import absolute_import, unicode_literals

from json import dumps

from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels import Group

from .models import Incident, AreaOfInterest
from .queues import notifications_exchange


def send_notification(notification):
    Group("notifications").send({'content': dumps(notification)})


@receiver(post_save, sender=Incident)
def incident_post_save(sender, **kwargs):
    send_notification({
        'type': 'post_save',
        'created': kwargs['created'],
        'feature': kwargs['instance'].geojson_feature
    })

    if not kwargs['instance'].closed:
        areas_of_interest = [
            area_of_interest.geojson_feature for area_of_interest in AreaOfInterest.objects.filter(
                polygon__contains=kwargs['instance'].location,
                severity__in=kwargs['instance'].alert_severities,
            )
        ]

        if areas_of_interest:
            send_notification(dict(
                type='alert',
                feature=kwargs['instance'].geojson_feature,
                areas_of_interest=[
                    {
                        'id': area_of_interest['id'],
                        'name': area_of_interest['properties']['name'],
                        'severity': area_of_interest['properties']['severity'],
                        'url': area_of_interest['properties']['url'],
                    }
                    for area_of_interest in areas_of_interest
                ]
            ))


@receiver(post_save, sender=AreaOfInterest)
def area_of_interest_post_save(sender, **kwargs):
    send_notification({
        'type': 'post_save',
        'created': kwargs['created'],
        'feature': kwargs['instance'].geojson_feature
    })


@receiver(post_delete, sender=Incident)
@receiver(post_delete, sender=AreaOfInterest)
def post_delete(sender, **kwargs):
    send_notification({
        'type': 'post_delete',
        'feature': kwargs['instance'].geojson_feature
    })
