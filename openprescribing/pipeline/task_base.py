from operator import attrgetter

import networkx as nx

from ordered_digraph import OrderedDiGraph


class TaskDefinition(object):
    @classmethod
    def ordered_task_definitions(cls, module=None):
        if module is None:
            import importlib
            module = importlib.import_module('task_definitions')

        graph = OrderedDiGraph()

        for task_definition in cls.task_definitions(module):
            graph.add_node(task_definition)
            if hasattr(task_definition, 'dependencies'):
                for dependency in task_definition.dependencies:
                    graph.add_edge(dependency, task_definition)

        for task in nx.topological_sort(graph):
            yield task

    @classmethod
    def task_definitions(cls, module):
        for v in vars(module).values():
            if isinstance(v, type) and v != cls and issubclass(v, cls):
                yield v
