import networkx as nx

from models import Source
from ordered_digraph import OrderedDiGraph


class TaskDefinitionMetaclass(type):
    def __new__(mcs, name, bases, attrs):
        if 'source_id' in attrs:
            try:
                attrs['source'] = Source.objects.get(id=attrs['source_id'])
            except Source.DoesNotExist:
                raise RuntimeError('Task {} has source_id {} but no such source was found'.format(name, attrs['source_id']))
        return type.__new__(mcs, name, bases, attrs)


class TaskDefinition(object):
    __metaclass__ = TaskDefinitionMetaclass

    @classmethod
    def ordered_task_definitions(cls, module=None):
        if module is None:
            import importlib
            module = importlib.import_module('pipeline.task_definitions')

        graph = OrderedDiGraph()

        for task_definition in cls.task_definitions(module):
            graph.add_node(task_definition)
            if hasattr(task_definition, 'dependencies'):
                for dependency in task_definition.dependencies:
                    graph.add_edge(dependency, task_definition)

        for task in nx.topological_sort(graph):
            yield task

    @classmethod
    def task_definitions(cls, module=None):
        if module is None:
            import importlib
            module = importlib.import_module('pipeline.task_definitions')

        for v in vars(module).values():
            if isinstance(v, type) and v != cls and issubclass(v, cls):
                yield v
