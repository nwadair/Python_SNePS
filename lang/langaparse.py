import langalex
from langAInterpreter import *

tokens = langalex.tokens
top = None

# =====================================
# -------------- RULES ----------------
# =====================================

# Wfts can be FWfts (function-eligible) or OWfts (other)
def p_Wft(p):
    '''
    Wft :               FWft
       |                OWft
    '''
    p[0] = p[1]
    global top
    top = p[0]

def p_FWft(p):
    '''
    FWft :              AtomicWft
         |              Y_WftNode
         |              Function
         |              Param1Op
    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[1])

def p_OWft(p):
    '''
    OWft :              BinaryOp
         |              NaryOp
         |              Param2Op
         |              CloseStmt
         |              EveryStmt
         |              SomeStmt
         |              QIdenStmt

    '''
    p[0] = ParseTree(description="wft")
    p[0].add_children(p[1])

def p_BinaryOp(p):
    '''
    BinaryOp :          Y_Impl LParen Argument Comma Argument RParen
             |          Y_OrImpl LParen Argument Comma Argument RParen
             |          Y_AndImpl LParen Argument Comma Argument RParen
    '''
    p[1].add_children(p[3], p[5])
    p[0] = p[1]

def p_NaryOp(p):
    '''
    NaryOp :            Y_And LParen Wfts RParen
           |            Y_Or LParen Wfts RParen
           |            Y_Not LParen Wfts RParen
           |            Y_Nor LParen Wfts RParen
           |            Y_Thnot LParen Wfts RParen
           |            Y_Thnor LParen Wfts RParen
           |            Y_Nand LParen Wfts RParen
           |            Y_Xor LParen Wfts RParen
           |            Y_DoubImpl LParen Wfts RParen
           |            Y_And LParen RParen
           |            Y_Or LParen RParen
           |            Y_Not LParen RParen
           |            Y_Nor LParen RParen
           |            Y_Thnot LParen RParen
           |            Y_Thnor LParen RParen
           |            Y_Nand LParen RParen
           |            Y_Xor LParen RParen
           |            Y_DoubImpl LParen RParen
    '''
    if len(p) == 5:
        p[1].add_children(*p[3])
    p[0] = p[1]

def p_Param2Op(p):
    '''
    Param2Op :          Y_AndOr LBrace Integer Comma Integer RBrace LParen Wfts RParen
             |          Y_Thresh LBrace Integer Comma Integer RBrace LParen Wfts RParen
    '''
    p[1].description = '<' + p[3] + '-' + p[5] + '>'
    p[1].add_children(*p[8])
    p[0] = p[1]

def p_Param1Op(p):
    '''
    Param1Op :          Y_Thresh LBrace Integer RBrace LParen Wfts RParen
    '''
    p[1].description = '<' + p[3] + '>'
    p[1].add_children(*p[7])
    p[0] = p[1]

def p_EveryStmt(p):
    '''
    EveryStmt :         Y_Every LBrace AtomicName RBrace LParen Wfts RParen
              |         Y_Every LBrace AtomicName RBrace LParen RParen
    '''
    p[1].add_children(p[3])
    if len(p) == 8:
        wftTree = ParseTree(description="wfts")
        wftTree.add_children(*p[6])
        p[1].add_children(wftTree)
    p[0] = p[1]

def p_SomeStmt(p):
    '''
    SomeStmt :          Y_Some LBrace AtomicName LParen AtomicName RParen RBrace LParen Wfts RParen
             |          Y_Some LBrace AtomicName LParen AtomicName RParen RBrace LParen RParen
    '''
    p[1].add_children(p[3], p[5])
    if len(p) == 11:
        wftTree = ParseTree(description="wfts")
        wftTree.add_children(*p[9])
        p[1].add_children(wftTree)
    p[0] = p[1]

def p_CloseStmt(p):
    '''
    CloseStmt :         Y_Close LParen AtomicNameSet Comma Wft RParen
    '''
    p[1].add_children(p[3], p[5])
    p[0] = p[1]

def p_AtomicWft(p):
    '''
    AtomicWft :         Y_Identifier
              |         Y_String
              |         Y_Integer
    '''
    p[0] = p[1]

def p_Function(p):
    '''
    Function :          FWft LParen Arguments RParen
    '''
    argsTree = ParseTree(description="args")
    argsTree.add_children(*p[3])
    p[0] = ParseTree(description="Function")
    p[0].add_children(p[1], argsTree)

def p_QIdenStmt(p):
    '''
    QIdenStmt :         Y_QIdentifier LParen Wfts RParen
              |         Y_QIdentifier LParen RParen
    '''
    if len(p) == 5:
        p[1].add_children(*p[3])
    p[0] = p[1]

def p_Argument(p):
    '''
    Argument :          Wft
             |          Y_None
             |          ArgumentFunction LParen Wfts RParen
             |          ArgumentFunction LParen RParen
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParseTree(description="Argument")
        p[0].add_children(p[1])
        if len(p) == 5:
            wftTree = ParseTree(description="wfts")
            wftTree.add_children(*p[3])
        p[0].add_children(wftTree)

def p_ArgumentFunction(p):
    '''
    ArgumentFunction :  Y_SetOf
    '''
    p[0] = p[1]

def p_Wfts(p):
    '''
    Wfts :              Wft
         |              Wfts Comma Wft
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_Arguments(p):
    '''
    Arguments :         Argument
              |         Arguments Comma Argument
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_AtomicNameSet(p):
    '''
    AtomicNameSet :     AtomicName
                  |     LParen AtomicNames RParen
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ParseTree(description="AtomicNameSet")
        p[0].add_children(*p[3])

def p_AtomicNames(p):
    '''
    AtomicNames :       AtomicName
                |       AtomicNames Comma AtomicName
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_AtomicName(p):
    '''
    AtomicName :        Y_Identifier
    '''
    p[0] = p[1]

# =====================================
# -------------- LEAVES ---------------
# =====================================

def p_Y_Impl(p):
    '''Y_Impl :         Impl'''
    p[0] = ParseTree(description="Implication", value=p[1])

def p_Y_Or(p):
    '''Y_Or :           Or'''
    p[0] = ParseTree(description="Or", value=p[1])

def p_Y_Integer(p):
    '''Y_Integer :      Integer'''
    p[0] = ParseTree(description="Integer", value=p[1])

def p_Y_String(p):
    '''Y_String :       String'''
    p[0] = ParseTree(description="String", value=p[1])

def p_Y_Not(p):
    '''Y_Not :          Not'''
    p[0] = ParseTree(description="Not", value=p[1])

def p_Y_Nor(p):
    '''Y_Nor :          Nor'''
    p[0] = ParseTree(description="Nor", value=p[1])

def p_Y_Thnot(p):
    '''Y_Thnot :        Thnot'''
    p[0] = ParseTree(description="Thnot", value=p[1])

def p_Y_Thnor(p):
    '''Y_Thnor :        Thnor'''
    p[0] = ParseTree(description="Thnor", value=p[1])

def p_Y_Nand(p):
    '''Y_Nand :         Nand'''
    p[0] = ParseTree(description="Nand", value=p[1])

def p_Y_Xor(p):
    '''Y_Xor :          Xor'''
    p[0] = ParseTree(description="Xor", value=p[1])

def p_Y_DoubImpl(p):
    '''Y_DoubImpl :     DoubImpl'''
    p[0] = ParseTree(description="DoubImpl", value=p[1])

def p_Y_AndOr(p):
    '''Y_AndOr :        AndOr'''
    p[0] = ParseTree(description="AndOr", value=p[1])

def p_Y_Thresh(p):
    '''Y_Thresh :       Thresh'''
    p[0] = ParseTree(description="Thresh", value=p[1])

def p_Y_SetOf(p):
    '''Y_SetOf :        SetOf'''
    p[0] = ParseTree(description="String", value=p[1])

def p_Y_Every(p):
    '''Y_Every :        Every'''
    p[0] = ParseTree(description="Every", value=p[1])

def p_Y_Some(p):
    '''Y_Some :         Some'''
    p[0] = ParseTree(description="Some", value=p[1])

def p_Y_Close(p):
    '''Y_Close :        Close'''
    p[0] = ParseTree(description="Close", value=p[1])

def p_Y_And(p):
    '''Y_And :          And'''
    p[0] = ParseTree(description="And", value=p[1])

def p_Y_WftNode(p):
    '''Y_WftNode :      WftNode'''
    p[0] = ParseTree(description="WftNode", value=p[1])

def p_Y_QIdentifier(p):
    '''Y_QIdentifier :  QIdentifier'''
    p[0] = ParseTree(description="QIdentifier", value=p[1])

def p_Y_Identifier(p):
    '''Y_Identifier :   Identifier'''
    p[0] = ParseTree(description="LEX", value=p[1])

def p_Y_None(p):
    '''Y_None :   None'''
    p[0] = ParseTree(description="None", value=p[1])

def p_Y_OrImpl(p):
    '''Y_OrImpl :   OrImpl'''
    p[0] = ParseTree(description="OrImpl", value=p[1])

def p_Y_AndImpl(p):
    '''Y_AndImpl :   AndImpl'''
    p[0] = ParseTree(description="AndImpl", value=p[1])

def p_error(p):
    raise Exception("Syntax error")

# =====================================
# ------------ RULES END --------------
# =====================================

if __name__ == '__main__':
    from ply import *
    yacc.yacc()
    while True:
        try:
            s = input('Command: ')
        except EOFError:
            break
        if str(s) == 'exit()':
            break
        yacc.parse(s)
        top.to_networkx()
