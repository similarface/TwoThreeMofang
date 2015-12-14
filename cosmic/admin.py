from django.contrib import admin

# Register your models here.
from models import CosmicMutant
class CosmicMutantAdmin(admin.ModelAdmin):
    # ...
    list_display = ('GENE_NAME', 'ACCESSION_NUMBER', 'GENE_CDS_LENGTH','MUTATION_ID','MUTATION_CDS','MUTATION_AA','MUTATION_DESCRIPTION',)

    list_filter = ['GENE_NAME']

    search_fields = ['GENE_NAME']

admin.site.register(CosmicMutant,CosmicMutantAdmin)