from task_definitions import ManualFetcher, TaskDefinition


def prompt_manual_data():
    for task_definition in ManualFetcher.ordered_task_definitions():
        task_definition().prompt_for_manual_download()
