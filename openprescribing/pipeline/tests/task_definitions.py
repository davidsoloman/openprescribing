from pipeline.task_base import AutoFetcher, Converter, Importer, ManualFetcher, PostProcessor


class FetchSourceA(ManualFetcher):
    source_id = 'source_a'


class FetchSourceB(AutoFetcher):
    source_id = 'source_b'
    command = 'fetch_source_b'


class FetchSourceC(AutoFetcher):
    source_id = 'source_c'
    command = 'fetch_source_c'
    command_args = ['--flag']


class ConvertSourceA(Converter):
    source_id = 'source_a'
    dependencies = [
        FetchSourceA,
    ]
    command = 'convert_source_a'
    command_args = ['--filename', 'source_a.csv']


class ImportSourceA(Importer):
    source_id = 'source_a'
    dependencies = [
        ConvertSourceA,
    ]
    command = 'import_source_a'
    command_args = ['--filename', 'source_a_formatted.csv']


class ImportSourceB(Importer):
    source_id = 'source_b'
    dependencies = [
        FetchSourceB,
        ImportSourceA,
    ]
    command = 'import_source_b'
    command_args = ['--filename', 'source_b_.*.csv']


class ImportSourceC1(Importer):
    source_id = 'source_c'
    dependencies = [
        FetchSourceC,
        ImportSourceA,
        ImportSourceB,
    ]
    command = 'import_source_c'
    command_args = ['--flag', '1', '--filename', 'source_c.csv']


class ImportSourceC2(Importer):
    source_id = 'source_c'
    dependencies = [
        FetchSourceC,
    ]
    command = 'import_source_c'
    command_args = ['--flag', '2', '--filename', 'source_c.csv']


class PostProcess(PostProcessor):
    dependencies = [
        ImportSourceA,
        ImportSourceB,
        ImportSourceC1,
    ]
    command = 'post_process'
