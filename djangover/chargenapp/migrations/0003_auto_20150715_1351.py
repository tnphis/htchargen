# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chargenapp', '0002_auto_20150715_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='RacialAttrModifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('attribute', models.ForeignKey(to='chargenapp.Attribute')),
                ('gender', models.ForeignKey(to='chargenapp.Gender')),
                ('race', models.ForeignKey(to='chargenapp.Race')),
            ],
        ),
        migrations.RenameModel(
            old_name='RacialFeats',
            new_name='RacialFeat',
        ),
        migrations.AlterUniqueTogether(
            name='racialattrmodifiers',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='racialattrmodifiers',
            name='attribute',
        ),
        migrations.RemoveField(
            model_name='racialattrmodifiers',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='racialattrmodifiers',
            name='race',
        ),
        migrations.DeleteModel(
            name='RacialAttrModifiers',
        ),
        migrations.AlterUniqueTogether(
            name='racialattrmodifier',
            unique_together=set([('race', 'gender', 'attribute')]),
        ),
    ]
