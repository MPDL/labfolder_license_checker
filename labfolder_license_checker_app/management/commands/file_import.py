import argparse

from django.core.management import BaseCommand
from django.db import IntegrityError

from labfolder_license_checker_app.controller import readAndSaveReport, batch_import_from_outlook
from django.conf import settings
import logging

from labfolder_license_checker_app.models import Instance

logger = logging.getLogger(__name__)
instance_not_exist_logger = logging.getLogger('InstanceNotExistLogger')
fh = logging.FileHandler(settings.BASE_DIR + '/instances.txt')
instance_not_exist_logger.addHandler(fh)
instance_not_exist_logger.setLevel(logging.INFO)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('path')

    def handle(self, path, *args, **options):
        import_from_file(path)


def import_from_file(path: str):
    with open(path, 'r') as content:
        batch_import_from_outlook(content.read())


