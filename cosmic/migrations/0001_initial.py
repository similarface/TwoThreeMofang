# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CosmicMutant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('GENE_NAME', models.CharField(max_length=64, verbose_name='\u57fa\u56e0\u540d\u79f0')),
                ('ACCESSION_NUMBER', models.CharField(max_length=24, verbose_name='\u8f6c\u5f55\u672c')),
                ('GENE_CDS_LENGTH', models.IntegerField(null=True, verbose_name='\u57fa\u56e0\u957f\u5ea6')),
                ('HGNC_ID', models.IntegerField(null=True)),
                ('SAMPLE_NAME', models.CharField(max_length=38, null=True)),
                ('ID_SAMPLE', models.IntegerField(null=True)),
                ('ID_TUMOUR', models.IntegerField(null=True)),
                ('PRIMARY_SITE', models.CharField(max_length=200, null=True)),
                ('SITE_SUBTYPE_1', models.CharField(max_length=64, null=True)),
                ('SITE_SUBTYPE_2', models.CharField(max_length=64, null=True)),
                ('SITE_SUBTYPE_3', models.CharField(max_length=64, null=True)),
                ('PRIMARY_HISTOLOGY', models.CharField(max_length=300, null=True)),
                ('HISTOLOGY_SUBTYPE_1', models.CharField(max_length=200, null=True)),
                ('HISTOLOGY_SUBTYPE_2', models.CharField(max_length=200, null=True)),
                ('HISTOLOGY_SUBTYPE_3', models.CharField(max_length=200, null=True)),
                ('GENOME_WIDE_SCREEN', models.CharField(max_length=64, null=True)),
                ('MUTATION_ID', models.CharField(max_length=64, null=True)),
                ('MUTATION_CDS', models.CharField(max_length=120, null=True)),
                ('MUTATION_AA', models.CharField(max_length=64, null=True)),
                ('MUTATION_DESCRIPTION', models.CharField(max_length=64, null=True)),
                ('MUTATION_ZYGOSITY', models.CharField(max_length=64, null=True)),
                ('LOH', models.CharField(max_length=64, null=True)),
                ('GRCH', models.CharField(max_length=64, null=True)),
                ('MUTATION_GENOME_POSITION', models.CharField(max_length=64, null=True)),
                ('MUTATION_STRAND', models.CharField(max_length=64, null=True)),
                ('SNP', models.CharField(max_length=64, null=True)),
                ('FATHMM_PREDICTION', models.CharField(max_length=64, null=True)),
                ('FATHMM_SCORE', models.CharField(max_length=64, null=True)),
                ('MUTATION_SOMATIC_STATUS', models.CharField(max_length=64, null=True)),
                ('PUBMED_PMID', models.IntegerField(null=True)),
                ('ID_STUDY', models.CharField(max_length=64, null=True)),
                ('SAMPLE_SOURCE', models.CharField(max_length=64, null=True)),
                ('TUMOUR_ORIGIN', models.CharField(max_length=64, null=True)),
                ('AGE', models.CharField(max_length=24, null=True)),
            ],
        ),
    ]
