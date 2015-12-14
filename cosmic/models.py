#coding:utf-8
from django.db import models

# Create your models here.
def decode(info):
    return info.decode('utf-8')

class CosmicMutant(models.Model):
    GENE_NAME=models.CharField(decode('基因名称'),max_length=64)
    ACCESSION_NUMBER=models.CharField(decode('转录本'),max_length=24)
    GENE_CDS_LENGTH=models.IntegerField(decode('基因长度'),null=True)
    HGNC_ID=models.IntegerField(null=True)
    SAMPLE_NAME=models.CharField(max_length=38,null=True)
    ID_SAMPLE=models.IntegerField(null=True)
    ID_TUMOUR=models.IntegerField(null=True)
    PRIMARY_SITE=models.CharField(max_length=200,null=True)
    SITE_SUBTYPE_1=models.CharField(max_length=64,null=True)
    SITE_SUBTYPE_2=models.CharField(max_length=64,null=True)
    SITE_SUBTYPE_3=models.CharField(max_length=64,null=True)
    PRIMARY_HISTOLOGY=models.CharField(max_length=300,null=True)
    HISTOLOGY_SUBTYPE_1=models.CharField(max_length=200,null=True)
    HISTOLOGY_SUBTYPE_2=models.CharField(max_length=200,null=True)
    HISTOLOGY_SUBTYPE_3=models.CharField(max_length=200,null=True)
    GENOME_WIDE_SCREEN=models.CharField(max_length=64,null=True)
    MUTATION_ID=models.CharField(max_length=64,null=True)
    MUTATION_CDS=models.CharField(max_length=120,null=True)
    MUTATION_AA=models.CharField(max_length=64,null=True)
    MUTATION_DESCRIPTION=models.CharField(max_length=64,null=True)
    MUTATION_ZYGOSITY=models.CharField(max_length=64,null=True)
    LOH=models.CharField(max_length=64,null=True)
    GRCH=models.CharField(max_length=64,null=True)
    MUTATION_GENOME_POSITION=models.CharField(max_length=64,null=True)
    MUTATION_STRAND=models.CharField(max_length=64,null=True)
    SNP=models.CharField(max_length=64,null=True)
    FATHMM_PREDICTION=models.CharField(max_length=64,null=True)
    FATHMM_SCORE=models.CharField(max_length=64,null=True)
    MUTATION_SOMATIC_STATUS=models.CharField(max_length=64,null=True)
    PUBMED_PMID=models.IntegerField(null=True)
    ID_STUDY=models.CharField(max_length=64,null=True)
    SAMPLE_SOURCE=models.CharField(max_length=64,null=True)
    TUMOUR_ORIGIN=models.CharField(max_length=64,null=True)
    AGE=models.CharField(max_length=24,null=True)




