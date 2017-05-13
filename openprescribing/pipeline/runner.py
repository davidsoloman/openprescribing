from task_definitions import TaskDefinition


def prompt_manual_data():
    for task_definition in TaskDefinition.ordered_task_definitions():
        print task_definition.__name__
        print getattr(task_definition, 'source', None)
