from django.db import models

# Create your models here.
class PopulationGenetics(models.Model):
    rsid=models.CharField(max_length=20,null=False)
    Population=models.CharField(max_length=200)
    Allele=models.CharField(max_length=200)
    Genotype=models.CharField(max_length=200)
    detail=models.CharField(max_length=30)

class SelfPopulationGenetics(models.Model):
    chrom=models.CharField(max_length=18,null=False)
    pos=models.CharField(max_length=18,null=False)
    rsid=models.CharField(max_length=18,null=False)
    ATGC=models.CharField(max_length=200)
    AATTGGCC=models.CharField(max_length=200)
    class Meta:
        managed=False
        db_table='mofang_populationgenetics'

class ModelInfo(models.Model):
    TABLE_SCHEMA=models.CharField(max_length=64)
    TABLE_NAME=models.CharField(max_length=64)
    COLUMN_NAME=models.CharField(max_length=64)
    COLUMN_COMMENT=models.CharField(max_length=1024)
    class Meta:
        managed=False
        db_table='ModelInfo'