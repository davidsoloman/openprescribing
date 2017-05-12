from collections import OrderedDict

import networkx as nx


class OrderedDiGraph(nx.DiGraph):
    node_dict_factory = OrderedDict
    adjlist_dict_factory = OrderedDict
