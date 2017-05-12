from task_definitions import TaskDefinition


for task_definition in TaskDefinition.ordered_task_definitions():
    print task_definition.__name__
