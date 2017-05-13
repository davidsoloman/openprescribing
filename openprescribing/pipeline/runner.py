from task_definitions import ManualFetcher, TaskDefinition


def prompt_manual_data():
    for task in ManualFetcher.tasks():
        task.prompt_for_manual_download()
