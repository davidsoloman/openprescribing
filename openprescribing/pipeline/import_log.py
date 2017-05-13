from collections import defaultdict
import datetime
import json
import re

from django.conf import settings


def imported_file_records(source_id, file_pattern):
    """Return a list of import records for all imported data for this
    source, whose path matches file_pattern.
    """
    records = _load_records()

    records_for_source = records[source_id]
    matched_records = filter(
        lambda record: re.findall(file_pattern, record['imported_file']),
        records_for_source)
    return sorted(
        matched_records,
        key=lambda record: record['imported_at'])


def set_last_imported_filename(source_id, filename):
    """Set the path of the most recently imported data for this source.
    """
    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    records = _load_records()
    records[source_id].append({
        'imported_file': filename,
        'imported_at': now,
    })
    _dump_records(records)


def _load_records():
    with open(settings.IMPORT_LOG_PATH) as f:
        log_data = json.load(f)
    return defaultdict(list, log_data)


def _dump_records(records):
    with open(settings.IMPORT_LOG_PATH, 'w') as f:
        json.dump(records, f, indent=2, separators=(',', ': '))
