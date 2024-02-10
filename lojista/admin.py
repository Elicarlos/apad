from django.contrib import admin
from .models import Lojista, RamoAtividade
import csv
from django.http import HttpResponse
from django import forms
from django.urls import include, path
from django.shortcuts import render, redirect
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse

class LojistaResource(resources.ModelResource):

    class Meta:
        model = Lojista

class RamoAtividadeResource(resources.ModelResource):

    class Meta:
        model = RamoAtividade

class LojistaAdmin(ImportExportModelAdmin):
    list_display = ['id','CNPJLojista', 'IELojista', 'razaoLojista', 'fantasiaLojista',
                         'ramoAtividade', 'dataCadastro', 'CadastradoPor', 'ativo' ]
    search_fields = ('fantasiaLojista', 'ramoAtividade__atividade', 'CNPJLojista')
    resource_class = LojistaResource

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class RamoAtividadeAdmin(ImportExportModelAdmin):
    list_display = ['atividade', 'dataCadastro', 'CadastradoPor', 'ativo']
    actions = ["export_as_csv"]
    resource_class = RamoAtividadeResource

# class LojistaAdmin(admin.ModelAdmin, ExportCsvMixin):
#     list_display = ['CNPJLojista', 'IELojista', 'razaoLojista', 'fantasiaLojista',
#                         'ramoAtividade', 'dataCadastro', 'CadastradoPor', 'ativo' ]
#     search_fields = ('fantasiaLojista', 'ramoAtividade__atividade', 'CNPJLojista')
#     actions = ["export_as_csv"]

#     change_list_template = "lojista/lojistas_changelist.html"

#     def get_urls(self):
#         urls = super().get_urls()
#         my_urls = [
#             path('import-csv/', self.import_csv),
#         ]
#         return my_urls + urls

#     def import_csv(self, request):
#         if request.method == "POST":
#             csv_file = request.FILES["csv_file"]
#             reader = csv.reader(csv_file)
#             # Create Hero objects from passed in data
#             # ...
#             self.message_user(request, "Your csv file has been imported")
#             return redirect("..")
#         form = CsvImportForm()
#         payload = {"form": form}
#         return render(
#             request, "lojista/csv_form.html", payload
#             )

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


admin.site.register(Lojista, LojistaAdmin)
admin.site.register(RamoAtividade, RamoAtividadeAdmin)
