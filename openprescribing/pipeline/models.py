from __future__ import print_function
from __future__ import unicode_literals

import textwrap

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.postgres.fields import ArrayField, HStoreField

import import_log


@python_2_unicode_compatible
class Source(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    publisher = models.CharField(max_length=40)
    publication_schedule = models.CharField(max_length=40, null=True)
    publication_lag = models.CharField(max_length=40, null=True)
    notes = models.TextField(null=True)
    index_url = models.CharField(max_length=200)
    urls = HStoreField(null=True)
    requires_captcha = models.BooleanField(default=False)
    licence = models.CharField(max_length=40, null=True)
    licence_attributions = ArrayField(models.CharField(max_length=200), null=True)
    core_data = models.BooleanField(default=False)
    research = models.BooleanField(default=False)
    file_patterns = ArrayField(models.CharField(max_length=200), default=[])

    def __str__(self):
        return self.id

    def prompt_for_manual_download(self, year_and_month):
        expected_location = os.path.join(self.data_dir(), year_and_month)

        print('~' * 80)
        print('You should now locate latest data for %s, if available' % self.id)
        print('You should save it at:')
        print('    %s' % expected_location)
        if self.index_url:
            print('Where to look:')
            print('   %s' % self.index_url)
        if self.urls:
            print('Previous data has been found at at:')
            for k, v in self.urls.items():
                print('    %s: %s' % (k, v))
        if self.publication_schedule:
            print('Publication frequency:')
            print('    %s' % self.publication_schedule)
        if self.notes:
            print('Notes:')
            for line in textwrap.wrap(self.notes):
                print('    %s' % line)
        print('The last imported data can be found at:')
        for file_pattern in self.file_patterns:
            imported_file_records = import_log.imported_file_records(self.id, file_pattern)
            if imported_file_records:
                print('    %s' % imported_file_records[-1]['imported_file'])
            else:
                print('    [never imported]')
        raw_input('Press return when done, or to skip this step')

    def fetched_paths(self, file_pattern):
        '''Returns list of paths to fetched files for source'''
        paths = glob.glob("%s/*/*" % self.data_dir())

        candidates = filter(
            lambda x: re.findall(file_pattern, x),
            files)
        return sorted(candidates)

    def data_dir(self):
        return os.path.join(settings.DATA_BASEDIR, self.id)
