# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaOfInterest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('severity', models.CharField(default='ME', max_length=2, choices=[('UR', 'Urgent'), ('HI', 'High'), ('ME', 'Medium'), ('LO', 'Low'), ('IN', 'Info')])),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
