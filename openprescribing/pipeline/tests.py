import json
import os

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from .import_log import imported_file_records, set_last_imported_filename
from .models import Source


class LoadSourceMetadataTests(TestCase):
    def test_source_added(self):
        '''Test loading metadata when source is added'''
        call_command('loadsourcemetadata', self._source_path(0))
        call_command('loadsourcemetadata', self._source_path(1))
        self.assertEqual(Source.objects.count(), 3)
        source = Source.objects.get(id='source-c')
        self.assertEqual(source.title, 'Source C')

    def test_source_changed(self):
        '''Test loading metadata when source has changed'''
        call_command('loadsourcemetadata', self._source_path(0))
        call_command('loadsourcemetadata', self._source_path(2))
        self.assertEqual(Source.objects.count(), 2)
        source = Source.objects.get(id='source-b')
        self.assertEqual(source.title, 'Sauce B')

    def test_no_changes(self):
        '''Test loading metadata with no changes'''
        call_command('loadsourcemetadata', self._source_path(0))
        call_command('loadsourcemetadata', self._source_path(0))
        self.assertEqual(Source.objects.count(), 2)

    def test_with_real_data(self):
        '''Test that real data in sources.json can be loaded'''
        call_command('loadsourcemetadata')

        source = Source.objects.get(id='bnf_codes')
        self.assertEqual(source.title, 'Human readable terms for BNF prescription codes')

    def _source_path(self, ix):
        return os.path.join(settings.SITE_ROOT, 'pipeline', 'test-data', 'sources-{}.json'.format(ix))


class ImportLogTests(TestCase):
    def setUp(self):
        log_data = {
            'dummy_source': [
                {
                    'imported_file': '/home/hello/openprescribing-data/data/dummy_source/2017_01/dummy_data_1701.csv',
                    'imported_at': '2017-01-01T12:00:00'
                },
                {
                    'imported_file': '/home/hello/openprescribing-data/data/dummy_source/2017_02/dummy_data_1702.csv',
                    'imported_at': '2017-02-01T12:00:00'
                }
            ]
        }

        with open(settings.IMPORT_LOG_PATH, 'w') as f:
            json.dump(log_data, f)

    def test_imported_file_records(self):
        imported = imported_file_records('dummy_source', 'dummy_data_\d+\.csv')
        self.assertEqual(2, len(imported))

    def test_imported_file_records_with_pattern_with_nothing_matching(self):
        imported = imported_file_records('dummy_source', 'dummy_data\.csv')
        self.assertEqual(0, len(imported))

    def test_imported_file_records_for_new_source(self):
        imported = imported_file_records('new_source', 'dummy_data_\d+\.csv')
        self.assertEqual(0, len(imported))

    def test_set_last_imported_filename(self):
        set_last_imported_filename('dummy_source', '/home/hello/openprescribing-data/data/dummy_source/2017_03/dummy_data_1703.csv')
        imported = imported_file_records('dummy_source', 'dummy_data_\d+\.csv')
        self.assertEqual(3, len(imported))

    def test_set_last_imported_filename_for_new_source(self):
        set_last_imported_filename('new_source', '/home/hello/openprescribing-data/data/new_source/2017_03/dummy_data_1703.csv')
        new_imported = imported_file_records('new_source', 'dummy_data_\d+\.csv')
        dummy_imported = imported_file_records('dummy_source', 'dummy_data_\d+\.csv')
        self.assertEqual(1, len(new_imported))
        self.assertEqual(2, len(dummy_imported))
