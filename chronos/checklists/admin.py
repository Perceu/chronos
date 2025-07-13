from django.contrib import admin

from chronos.checklists.models import Checklist, ChecklistItem

class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItem

class ChecklistAdmin(admin.ModelAdmin):
    inlines = [ChecklistItemInline]

admin.site.register(Checklist, ChecklistAdmin)
