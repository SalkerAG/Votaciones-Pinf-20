from django.contrib import admin
from .models import Censo
from import_export.admin import ImportExportModelAdmin


#admin.site.register(Censo)

@admin.register(Censo)
class ViewAdmin(ImportExportModelAdmin):
    pass