from django.contrib import admin

from labfolder_license_checker_app.models import Institute, Instance, ActivityReport, ActivityReportEntry


class InstanceInline(admin.StackedInline):
    model = Instance


class InstituteAdmin(admin.ModelAdmin):
    inlines = [InstanceInline,]


class ActivityReportEntryInline(admin.StackedInline):
    model = ActivityReportEntry


class ActivityReportAdmin(admin.ModelAdmin):
    inlines = [ActivityReportEntryInline,]


admin.site.register(Institute, InstituteAdmin)
admin.site.register(Instance)
admin.site.register(ActivityReport, ActivityReportAdmin)
