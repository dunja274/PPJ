class State:
    id = ""
    name = tuple()
    parens = []
    dot = 0

    def __init__(self, name, parens, dot):
        self.name = name    
        self.parens = parens
        self.dot = dot

    def __str__(self):
        gram = ''
        for g in self.name[1]:
            gram = gram + g
        return f'{self.name[0]}->{gram} {{{self.parens}}} {self.dot}'
    
    def __repr__(self):
        gram = ''
        for g in self.name[1]:
            gram = gram + g
        return f'{self.name[0]}->{gram} {{{self.parens}}} {self.dot}'

    def __eq__(self, other):
        if isinstance(other, State):
            return ((self.name, self.parens, self.dot) ==
                (other.name, other.parens, other.dot))
        else:
            return False

    def __hash__(self):
        h = hash(self.name[0])
        for par in self.name[1]:
            h = h ^ hash(par)
        h = h ^ hash(self.dot)
        return h

    @staticmethod
    def sorted_name(State):
        return State.name

class E_NKA:
    curr = 0
    Q = dict()
    F = []
    L = set()
    lookup = dict()
    q0 = ''

    def add_state(self, state):
        self.Q[self.curr] = state
        self.curr += 1
        return self.curr - 1

    def find_id(self, state):
        for s in self.Q:
            if state == self.Q[s]:
                return s
    
    def add_transition(self, state_old, delta, state_new):
        key = (state_old, delta)
        if key not in self.lookup:
            self.lookup[key] = []
        self.lookup[key].append(state_new)

    def e_closure(self, Q):
        Y = [Q]
        stack = [Q]
        
        while len(stack) != 0:
            q = stack.pop()
            key = (q, '$')
            if key in self.lookup:
                for state in self.lookup[key]:
                    if state not in Y:
                        Y.append(state)
                        stack.append(state)
        return Y 

    def fill_langauge(self):
        for key in self.lookup:
            new_state = self.lookup[key]
            self.L.add(key[1])
        return self.L
    
    def fix_lookup(self):
        new = {}
        for state in self.lookup:
            id1 = self.find_id(state[0])
            id2 = []
            for s in self.lookup[state]:
                id2.append(self.find_id(s))
            new[id1, state[1]] = id2
        self.lookup = new

class DKA:
    Q = dict()
    L = set()
    F = []
    q0 = []
    lookup = {}

    def lookup_num(self, states):
        for state in self.Q:
            if states == self.Q[state]:
                return state
        return -1
   
class Util:
    @staticmethod
    def enka_to_dka(enka):
        dka = DKA()
        dka.q0 = []
        dka.L = enka.fill_langauge()
        dka.L.remove('$')
        
        e_closures = dict()
        for state in enka.Q:
            e_closures[state] = enka.e_closure(state)

        dka.q0.append(e_closures[0])
        dka.Q[0] = dka.q0[0]
        
        new_Q = set()
        new_Q.add(0)

        stack = []
        stack.append(dka.q0[0])

        state_num = 0
        new_state = set()

        while len(stack) > 0:
            curr_q = stack.pop()
            curr_id = dka.lookup_num(curr_q)

            for l in dka.L:    
                
                moves = []
                for q in curr_q:    
                    key = (q, l)
                    if key in enka.lookup:
                        tmp = enka.lookup[key]
                        for t in tmp:
                            moves.append(t)
                moves = list(dict.fromkeys(moves))
                moves.sort(key= lambda x : id(x), reverse=True)
                
                new = []
                for move in moves:
                    tmp = e_closures[move]
                    for t in tmp:
                        new.append(t)
    
                new = list(dict.fromkeys(new))
                new.sort(key= lambda x : id(x), reverse=True)

                ids = []
                for n in new:
                    ids.append(id(n))
                
                if len(new) > 0:
                    if str(ids) not in new_state:
                        stack.append(new)
                        state_num += 1
                        dka.Q[state_num] = new
                    dka.lookup[curr_id, l] = new
                    new_state.add(str(ids))
        
        dka.q0 = [dka.q0]

        for look in dka.lookup:
            dka.lookup[look] = dka.lookup_num(dka.lookup[look])
            

        for state in dka.Q:
            if enka.q0 in dka.Q[state]:
                dka.F.append(dka.Q[state])
        return dka

    @staticmethod
    def print_lookup(lookup):
        for look in lookup:
            print(f"{look} => {lookup[look]}")

    @staticmethod
    def print_automata(automata):
        print("================== Automata ==================")
        print("===== States =====")
        for key in automata.Q:
            print(f'#{key} {automata.Q[key]}')
        print("===== Finite states =====")
        for state in automata.F:
            print(f'#{state}')
        print("===== Start states =====")
        for state in automata.q0:
            print(f'#{state}')
        print("===== Lookup table =====")
        Util.print_lookup(automata.lookup)