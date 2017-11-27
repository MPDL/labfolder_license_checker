import re
import datetime

from django.conf import settings

from .models import ActivityReport, ActivityReportEntry, Instance
from django.db import transaction, IntegrityError
import logging
logger = logging.getLogger(__name__)
instance_not_exist_logger = logging.getLogger('InstanceNotExistLogger')
fh = logging.FileHandler(settings.BASE_DIR + '/instances.txt')
instance_not_exist_logger.addHandler(fh)
instance_not_exist_logger.setLevel(logging.INFO)

@transaction.atomic
def readAndSaveReport(reportString):
    regex = ("labfolder report for (?P<instance_name>.*) for (?P<date>\d\d\.\d\d\d\d)(\n|\r|\r\n)"
             "(\n|\r|\r\n)"
             "Registered users: (?P<registered_users>\d*)(\n|\r|\r\n)"
             "Active users: (?P<active_users>\d*)(\n|\r|\r\n)"
             "(\n|\r|\r\n)"
             "User    Activity Count(\n|\r|\r\n)"
             "(\n|\r|\r\n)"
             "(?P<activity_table>[^z^-]*).*$")

    p = re.compile(regex, re.DOTALL)
    m = p.search(reportString)

    instance_name = m.group("instance_name");
    logger.debug("Parsed instance name: " + instance_name)
    report_month = datetime.datetime.strptime("01." + m.group("date"), "%d.%m.%Y")
    logger.debug("Parsed report month: " + str(report_month))
    registered_users = m.group("registered_users")
    logger.debug("Parsed registered users: " + registered_users)
    active_users = m.group("active_users")
    logger.debug("Parsed active users: " + active_users)
    activity_table = m.group("activity_table")
    logger.debug("Parsed activity table: " + activity_table)

    activity_report = ActivityReport()
    try:
        activity_report.instance = Instance.objects.get(name=instance_name)
    except Instance.DoesNotExist as e:
        e.instance_name = instance_name
        raise e
    activity_report.reportmonth = report_month;
    activity_report.registered_users = registered_users
    activity_report.save()

    for line in activity_table.splitlines():
        if line.strip():
            strippedLine = re.split("\s+", line.strip())

            entry = ActivityReportEntry()
            entry.activity_report = activity_report;
            entry.user_id = strippedLine[0]
            entry.activity_count = strippedLine[1]
            entry.save()

    return activity_report





def batch_import_from_outlook(content: str):
    current_report = ""
    current_subject = ""
    add_line = False
    errorlist = []
    for line in content.splitlines():
        line += "\n"
        if line.startswith("labfolder report for"):
            add_line = True

        elif line.startswith("Betreff:"):
            current_subject = line
        elif line.startswith("Von:"):
            add_line = False

            if current_report:
                batch_import_handle_single_report(current_subject, current_report, errorlist)

            current_report = ""

        if add_line:
            current_report += line

    if(current_report):
        batch_import_handle_single_report(current_subject, current_report, errorlist)

    return errorlist


def batch_import_handle_single_report(current_subject: str, current_report: str, errorlist):
    try:
        readAndSaveReport(current_report)
        errorlist.append((current_subject, None))
    except Instance.DoesNotExist as e:
        errorlist.append((current_subject, e))
        instance_not_exist_logger.info(e.instance_name)
    except IntegrityError as e:
        instance_not_exist_logger.info("Already exists: " + current_subject)
        errorlist.append((current_subject, e))
    except Exception as e:
        logger.exception("Problem while parsing report")
        instance_not_exist_logger.info("Problem with report: " + current_subject)
        errorlist.append((current_subject, e))