from django.contrib import admin
from .models import Cupom
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin
from import_export import resources
from import_export import resources, fields
# Register your models here.

class CupomResource(resources.ModelResource):
    nome_participante = fields.Field(attribute='user__profile__nome', column_name='Nome do Participante')
    cpf_participante = fields.Field(attribute='user__profile__CPF', column_name='CPF do Participante')
    numero_documento_fiscal = fields.Field(attribute='documentoFiscal__numeroDocumento', column_name='Número do Documento Fiscal')

    class Meta:
        model = Cupom
        fields = ('nome_participante', 'cpf_participante', 'numero_documento_fiscal', 'dataCriacao', 'impresso', 'dataImpressao')
        export_order = ('nome_participante', 'cpf_participante', 'numero_documento_fiscal', 'dataCriacao', 'impresso', 'dataImpressao')



class CupomAdmin(ImportExportActionModelAdmin,ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ( 'id','user', 'documentoFiscal', 'operador', 'dataCriacao', 'impresso', 'dataImpressao')
    search_fields = ( 'documentoFiscal__numeroDocumento','id', 'user__username')
    resource_class = CupomResource

admin.site.register(Cupom, CupomAdmin)
