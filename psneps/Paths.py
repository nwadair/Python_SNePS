class Paths(Path):
    """ A composed list of paths, following one after another """
    def __init__(self, paths):
        self.paths = paths

    def derivable(self, start_node):
        for path in self.paths:
            pass

class AndPaths(Path):
    def __init__(self, paths):
        pass

class OrPaths(Path):
    def __init__(self, paths):
        pass

class KStarPath(Path):
    def __init__(self, paths):
        pass

class KPlusPath(Path):
    def __init__(self, paths):
        pass

class BasePath:
    """ Atomic path existing on a single non-repeated slot """
    def __init__(self, slot, self.backward=False, self.asserted=False):
        self.backward = backward

    followable(self, start_node, finish_node):
        pass


(member (kstar (equiv- ! equiv)))
