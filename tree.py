import re
class Node:
    def __init__(self, identifier, vector):
        self.__identifier = identifier
        self.__vector = vector
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    @property
    def vector(self):
        return  self.__vector

    def add_child(self, child):
        self.__children.append(child)


(_ROOT, _DEPTH, _BREADTH) = range(3)


class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def get_nodes(self, regex):
        ret = []
        for node in self.__nodes:
            match = re.match(regex, node)
            if match:
                ret.append(self.__nodes[node])
        return ret

    def add_node(self, node, parent=None):
        try:
            dummy = self[node.identifier]
        except KeyError:
            self[node.identifier] = node
            if parent is not None:
                self[parent.identifier].add_child(node)
        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett,
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item