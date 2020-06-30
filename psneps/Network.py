"""
This is the main file of the package. In here, we define the Network class.
Authors: Seamus Wiseman, John Madigan, Ben Kallus
"""

from .SemanticType import SemanticMixin
from .Context import ContextMixin
from .Slot import SlotMixin, AdjRule
from .Node import NodeMixin, Molecular, MinMaxOpNode
from .Caseframe import CaseframeMixin
from .wft.WftParse import wft_parser
from sys import stderr
from re import match
try:
    import networkx as nx
    has_nx = True
except ModuleNotFoundError:
    has_nx = False
try:
    import matplotlib.pyplot as plt
    has_mpl = True
except ModuleNotFoundError:
    has_mpl = False
try:
    import netgraph as ng
    has_ng = True
except ModuleNotFoundError:
    has_ng = False

class Network(SlotMixin, CaseframeMixin, SemanticMixin, NodeMixin, ContextMixin):
    def __init__(self) -> None:
        self.enforce_name_syntax = False
        for cls in type(self).__bases__:
            cls.__init__(self)

        # self.nodes = {} (defined in Node.py)
        # self.caseframes = {} (defined in Caseframe.py)
        # self.slots = {} (defined in Slot.py)
        # self.sem_hierarchy = SemanticHierarchy() (defined in SemanticType.py)
        # self.contexts = {} (defined in Context.py)
        # self.default_context = Context(docstring="The default context") (defined in Context.py,_default",
        # self.default_context = self.default_context
        self._build_default()

    def _build_default(self) -> None:
        """ Builds the default context """

        # Types
        # =====

        # Entities
        self.define_type("Act")
        self.define_type("Propositional")
        self.define_type("Thing")
        self.define_type("Policy")

        # Propositional
        self.define_type("Proposition", ["Propositional"])
        self.define_type("WhQuestion", ["Propositional"])

        # Things
        self.define_type("Category", ["Thing"])
        self.define_type("Action", ["Thing"])

        # Slots
        # =====

        # Propositions
        self.define_slot("class", "Category", docstring="Points to a Category that some Entity is a member of.",
                         neg_adj='reduce')
        self.define_slot("member", "Entity", docstring="Points to the Entity that is a member of some Category.",
                         neg_adj='reduce')
        self.define_slot("equiv", "Entity", docstring="All fillers are coreferential.",
                         neg_adj='reduce', min=2)
        self.define_slot("closedvar", "Entity", docstring="Points to a variable in a closure.")
        self.define_slot("proposition", "Propositional", docstring="Points to a proposition.")

        # Rules
        self.define_slot('and', 'Proposition', docstring='Fillers are arguments of a conjuction',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('or', 'Proposition', docstring='Fillers are arguments of a disjunction',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('nor', 'Proposition', docstring='Fillers are arguments of a nor',
                         pos_adj='reduce', neg_adj='expand', min=1)
        self.define_slot('andorargs', 'Proposition', docstring='Fillers are arguments of an andor',
                         pos_adj='none', neg_adj='none', min=2)
        self.define_slot('threshargs', 'Proposition', docstring='Fillers are arguments of a thresh',
                         pos_adj='none', neg_adj='none', min=2)
        self.define_slot('thnor', 'Proposition', docstring='Fillers are arguments of a thnor',
                         pos_adj='reduce', neg_adj='reduce', min=1)
        self.define_slot('ant', 'Proposition', docstring='antecedent for a set',
                         pos_adj='expand', neg_adj='reduce', min=1)
        self.define_slot('cq', 'Proposition', docstring='consequent for a set',
                         pos_adj='reduce', neg_adj='expand', min=1)

        self.define_slot('xor', 'Proposition', docstring='exclusive or',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('nand', 'Proposition', docstring='not and',
                         pos_adj='reduce', neg_adj='expand', min=2)
        self.define_slot('equivalence', 'Proposition', docstring='double implication',
                         pos_adj='reduce', neg_adj='expand', min=2)

        # SNeRE
        self.define_slot("action", "Action", docstring="The actions of an act.",
                         neg_adj='none', pos_adj='none', min=1, max=1)


        # Condition-Action Rules
        self.define_slot("condition", "Propositional", docstring="Conditions for a rule.",
            neg_adj='reduce', pos_adj='expand', min=1)
        self.define_slot("rulename", "Thing", docstring="The name of a rule.",
            neg_adj='none', pos_adj='none', min=1, max=1)
        self.define_slot("subrule", "Policy", docstring="Subrules for a rule.",
            neg_adj='reduce', pos_adj='expand', min=0)

        # Caseframes
        self.define_caseframe('Isa', 'Propositional', slot_names=["member", "class"],
                                docstring="[member] is a [class]")
        self.define_caseframe('Equiv', 'Propositional', slot_names=["equiv"],
                                docstring="[equiv] are all co-referential")
        self.define_caseframe('and', 'Propositional', slot_names=["and"],
                                docstring="it is the case that [and]")
        self.define_caseframe('or', 'Propositional', slot_names=["or"],
                                docstring="it is the case that [or]")
        self.define_caseframe('nor', 'Propositional', slot_names=["nor"],
                                docstring="it is not the case that [nor]")
        self.define_caseframe('thnor', 'Propositional', slot_names=["thnor"],
                                docstring="I don't know that it is the case that [thnor]")
        self.define_caseframe('andor', 'Propositional', slot_names=["andorargs"],
                                docstring="I don't know that it is the case that [thnor]")
        self.define_caseframe('thresh', 'Propositional', slot_names=["threshargs"],
                                docstring="I don't know that it is the case that [thnor]")
        self.define_caseframe('if', 'Propositional', slot_names=["ant", "cq"],
                                docstring="if [ant] then [cq]")
        self.define_caseframe('close', 'Propositional', slot_names=["proposition", "closedvar"],
                                docstring="[proposition] is closed over [closedvar]")
        self.define_caseframe('rule', 'Policy', slot_names=["rulename", "condition", "action", "subrule"],
                                docstring="for the rule [name] to fire, [condition] must be matched, then [action] may occur, and [subrule] may be matched.")

        self.define_caseframe('nand', 'Propositional', slot_names=['nand'],
                               docstring='it is the case that [nand]')
        self.define_caseframe('xor', 'Propositional', slot_names=['xor'],
                               docstring='it is the case that [xor]')
        self.define_caseframe('iff', 'Propositional', slot_names=['equivalence'],
                               docstring='it is the case that [doubimpl]')

        # Aliases
        self.caseframes["nor"].add_alias("not")
        self.caseframes["thnor"].add_alias("thnot")

        # Turn off enforcing name syntax
        # ==============================
        self.enforce_name_syntax = True


    def assert_wft(self, wft_str: str, hyp: bool = False) -> None:
        wft = wft_parser(wft_str, self)
        print("=> {}".format(wft.name), end='')
        if hyp:
            print('!')
            self.current_context.add_hypothesis(wft)
        else:
            print()

    def print_graph(self) -> None:
        if not has_nx:
            print("In order to use this function, you must pip install networkx")
        if not has_mpl:
            print("In order to use this function, you must pip install matplotlib")

        G = nx.DiGraph()
        edge_labels = {}
        for node in self.nodes.values():
            node_name = node.name
            if self.current_context.has_hypothesis(node_name):
                node_name += '!'
            G.add_node(node_name)
            if isinstance(node, Molecular):
                for i in range(len(node.frame.filler_set)):
                    fillers = node.frame.filler_set[i]
                    name = node.frame.caseframe.slots[i].name
                    if isinstance(node, MinMaxOpNode):
                        name += " ({}, {})".format(node.min, node.max)
                    if name == "nor" and len(fillers) == 1:
                        name = "not"
                    for filler in fillers.nodes:
                        G.add_edge(node_name, filler.name)
                        try:
                            edge_labels[(node_name, filler.name)] += ", " + name
                        except:
                            edge_labels[(node_name, filler.name)] = name

        pos = nx.circular_layout(G)
        if has_ng:
            # This is kind of a buggy module. You have to do _ = for some reason.
            _ = ng.InteractiveGraph(G, pos, node_size=10, node_label_font_size=12.0, node_color='grey', alpha=0.8,
                                    node_labels={node.name:node.name for node in self.nodes.values()},
                                    edge_labels=edge_labels, font_color='black')
        else:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
            nx.draw_networkx(G, pos, node_size=800, node_color='grey', alpha=0.8)
        plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        plt.show()
