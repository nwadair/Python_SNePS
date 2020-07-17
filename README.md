# Python_SNePS
> SNePS 3 in Python

This repository contains a partial implementation of the SNePS 3 semantic network in Python. A few test files have been included to demonstrate the system's current capabilities.

#### Implemented:
* SNePS module for building a network

#### Not implemented:
* Some tokens in well-formed-terms (See section 5)
* Uniqueness on variables in ‘donkey sentences’ (See section 1, resource 1)
* Inference package
* Belief revision

We would recommend any persons continuing with this project implement the missing features in the order in which they are listed.

## Section 1: Preliminary Reading

1. [“A Logic of Arbitrary and Indefinite Objects”](https://www.aaai.org/Papers/KR/2004/KR04-059.pdf) by Stuart Shapiro
    * This paper outlines the ideas behind the logical language implemented in SNePS 3. We have revised SNePS's grammar to be more Python-like in syntax, but the general concepts from this paper are very important.

2. [“An Introduction to SNePS 3”](https://cse.buffalo.edu/~shapiro/Papers/sneps3intro.pdf) by Stuart Shapiro
    * This paper explains the different semantic and syntactic types, the function of caseframes, frames, and slots (relations), and the different inference methods.

3. [“Visually Interacting with a Knowledge Base Using Frames, Logic, and Propositional Graphs”](https://cse.buffalo.edu/~shapiro/Papers/schsha2011b.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * This paper gives great working definitions for the various terms used in SNePS 3.

4. [“SNePS 3 User&rsquo;s Manual”](https://cse.buffalo.edu/sneps/Projects/sneps3manual.pdf) by Stuart Shapiro
    * Reference this manual to understand the user commands. The pseudo-yacc rules are defunct in Python_SNePS, but redefined below in Section 5 of the README.

5. [“Types in SNePS 3”](https://cse.buffalo.edu/~shapiro/Talks/TypesInSneps3.pdf) by Stuart Shapiro
    * This paper clearly explains the relationship between caseframes and slots. Note that slots are called “relations” in the paper.

6. [“Concurrent Reasoning in Inference Graphs”](https://cse.buffalo.edu/~shapiro/Papers/schsha13e.pdf) by Daniel R. Schlegel and Stuart C. Shapiro
    * Explains much of the induction work done in the SNIP package (Note that this is not all complete in CSNePS).

7. [“SUNY at Buffalo CSE563 Lecture Notes”](https://cse.buffalo.edu/~shapiro/Courses/CSE563/Slides/krrSlides.pdf) by Stuart C. Shapiro
    * Lecture notes from Stuart C. Shapiro’s course on knowledge representation. A long read, but explains many of the logical concepts at play beneath SNePS (e.g. andor, thresh, relations). The most thorough tutorial available.

## Section 2: Structure

### 1: Nodes

A node is a unique syntactic object, consisting of the following:
1. Name
2. Semantic Type
3. Up Cableset (An array of frames)

and sometimes:

4. Frame
5. Min
6. Max
7. Bound

Nodes are typecast to syntactic types, which theoretically correspond to the functions performed by certain grammatical structures (e.g. If x then y), and are, in our system, represented by classes.

![Syntactic Types](/assets/syntactic.svg)

### 2: Frames

A frame is a unique object, consisting of the following tuple:
1. Caseframe
2. Filler Set (An ordered list of Fillers)

Each Fillers instance must correspond to a slot in the caseframe (i.e. their semantic types must be compatible with the slot and their number must fall within the range set by the slot's min and max).

Each molecular node has a *single* frame.

### 3: Fillers

A filler is a non-unique object that contains an array of nodes. Fillers are used by frames to fill slots.

### 4. Caseframes

A caseframe is a unique object, consisting of the following:
1. Name
2. Semantic Type
3. Semantic Hierarchy (Of the parent network)
4. Docstring
5. Slots (An ordered list of slots)
6. Aliases (An array of strings also referring to this frame)

Caseframes, like *Isa*, form Molecular nodes and tell the system something about the nodes which are used (via Frames) to fill their slots.

(In the case of *Isa*, fillers in the first slot must be of type Entity (or a subtype) and are designated as *member*, and fillers in the second slot must be of type *Category* (or a subtype) and are designated as *class*)

### 5: Slots

Slots are “relations.” A slot is a unique object, consisting of the following:
1. Name
2. Docstring
3. Semantic Type
4. Positive adjustment rule (expand, reduce, or none)
5. Negative adjustment rules (expand, reduce, or none)
6. Minimum number of fillers
7. Maximum number of fillers
8. Path

### 6: Semantic Types

Semantic types tell a user the type of ontological entity a node represents (e.g. agent, action).

Because certain slots require certain types of entities, semantic types ensure ontological consistency. For example, a person can perform an action, but a person cannot perform an agent.

![Semantic Types](/assets/semantic.svg)

### 7: Paths

Paths, defined on slots, are items of the class Path. Some paths perform functions on child paths, and others perform functions on multiple children. The user should enter paths into functions as strings using the following syntax:

* ∅ is used to indicate that there should be no space between two tokens  
* \+ is used to indicate that there can be one or more of a given token  
* \* is used to indicate that there can be zero or more of a given token

```yacc
path :       slotname                             // e.g. "member"
     |       slotname ∅ '-'                       // Follows slot backward e.g. "member-"
     |       '!'                                  // Node at this point in interpretation
                                                      // must be asserted in the context
     |       'converse' '(' path ')'              // Follows a given path backward
     |       'kplus' '(' path ')'                 // Follows a path one or more times
     |       'kstar' '(' path ')'                 // Follows a path zero or more times
     |       composed
     |       'or' '(' paths ')'                   // Follows all of the paths and returns the
                                                      // set of nodes that at least one of them reaches
     |       'and' '(' paths ')'                  // Follows all of the paths and returns the
                                                      // set of nodes that every one of them reaches
     |       'irreflexive-restrict' '(' path ')'  // Follows the path such that it doesn't wind up
                                                      // where it began

paths :      'path'
      |      'path' ',' 'paths'

composed :   'composed' '(' paths ')'             // Follows each path followed by the next
         |   '[' paths ']'
```

## Section 3: Using Python_SNePS's Functions

Create a network object:

```python
from src import *
net = Network()
```

The following methods are defined:

```python
# Defines a term with a name and optional semantic type.
# The default semantic type is Entity.
net.define_term("Ben", sem_type_name="Agent")

# Prints all terms
net.list_terms()

# Returns the term we just defined.
net.find_term("Ben")

# Defines a semantic type, with a given name, followed by an
# optional array of parent types
net.define_type("Action", ["Thing"])

# Prints all types
net.list_types()

# Defines a slot corresponding to a type
# Name, followed by semantic type, with optional
# docstring, adjustment rules, min, max, and path
net.define_slot("class", "Category",
                docstring="Points to a Category that some Entity is a member of.",
                pos_adj="none", neg_adj="reduce", min=1, max=0, path='')

# Returns the Slot object we just defined.
net.find_slot("class")

# Prints all slots
net.list_slots()

# Defines a new caseframe with a name, semantic type, list of slots,
# and optional docstring
net.define_caseframe("Isa", "Propositional", ["member", "class"],
                     docstring="Epistemic relationship for class membership")

# Prints all caseframes
net.list_caseframes()

# Finds a specific caseframe
net.find_caseframe("Isa")

# Adds two aliases, "AlsoIsa" and "IsAlsoa", to the "Isa" caseframe.
net.same_frame(["AlsoIsa", "IsAlsoa"], "Isa")

# Passes wft followed by optional parameter "inf" for
# triggering forward inference
net.assert_wft("Isa(Dog, Pet)", inf=False)

# Prints out a visual representation of the knowledge base
# This should probably be renamed to something else, since it's not
# printing anything to stdout, but making a matplotlib window.
net.print_graph()

# Outputs the network in the Graphviz DOT format to out.dot
net.export_graph(file_name="out.dot")

# Defines a new context, accessible through net.contexts["test"]
net.define_context("test")

# Sets the current context to the "test" context.
net.set_current_context("test")

# Prints out the contexts defined in the network.
net.list_contexts()

### NOT DONE ANNOTATING:
net.define_path()
net.paths_from()
```

## Section 4: Inference

We have implemented a portion of SNIP, the inference package for SNePS, in the snip directory of this repository.

To do inference, instantiate an object in the Instance class, and call its methods. These methods are documented below:

```python
from src import *
net = Network()
inf = Inference(net)
```

## Section 5: Using Python_SNePS's Well Formed Terms (wfts)

All wft parsing is handled through ply, a Python module that implements lex and yacc. The following yacc-like reduction rules should give an idea of how a wft is parsed.

* ∅ is used to indicate that there should be no space between two tokens  
* \+ is used to indicate that there can be one or more of a given token  
* \* is used to indicate that there can be zero or more of a given token

```yacc
wft :        atomicName                              // e.g. "Dog"
    |        'wft' ∅ i                               // e.g. "wft1"
    |        identifier '(' argument+ ')'            // A function (e.g. "Has(Dog, Bone)")
    |        BinaryOp '(' argument ',' argument ')'  // e.g. "if(Has(Dog, Bone), Happy(Dog))"
    |        NaryOp '(' wft* ')'                     // e.g. "and(a, b, c)"
    |        Param2Op '{' i ',' j '}' '(' wft+ ')'   // e.g. "thresh{1, 2}(a, b, c, d)"
    |        'thresh' '{' i '}' '(' wft+ ')'         // e.g. "thresh{1}(a, b, c)"
    |        'close' '(' atomicNameSet ',' wft ')'
    |        'every' '(' atomicName ',' argument ')'
    |        'some' '(' atomicName '(' atomicName ')' ',' argument ')'
    |        '?' ∅ atomicName '(' wft* ')'           // e.g. "?John"


BinaryOp :   i ∅ '=>' | 'v=>' | '=>' | 'if'          // 'v=>' does or-implication and
                                                     // "i ∅ '=>'" does and-implication (e.g. "5=>")

NaryOp :     'and' | 'or' | 'not' | 'nor'            // These operators, exclusively, can take
       |     'thnot' | 'thnor' | 'nand'              // any number of parameters
       |     'xor' | 'iff' | '<=>' | Equiv


Param2Op :   'andor' | 'thresh'


atomicName : identifier | i                          // Identifier matches r'[A-Za-z][A-Za-z0-9_]*'
                                                     // i (Integer) matches r'\d+'

argument :   wft
         |   'None'                                  // Equivalent to an empty set
         |   'setof' '(' wfts* ')'                   // Creates a set of filler nodes for a single slot
         |   '[' wfts* ']'                           // Equivalent to 'setof(wfts*)'

```

## Section 6: Imports

To display visual graphs, Pthon_SNePS requires extra Python modules. For simple graphs, run:
```bash
pip install networkx matplotlib
```

For draggable graphs, also run:
```bash
pip install netgraph
```

To export graphs as dot files, run:
```bash
pip install pydot
```

## Section 7: Older Versions of Python_SNePS

A previous version of Python_SNePS from the summer of 2019 can be found under the Releases tab on GitHub, and may be useful for reference.
