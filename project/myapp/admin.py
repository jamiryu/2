from django.contrib import admin
from .models import WeldRecord

@admin.register(WeldRecord)
class WeldRecordAdmin(admin.ModelAdmin):
    list_display = ('weld_no', 'isometri_no', 'spool_no', 'weld_date', 'weld_result')
