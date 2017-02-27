# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chargenapp', '0004_character_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='primary_attribute',
            field=models.ForeignKey(related_name='primary_attr', default='', to='chargenapp.Attribute'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='secondary_attribute',
            field=models.ForeignKey(related_name='secondary_attr', default='', to='chargenapp.Attribute'),
            preserve_default=False,
        ),
    ]
