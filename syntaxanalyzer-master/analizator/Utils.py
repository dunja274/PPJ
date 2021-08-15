import sys
from queue import LifoQueue

class Triplet:
    first = ""
    second = ""
    third = ""  
    
    def __init__(self, x, y, z):
        self.first = x
        self.second = y
        self.third = z

    def __str__(self):
        return f'{self.first} {self.second} {self.third}'

    def __repr__(self):
        return str(self)

class Util:
    @staticmethod
    def parse_anaylzer_input(input):
        for line in sys.stdin:
            splited = line.split(' ')
            third = ""
            for i in range(2, len(splited)):
                third += splited[i]
                third += " "
            third = third[:-1].strip()
            input.append(Triplet(splited[0], splited[1], third))
    
    @staticmethod
    def list_print(list):    
        for item in list:
            print(item)

class Tree:
    data = ''
    children = []

    def __init__(self, data):
        self.data = data
    
    def __str__(self):
        return f'{self.data}'

    def __repr__(self):
        return str(self)

    def add_child(self, child):
        self.children = child

    def print_tree(self):
        self.print(0)

    def print(self, num):       
        tmp = ' ' * num
        
        if self.data.first[0] == "<" or self.data.first == '$':
            tmp2 = self.data.first
        else:
            tmp2 = self.data

        print(f"{tmp}{tmp2}")
        children = self.children
        
        while len(children) > 0:   
            new_tmp = num     
            new = self.children.pop()
            new.print(new_tmp + 1)



class Parser:
    stack = []
    head = None
    lex_units = []
    actions = {}
    grammar = {}
    syn = []

    def __init__(self, lex_units, syn, actions, grammar):
        self.stack.append('0')
        self.lex_units = lex_units
        self.lex_units.append(Triplet("", "", ""))
        self.actions = actions
        self.grammar = grammar
        self.syn = syn

    def simulate(self):
        popped = ''
        while len(self.lex_units) > 0:
            peek_lex = self.lex_units[0]
            if(type(self.stack[-1]) == Tree):
                key = (self.stack[-2], self.stack[-1].data.first)
            else:
                key = (self.stack[-1], peek_lex.first)

            if key not in self.actions:  
                print(f'on row {peek_lex.second} read lex({peek_lex.first}) = {peek_lex.third}', file=sys.stderr)
                list_expected = []
                for action in self.actions:
                    if action[0] == key[0]:
                        list_expected.append(action[1])
                print(f'expected {list_expected}', file=sys.stderr) 
            
                while len(self.lex_units) > 1:
                    if self.lex_units[0].first in self.syn:
                        syn = self.lex_units[0].first
                        break
                    else:
                        self.lex_units.pop(0)
                while True:
                    stanje = self.stack[-1]
                    if len(self.stack) > 2:
                        stablo = self.stack[-2]    
                    key = (stanje, syn)
                    if key in self.actions:
                        break
                    else:
                        self.stack.pop()
                        self.stack.pop()

            action = self.actions[key]
            if action[0] == 'p':
                self.pomakni(action[1:])
            elif action[0] == 'r':
                self.reduciraj(action[1:])
            elif action == "Prihvati()":
                self.prihvati()
            else:
                self.novo_stanje(action)
        
        self.head.print_tree()

    def pomakni(self, state):
        self.stack.append(Tree(self.lex_units.pop(0)))
        self.stack.append(state)

    def reduciraj(self, number):
        g = self.grammar[number]
        node = Tree(Triplet(g[0], g[1], '')) 

        left_side = ['']
        tmp = []
        while left_side != g[1]:
            el = self.stack.pop() 
            if type(el) is Tree:
                left_side.insert(0, el.data.first)
                tmp.append(el)

        for t in tmp:
            if t.data.second == ['']:
                t.children.append(Tree(Triplet('$', '', '')))

        node.add_child(tmp)
        self.stack.append(node)

    def prihvati(self):
        self.lex_units.pop(0)
        self.stack.pop()
        self.head = self.stack.pop()

    def novo_stanje(self, action):
        self.stack.append(action)
