from task_base import AutoFetcher, ManualFetcher, TaskDefinition


class FetchBnfCodes(ManualFetcher):
    source_id = 'bnf_codes'


class FetchAdqs(ManualFetcher):
    source_id = 'adqs'


class FetchCcgBoundaries(ManualFetcher):
    source_id = 'ccg_boundaries'


class FetchPatientListWeightings(ManualFetcher):
    source_id = 'patient_list_weightings'


class FetchPatientListSize(AutoFetcher):
    source_id = 'patient_list_size'
    fetch_command = 'hscic_list_sizes'


class FetchCcgDetails(AutoFetcher):
    source_id = 'ccg_details'
    fetch_command = 'org_codes'
    fetch_command_args = ['--ccg']


class FetchPracticeDetails(AutoFetcher):
    source_id = 'practice_details'
    fetch_command = 'org_codes'
    fetch_command_args = ['--practice']


class ImportBnfCodes(TaskDefinition):
    task_type = 'importer'
    source_id = 'bnf_codes'
    dependencies = [
        FetchBnfCodes,
    ]

    def run(self):
        '''import_bnf_codes --filename bnf_codes.csv'''


class ImportCcgBoundaries(TaskDefinition):
    task_type = 'importer'
    source_id = 'ccg_boundaries'
    dependencies = [
        FetchCcgBoundaries,
    ]

    def run(self):
        '''import_ccg_boundaries --filename ccg_boundaries.*\.kml'''


class ImportCcgDetails(TaskDefinition):
    task_type = 'importer'
    source_id = 'ccg_details'
    dependencies = [
        FetchCcgDetails,
        ImportCcgBoundaries,
    ]

    def run(self):
        '''import_org_names --ccg eccg.csv'''


class FetchPrescribingMetadata(AutoFetcher):
    source_id = 'prescribing_metadata'
    fetch_command = 'hscic_prescribing'
    fetch_command_args = ['--most_recent_date']


class FetchPrescribing(ManualFetcher):
    source_id = 'prescribing'


class ImportAdqs(TaskDefinition):
    task_type = 'importer'
    source_id = 'adqs'
    dependencies = [
        FetchAdqs,
        ImportBnfCodes,
    ]

    def run(self):
        '''import_adqs --filename adqs_.*csv'''


class ImportPatientListWeightings(TaskDefinition):
    task_type = 'importer'
    source_id = 'patient_list_weightings'
    dependencies = [
        FetchPatientListWeightings,
    ]

    def run(self):
        '''calculate_star_pu_weights --filename prescribing_units.xlsx'''


class ImportPracticeDetails(TaskDefinition):
    task_type = 'importer'
    source_id = 'practice_details'
    dependencies = [
        FetchPracticeDetails,
        ImportCcgDetails,
    ]

    def run(self):
        '''import_practices --epraccur epraccur.csv'''


class FetchNhsPostcodeFile(AutoFetcher):
    source_id = 'nhs_postcode_file'
    fetch_command = 'org_codes'
    fetch_command_args = ['--postcode']


class ImportNhsPostcodeFile(TaskDefinition):
    task_type = 'importer'
    source_id = 'nhs_postcode_file'
    dependencies = [
        FetchNhsPostcodeFile,
        ImportPracticeDetails,
    ]

    def run(self):
        '''geocode_practices --filename gridall\.csv'''


class ImportHscicChemicals(TaskDefinition):
    task_type = 'importer'
    source_id = 'prescribing_metadata'
    dependencies = [
        FetchPrescribingMetadata,
    ]

    def run(self):
        '''import_hscic_chemicals --chem_file T\d+CHEM.*\.CSV'''


class ImportHscicPractices(TaskDefinition):
    task_type = 'importer'
    source_id = 'prescribing_metadata'
    dependencies = [
        FetchPrescribingMetadata,
        ImportCcgDetails,
        ImportPracticeDetails,
    ]

    def run(self):
        '''import_practices --hscic_address T\d+ADDR.*\.CSV'''


class ConvertHscicPrescriptions(TaskDefinition):
    task_type = 'other'
    source_id = 'prescribing'
    dependencies = [
        FetchPrescribing,
    ]

    def run(self):
        '''convert_hscic_prescribing --filename .*Detailed_Prescribing_Information.csv'''


class ImportPrescriptions(TaskDefinition):
    task_type = 'importer'
    source_id = 'prescribing'
    dependencies = [
        ImportHscicPractices,
        ConvertHscicPrescriptions,
        ImportBnfCodes,
        ImportCcgDetails,
        ImportPracticeDetails,
    ]

    def run(self):
        '''import_hscic_prescribing --filename .*Detailed_Prescribing_Information_formatted.CSV'''


class ImportDispensingPractices(TaskDefinition):
    task_type = 'importer'
    source_id = 'dispensing_practices'
    dependencies = [
        ImportHscicPractices,
        ImportPracticeDetails,
    ]

    def run(self):
        '''import_practice_dispensing_status --filename dispensing_practices.*\.csv'''


class ImportPatientListSize(TaskDefinition):
    task_type = 'importer'
    source_id = 'patient_list_size'
    dependencies = [
        FetchPatientListSize,
        ImportHscicPractices,
        ImportPracticeDetails,
        ImportPatientListWeightings,
    ]

    def run(self):
        '''import_list_sizes --filename patient_list_size_new.csv'''


class UploadToBigquery(TaskDefinition):
    task_type = 'other'
    dependencies = [
        ImportPatientListSize,
        ImportHscicPractices,
        ImportPrescriptions,  # Not sure whether this is a dependency
        ImportCcgDetails,
        ImportPracticeDetails,
    ]

    def run(self):
        '''runner:bigquery_upload'''


class ImportMeasureDefinitions(TaskDefinition):
    task_type = 'other'
    dependencies = [
        # Since this reads from data in measure_definitions directory,
        # presumably we should re-run this when that data is updated.  However,
        # there is no fetcher for this data.
    ]

    def run(self):
        '''import_measures --definitions_only'''


class ImportMeasures(TaskDefinition):
    task_type = 'other'
    dependencies = [
        UploadToBigquery,
        ImportMeasureDefinitions,
    ]

    def run(self):
        '''import_measures'''


class RefreshViews(TaskDefinition):
    task_type = 'other'
    dependencies = [
        UploadToBigquery,
    ]

    def run(self):
        '''create_views'''
