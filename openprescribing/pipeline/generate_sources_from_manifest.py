from __future__ import print_function

from collections import OrderedDict
import json
import shlex

with open('manifest.json') as f:
    raw_sources = json.load(f)

sources = []

keys = [
    'id',
    'title',
    'description',
    'publisher',
    'publication_schedule',
    'publication_lag',
    'index_url',
    'urls',
    'notes',
    'requires_captcha',
    'licence',
    'licence_attributions',
]

non_source_keys = [
    'fetcher',
    'depends_on',
    'always_import',
    'importers',
    'before_import',
    'after_import',
    'filename_pattern',
    'tags',
]

filename_flags = [
    'filename',
    'ccg',
    'epraccur',
    'chem_file',
    'hscic_address',
    'month_from_prescribing_filename',
]


for raw_source in raw_sources:
    if not raw_source.get('publisher'):
        print('No publisher for {}'.format(raw_source['id']))
        continue
    for k in raw_source.keys():
        if k not in keys and k not in non_source_keys:
            print('Unexpected key {} for {}'.format(k, raw_source['id']))

    source = OrderedDict([[k, raw_source[k]] for k in keys if raw_source.get(k)])

    if 'core_data' in raw_source['tags']:
        source['core_data'] = True
    if 'research' in raw_source['tags']:
        source['research'] = True

    if 'research' not in raw_source['tags']:
        source['file_patterns'] = []
        for importer_cmd in raw_source.get('importers', []):
            cmd_parts = shlex.split(importer_cmd.encode('unicode-escape'))
            filename_idx = None
            for flag in filename_flags:
                try:
                    filename_idx = cmd_parts.index("--%s" % flag) + 1
                except ValueError:
                    pass
            assert filename_idx is not None
            source['file_patterns'].append(cmd_parts[filename_idx])

    sources.append(source)

sources.sort(key=lambda source: source['id'])

with open('data/sources.json', 'w') as f:
    json.dump(sources, f, indent=4)
