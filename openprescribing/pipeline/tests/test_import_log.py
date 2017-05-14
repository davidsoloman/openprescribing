import json

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase

from pipeline.import_log import imported_file_records, set_last_imported_filename


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
