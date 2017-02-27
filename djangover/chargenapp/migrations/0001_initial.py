# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('level', models.PositiveSmallIntegerField()),
                ('point_pool', models.PositiveSmallIntegerField()),
                ('wealth', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CharacterAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField()),
                ('attribute', models.ForeignKey(to='chargenapp.Attribute')),
                ('character', models.ForeignKey(to='chargenapp.Character')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterFeat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.ForeignKey(to='chargenapp.Character')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterSkill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.SmallIntegerField()),
                ('character', models.ForeignKey(to='chargenapp.Character')),
            ],
        ),
        migrations.CreateModel(
            name='CharacterSkillTraining',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.ForeignKey(to='chargenapp.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Feat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=4000)),
                ('point_cost', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FeatType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RacialAttrModifiers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField()),
                ('attribute', models.ForeignKey(to='chargenapp.Attribute')),
                ('gender', models.ForeignKey(to='chargenapp.Gender')),
                ('race', models.ForeignKey(to='chargenapp.Race')),
            ],
        ),
        migrations.CreateModel(
            name='RacialFeats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feat', models.ForeignKey(to='chargenapp.Feat')),
                ('race', models.ForeignKey(to='chargenapp.Race')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SkillGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SkillTrainingLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SocialBackground',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=50)),
                ('starting_wealth', models.PositiveIntegerField()),
                ('point_cost', models.SmallIntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='socialbackground',
            unique_together=set([('value',)]),
        ),
        migrations.AlterUniqueTogether(
            name='skilltraininglevel',
            unique_together=set([('value',)]),
        ),
        migrations.AlterUniqueTogether(
            name='skillgroup',
            unique_together=set([('name',)]),
        ),
        migrations.AddField(
            model_name='skill',
            name='group',
            field=models.ForeignKey(to='chargenapp.SkillGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='settings',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='race',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='gender',
            unique_together=set([('value',)]),
        ),
        migrations.AlterUniqueTogether(
            name='feattype',
            unique_together=set([('value',)]),
        ),
        migrations.AddField(
            model_name='feat',
            name='feat_type',
            field=models.ForeignKey(to='chargenapp.FeatType'),
        ),
        migrations.AddField(
            model_name='characterskilltraining',
            name='skill',
            field=models.ForeignKey(to='chargenapp.Skill'),
        ),
        migrations.AddField(
            model_name='characterskilltraining',
            name='value',
            field=models.ForeignKey(to='chargenapp.SkillTrainingLevel'),
        ),
        migrations.AddField(
            model_name='characterskill',
            name='skill',
            field=models.ForeignKey(to='chargenapp.Skill'),
        ),
        migrations.AddField(
            model_name='characterfeat',
            name='feat',
            field=models.ForeignKey(to='chargenapp.Feat'),
        ),
        migrations.AddField(
            model_name='character',
            name='gender',
            field=models.ForeignKey(to='chargenapp.Gender'),
        ),
        migrations.AddField(
            model_name='character',
            name='race',
            field=models.ForeignKey(to='chargenapp.Race'),
        ),
        migrations.AddField(
            model_name='character',
            name='social_background',
            field=models.ForeignKey(to='chargenapp.SocialBackground'),
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set([('name',), ('code',)]),
        ),
        migrations.AlterUniqueTogether(
            name='skill',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='racialfeats',
            unique_together=set([('race', 'feat')]),
        ),
        migrations.AlterUniqueTogether(
            name='racialattrmodifiers',
            unique_together=set([('race', 'gender', 'attribute')]),
        ),
        migrations.AlterUniqueTogether(
            name='feat',
            unique_together=set([('name',)]),
        ),
        migrations.AlterUniqueTogether(
            name='characterskilltraining',
            unique_together=set([('character', 'skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterskill',
            unique_together=set([('character', 'skill')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterfeat',
            unique_together=set([('character', 'feat')]),
        ),
        migrations.AlterUniqueTogether(
            name='characterattribute',
            unique_together=set([('character', 'attribute')]),
        ),
    ]
