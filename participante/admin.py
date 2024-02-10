from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, DocumentoFiscal
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from import_export.admin import ImportExportActionModelAdmin

class UserResource(resources.ModelResource):

    class Meta:
        model = User

class MyUserAdmin(ImportExportActionModelAdmin, ImportExportModelAdmin, UserAdmin):
	resource_class = UserResource

class ProfileResource(resources.ModelResource):

    class Meta:
        model = Profile

class DocumentoFiscalResource(resources.ModelResource):

    class Meta:
        model = DocumentoFiscal


class ProfileAdmin(ImportExportModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo', 'CHOICES_SEXO', 'nome', 'RG', 'CPF', 'sexo', 'foneFixo',
                    'foneCelular1', 'foneCelular2', 'foneCelular3', 'whatsapp', 'facebook', 'twitter',
                    'endereco', 'enderecoNumero', 'enderecoComplemento', 'bairro', 'cidade', 'estado', 'CEP', 'cadastradoPor',
                    'dataCadastro', 'observacao', 'pergunta', 'ativo']
    search_fields = ('CPF', 'nome')
    resource_class = ProfileResource

class DocumentoFiscalAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user', 'numeroDocumento', 'lojista', 'vendedor', 'dataDocumento', 'valorDocumento', 'compradoREDE', 'compradoMASTERCARD',
     'valorREDE','valorMASTERCARD', 'valorVirtual', 'dataCadastro', 'cadastradoPor']

    search_fields = ('numeroDocumento', 'user__username',)
    resource_class = DocumentoFiscalResource


class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'
    readonly_fields = ('action_time',)
    list_filter = ['user', 'content_type']
    search_fields = ['object_repr', 'change_message']
    list_display = ['__str__', 'content_type', 'action_time', 'user', 'object_link']

    # keep only view permission
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = obj.object_repr
        else:
            ct = obj.content_type
            try:
                link = mark_safe('<a href="%s">%s</a>' % (
                                 reverse('admin:%s_%s_change' % (ct.app_label, ct.model),
                                         args=[obj.object_id]),
                                 escape(obj.object_repr),
                ))
            except NoReverseMatch:
                link = obj.object_repr
        return link
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = 'object'

    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(DocumentoFiscal, DocumentoFiscalAdmin)
