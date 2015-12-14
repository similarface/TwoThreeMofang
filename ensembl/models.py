from django.db import models

# Create your models here.
class PopulationGenetics(models.Model):
    rsid=models.CharField(max_length=20,null=False)
    Population=models.CharField(max_length=200)
    Allele=models.CharField(max_length=200)
    Genotype=models.CharField(max_length=200)
    detail=models.CharField(max_length=30)