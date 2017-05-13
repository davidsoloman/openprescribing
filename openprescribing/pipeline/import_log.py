import datetime
import json
import re

from django.conf import settings


def imported_file_records(source_id, file_pattern):
    """Return an list of import records for all imported data for this
    source, whose path matches file_pattern.
    """
    with open(settings.IMPORT_LOG_PATH, 'r') as f:
        log = json.load(f)

    import_records = log.get(source_id, [])
    matched_records = filter(
        lambda record: re.findall(file_pattern, record['imported_file']),
        import_records)
    return sorted(
        matched_records,
        key=lambda record: record['imported_at'])


def set_last_imported_filename(source_id, filename):
    """Set the path of the most recently imported data for this source
    """
    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    with open(settings.IMPORT_LOG_PATH, 'r+') as f:
        try:
            log = json.load(f)
        except ValueError:
            log = {}
        if not log.get(source_id, None):
            log[source_id] = []
        log[source_id].append(
            {'imported_file': filename,
             'imported_at': now})
        f.seek(0)
        f.write(json.dumps(log, indent=2, separators=(',', ': ')))

