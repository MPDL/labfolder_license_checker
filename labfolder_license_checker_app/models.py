from django.db import models
from django.db.models import Count, Sum


class Institute(models.Model):
    name = models.CharField(default=None, max_length=512, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Instance(models.Model):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    name = models.CharField(default=None, max_length=512, unique=True)
    moderator_name = models.CharField(default=None, null=True, blank=True, max_length=512)
    moderator_email = models.EmailField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

    def latest_report(self):
        return self.activityreport_set.latest('reportmonth')

    def active_users(self):
        return ActivityReportEntry.objects.filter(activity_report__instance=self).values('user_id').annotate(
            activity_count=Sum('activity_count'))

    def active_users_by_date(self, from_date, to_date):
        return ActivityReportEntry.objects.filter(activity_report__instance=self).filter(
            activity_report__reportmonth__range=[from_date, to_date]).values('user_id').annotate(
            activity_count=Sum('activity_count'))

    class Meta:
        ordering = ['name']


class ActivityReport(models.Model):
    instance = models.ForeignKey(Instance, on_delete=models.CASCADE)
    reportmonth = models.DateField(default=None)
    registered_users = models.BigIntegerField(default=None)
    active_users_last_6_months = models.BigIntegerField(default=None, null=True, blank=True)
    server_version = models.CharField(default=None, null=True, max_length=512)

    def entries(self):
        return self.activityreportentry_set.all()

    def __str__(self):
        return str(self.reportmonth) + " for " + str(self.instance)

    class Meta:
        unique_together = ('instance', 'reportmonth')
        ordering = ['-reportmonth', 'instance__name']


class ActivityReportEntry(models.Model):
    activity_report = models.ForeignKey(ActivityReport, on_delete=models.CASCADE)
    user_id = models.BigIntegerField()
    activity_count = models.BigIntegerField()

    class Meta:
        ordering = ['user_id']
