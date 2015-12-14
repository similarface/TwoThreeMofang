# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PopulationGenetics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rsid', models.CharField(max_length=20)),
                ('Population', models.CharField(max_length=200)),
                ('Allele', models.CharField(max_length=200)),
                ('Genotype', models.CharField(max_length=200)),
                ('detail', models.CharField(max_length=30)),
            ],
        ),
    ]
