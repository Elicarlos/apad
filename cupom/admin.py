from django.contrib import admin
from .models import Cupom
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import resources
# Register your models here.

class CupomResource(resources.ModelResource):

	class Meta:
		model = Cupom


class CupomAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ( 'id','user', 'documentoFiscal', 'operador', 'dataCriacao', 'impresso', 'dataImpressao')
    search_fields = ( 'documentoFiscal__numeroDocumento','id', 'user__username')
    resource_class = CupomResource

admin.site.register(Cupom, CupomAdmin)
