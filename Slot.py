from enum import Enum
class AdjRule(Enum):
    NONE = 0
    REDUCE = 1
    INF_REDUCE = 2
    EXPAND = 3
    INF_EXPAND = 4

class Slot:
    def __init__(self, name, sem_type, docstring="", pos_adj=AdjRule.REDUCE, neg_adj=AdjRule.EXPAND, min=1, max=None, path=None):
        self.name = name
        self.docstring = docstring
        self.sem_type = sem_type # Semantic type
        self.pos_adj = pos_adj # Positive adjustment
        self.neg_adj = neg_adj # Negative adjustment
        self.min = min
        self.max = max
        self.path = path

    def __repr__(self):
        return "<Slot {} id: {}>".format(self.name, hex(id(self)))

    def __str__(self):
        ret = "<{}>: {}\n".format(self.name, self.docstring)
        ret += "\tSemantic Type: {}".format(self.sem_type)
        ret += "\tPositive Adjust: {}".format(self.pos_adj)
        ret += "\tNegative Adjust: {}".format(self.neg_adj)
        ret += "\tMinimum Fillers: {}".format(self.min)
        ret += "\tMaximum Fillers: {}".format(self.max)
        ret += "\tPath: {}".format(self.path)
        return ret