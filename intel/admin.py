from django.contrib import admin
from .intel_models import IntelReport, IntelReportDetails

# Register your models here.

admin.site.register(IntelReportDetails)
admin.site.register(IntelReport)
