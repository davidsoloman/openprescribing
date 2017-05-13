import datetime

from task_definitions import ManualFetcher, TaskDefinition


def prompt_manual_data():
    year_and_month = datetime.datetime.now().strftime('%Y_%m')
    for task in ManualFetcher.tasks():
        task.prompt_for_manual_download(year_and_month)
