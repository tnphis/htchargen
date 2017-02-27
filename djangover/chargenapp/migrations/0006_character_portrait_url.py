# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chargenapp', '0005_auto_20151014_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='portrait_url',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
