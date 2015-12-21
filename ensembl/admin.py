from django.contrib import admin

# Register your models here.
from models import PopulationGenetics,ModelInfo
class PopulationGeneticsAdmin(admin.ModelAdmin):
    # ...
    list_display = ('rsid', 'Population', 'Allele','Genotype','detail')

    list_filter = ['rsid']

    search_fields = ['rsid']

admin.site.register(PopulationGenetics,PopulationGeneticsAdmin)

admin.site.register(ModelInfo)

