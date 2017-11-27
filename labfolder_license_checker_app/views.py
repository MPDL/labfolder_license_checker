import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory

from labfolder_license_checker_app.models import Instance, ActivityReport, ActivityReportEntry
from . import models
import logging

logger = logging.getLogger(__name__)
import re
from . import controller
from django.db import IntegrityError
from django.contrib import messages
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Sum, Max, F


def instance_overview(request):
    if request.method == 'POST':
        date_from_input = request.POST.get('date_from_input');
        date_to_input = request.POST.get('date_to_input');
        date_format = '%Y-%m-%d'
        # First day of selected month
        date_from = datetime.datetime.strptime(date_from_input, date_format).replace(day=1)
        #Last day of selected month
        date_to = datetime.datetime.strptime(date_to_input, date_format) + relativedelta(day=31)

    elif request.method == 'GET':
        # Get end of last month as to_date
        date_to = datetime.datetime.now().replace(day=1) - datetime.timedelta(days=1)

        # Get 6 months before as to_date
        date_from = date_to + relativedelta(months=-5)
        date_from = date_from.replace(day=1)

    instances = Instance.objects.all().order_by('institute__name')

    all_active_users = ActivityReportEntry.objects.all().filter(
        activity_report__reportmonth__range=[date_from, date_to]).values('activity_report__instance',
                                                                         'user_id').annotate(
        activity_count=Sum('activity_count'))

    all_registered_users_count = None
    # all_registered_users_count = ActivityReport.objects.values('')annotate(max_date = Max('reportmonth')).filter(reportmonth = F('max_date')).aggregate(Sum('registered_users'))

    return render(
        request,
        template_name='instance_overview.html',
        context={'instances': instances, "date_from": date_from, "date_to": date_to,
                 "all_active_users": all_active_users, "all_registered_users_count": all_registered_users_count}
    )


def view_instance(request, instance_id):
    if request.method == 'GET':
        instance = get_object_or_404(Instance, pk=instance_id);

        return render(
            request, "instance.html", {"instance": instance}
        )


@login_required
def add_report(request):
    if request.method == 'POST':
        logger.debug("POST request in add_report")
        report = request.POST.get('report')
        return_report = ""
        try:
            controller.readAndSaveReport(report)
            messages.add_message(request, messages.SUCCESS, "Report successfully created")
        except IntegrityError:
            messages.add_message(request, messages.WARNING, "A report for the given instance and month already exists")
            return_report = report
        except Instance.DoesNotExist:
            messages.add_message(request, messages.WARNING,
                                 "The given labfolder instance does not exist yet. Please go to the Admin Area and add it or change the name of an existing instance")
            return_report = report
        except Exception as e:
            logger.exception("Exception occured while saving and parsing report")
            messages.add_message(request, messages.ERROR, e)
            return_report = report

        return render(request, template_name="add_report.html", context={"return_report": return_report})

    if request.method == 'GET':
        return render(request, template_name='add_report.html')

@login_required
def add_reports_batch(request):

    if request.method == 'POST':
        logger.debug("POST request in add_reports_batch")
        reports = request.POST.get('report')
        return_report = ""

        resultlist = controller.batch_import_from_outlook(reports)

        if(len(resultlist)>0):
            messages.add_message(request, messages.SUCCESS, "Found " + str(len(resultlist)) + " reports")
        else:
            messages.add_message(request, messages.ERROR, "No reports found!")


        for error in resultlist:
            if error[1] is not None:
                try:
                    raise(error[1])
                except IntegrityError:
                    messages.add_message(request, messages.WARNING, error[0] + " - A report for the given instance and month already exists")
                    return_report = reports
                except Instance.DoesNotExist:
                    messages.add_message(request, messages.ERROR,
                                         error[0] + " - The given labfolder instance does not exist yet. Please go to the Admin Area and add it or change the name of an existing instance")
                    return_report = reports
                except Exception as e:
                    logger.exception("Exception occured while saving and parsing report")
                    messages.add_message(request, messages.ERROR, error[0] + " - Error while parsing")
                    return_report = reports
            else:
                 messages.add_message(request, messages.SUCCESS, error[0] + " - successfully added")

        return render(request, template_name="add_reports_batch.html", context={"return_report": return_report})

    if request.method == 'GET':
        return render(request, template_name='add_reports_batch.html')
