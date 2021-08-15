import sys
from Automata import *
import copy

def calculateBeginsNow():
    
    for key in productions.keys():
        beginsDict.setdefault(key,[])
        #za svaki key prvo idi po values od key
        # stavi pocetni znak od produkcije, ako nije $ breakaj 
        for transitions in productions[key]:
            for c in transitions:
                con=0
                if c in terminal:
                    beginsDict[key].append(c)
                    break
                elif c in non_terminal:
                    beginsDict[key].append(c)
                    #print(productions[c])
                    for p in productions[c]:
                        if '$' in p:
                            con=1
                if con==1:
                    continue
                break
    return

def calculateBegins():
    tmpDict = copy.deepcopy(beginsDict)
    while True:
        for key in beginsDict.keys():
            for v in beginsDict[key]:
                if v in non_terminal:
                    for v2 in beginsDict[v]:
                        if v2 not in beginsDict[key]:
                            beginsDict[key].append(v2)
            beginsDict[key] =  list(dict.fromkeys(beginsDict[key]))
        if(beginsDict == tmpDict):
            break
        tmpDict = copy.deepcopy(beginsDict)
        #beginsDict.deepcopy()
    return


def calculateEndsNow():
    
    for key in productions.keys():
        endsDict.setdefault(key,[])
        #za svaki key prvo idi po values od key
        # stavi pocetni znak od produkcije, ako nije $ breakaj 
        for transitions in productions[key]:
            lista = copy.deepcopy(transitions)
            lista.reverse()
            #print(lista)
            lista = lista[1:]
            for c in lista:
                con=0
                if (c in terminal or c == '$') and c not in endsDict[key]:
                    endsDict[key].append(c)
                    break
                elif c in non_terminal and c not in endsDict[key]:
                    endsDict[key].append(c)
                    #print(productions[c])
                    for p in productions[c]:
                        if '$' in p:
                            con=1
                if con==1:
                    continue
                break
    
    return

def calculateEnds():
    tmpDict = copy.deepcopy(endsDict)
    while True:
        for key in endsDict.keys():
            for v in endsDict[key]:
                if v in non_terminal:
                    for v2 in endsDict[v]:
                        if v2 not in endsDict[key]:
                            endsDict[key].append(v2)
            endsDict[key] =  list(dict.fromkeys(endsDict[key]))
        if(endsDict == tmpDict):
            break
        tmpDict = copy.deepcopy(endsDict)
        #beginsDict.deepcopy()
    return

def calcParens(value):
    parens = []
    hasDollar=0
    # if value[0] == '':
    #     #print('wu')
    #     parens.append('')
    #     return parens
    for v in value:
        if v in non_terminal:
            for b in beginsDict[v]:
                parens.append(b)
            # for p in productions[v]:
            #     if '$' in p:
            #         hasDollar=1
            #         #break
            if '$' in endsDict[v]:
                #print('wu')
                hasDollar=1
            if hasDollar==0:
                break
        elif v in terminal:
            parens.append(v)
            break

    #print(parens)
    return parens


def inherit(value):
    #parens = []
    if value[0]=='':
        return True
    count = 0
    for v in value:
        if v in non_terminal:
            if '$' in endsDict[v]:
                count+=1
        elif v=='$':
            count+=1
    if count+1 == len(value):
        return True
    else:
        return False


# def beginsRec(state):
#     tmp = []
#     #dodati sve transitions + podnizove iza state u svim produkcijama
#     for t in productions[state]:
#             b = 0
#             for c in t:
#                 if c in terminal:
#                     #print(c)
#                     tmp.append(c)
#                     break
#                 elif c in non_terminal:
#                     #print(c)
#                     tmp2 = beginsRec(c)
#                     for i in tmp2:
#                         tmp.append(i)
#                     #print(tmp)
#                     for i in productions[c]:
#                         #print(i)
#                         if '$' not in i:
#                             #print('b')
#                             b = 1
#                             break
#                 #if b == 1:
#                  #   break
#     #print(tmp)
#     tmp = list(dict.fromkeys(tmp))                  
#     return tmp

def is_reduciraj(enka, states):
    res = False
    for state in states:
        if enka.Q[state].dot >= len(enka.Q[state].name[1]) - 1:
            res =  True
    return res

def get_grammar(enka, grammar, s):
    lg = []
    for g in grammar:
        if s.name == grammar[g]:
            lg.append(g)
    return list(dict.fromkeys(lg))


if __name__ == "__main__":
    #print("generator")

    ulaz = []
    terminal = []
    non_terminal = []
    syn = []
    productions = {}
    key = ''
    grammar = {}
    gram_num = 1

    for line in sys.stdin:
        line = line[:-1]
        #ulaz.append(line)
        #print(line)
        line = line.split(" ")
        #print(line)
        if "%V" in line:
            non_terminal = line[1:]
        elif "%T" in line:
            terminal = line[1:]
        elif "%Syn" in line:
            syn = line[1:]
        elif line[0]!='':
            #print(line)
            key = line[0]
            productions.setdefault(key,[])   
        else:
            #print(line)
            line.append('') # promijeni u []
            productions[key].append(line[1:])
            t = line[1:]
            if '$' in t:
                t.remove('$')
            grammar[gram_num] = (key, t)
            gram_num = gram_num + 1
            #productions[key].append([])


    #print(productions)
    beginState = non_terminal[0]
    productions['<S\'>'] = [[beginState, '']]
    grammar[0] = ('<S\'>', [beginState, ''])
    #print(productions)
    #calculateBegins("<A>", productions)

    # transitions = {}
    # for state in productions.keys():     
    #     for t in productions[state]:
    #         transitions.setdefault(state,[])
    #     for v in productions.values():
    #         #print(v)
    #         for t in v:
    #             #print(v)
    #             if(state in t):
                    
    #                 idx = [i for i, x in enumerate(t) if x == state]
    #                 ok = 1
    #                 for i in idx:
    #                     # for begin in transitions[state]:
    #                     #     #print(t[i+1:])
                            
    #                     #     if t[i+1:] != [] and begin[0] != [] and begin[0] == t[i+1]:
    #                     #         ok = 0
    #                     #         #print(ok)
                                
    #                     if t[i+1:] not in transitions[state] and ok == 1:
    #                         transitions.setdefault(state,[]).append(t[i+1:])
    
    

    # for state in productions.keys():
    #     beginsDict[state] = beginsRec(state)
    
    #transitions = transitions[:-1]
    #print(transitions["<A>"])       
    #print(beginsRec('<A>'))
    #print(transitions)
    #print(productions)
    #print(productions['<A>'])
    beginsDict = {}
    calculateBeginsNow()
    
    calculateBegins()

    

    endsDict = {}
    calculateEndsNow()
   
    calculateEnds()
    #print(endsDict)

    #print(beginsDict)

    for key,value in beginsDict.items():
        beginsDict[key] = list(dict.fromkeys(value))
        for c in non_terminal:
            #print(c)
            beginsDict[key] = list(filter(lambda a: a != c, beginsDict[key]))

    #print(beginsDict)

    enka = E_NKA()
    
    tmpStates = []
    statesStr = []

    pocetno1 = State(('<S\'>',[beginState, '']),[''],0)
    pocetno2 = State(('<S\'>',[beginState, '']),[''],1)

    tmpStates.append(pocetno1)
    statesStr.append(str(pocetno1))
    statesStr.append(str(pocetno2))

    poc = enka.add_state(pocetno1)
    enka.q0 = [poc]
    enka.F = [poc]
    enka.add_state(pocetno2)
    

    while len(tmpStates) > 0:
        currentState = tmpStates.pop()
        # kada je tockica na kraju niza nema prijelaza dalje
        if currentState.dot == len(currentState.name[1])-1:
            continue
        delta = currentState.name[1][currentState.dot]
        if delta != '':
                parensTemp = copy.deepcopy(currentState.parens)
                parensTemp.sort()
                newState = State(currentState.name,parensTemp,currentState.dot+1)
                if str(newState) not in statesStr:
                    statesStr.append(str(newState))
                    tmpStates.append(newState)
                    enka.add_state(newState)
                enka.add_transition(currentState,delta,newState)
                if delta in non_terminal:
                    t = calcParens(currentState.name[1][currentState.dot+1:])
                    if inherit(currentState.name[1][currentState.dot+1:]) == True:
                        #t = list(set(t) | set(currentState.parens))
                        #t = []
                        for p in currentState.parens:
                            if p not in t:
                                t.append(p)
                                #print(t)
                        #print(t)
                    t = list(dict.fromkeys(t))
                    t.sort()
                    for val in productions[delta]:
                        if '$' in val:
                            newState = State((delta,val[1:]),t,0)
                            if str(newState) not in statesStr:
                                statesStr.append(str(newState))
                                tmpStates.append(newState)
                                enka.add_state(newState)
                            enka.add_transition(currentState, '$', newState)
                        else:
                            newState = State((delta,val),t,0)
                            if str(newState) not in statesStr:
                                statesStr.append(str(newState))
                                tmpStates.append(newState)
                                enka.add_state(newState)
                            enka.add_transition(currentState, '$', newState)

    #print(productions)                       
    #print(len(statesStr))
    #for s in statesStr:
    #    print(s)
    #c=0
    #for k,v in enka.lookup.items():
    #    for i in v:
    #        c+=1
    #print(c)
    enka.fix_lookup() # TODO(Dino) : rijesiti ovo odma pri dodavanju tranzicija
    #Util.print_automata(enka)
    dka = Util.enka_to_dka(enka)
    #Util.print_automata(dka)
    
    #print(len(dka.Q))   
    #print(len(dka.lookup.keys()))

    # for g in grammar:
    #     print(f'grammar{g} => {grammar[g]}')
    
    actions = dict()
    terminal.append('$')
    
    for states in dka.Q:
        for state in dka.Q[states]:
            s = enka.Q[state]
            on_end = s.dot >= len(s.name[1]) - 1

            if s == pocetno2:
                actions[(states, '')] = 'Prihvati()'
                continue

            if on_end:
                for t in s.parens:
                    if (states, t) not in actions:
                        gg = get_grammar(enka, grammar, s)
                        if len(gg) > 0:
                            actions[(states , t)] = f"r{gg[0]}"
            
            else:
                symb = s.name[1][s.dot]
                if ((states, symb) in dka.lookup):
                    if symb in terminal:
                        actions[(states, symb)] = f"p{dka.lookup[(states, symb)]}"
                    else:
                        actions[(states, symb)] = f"{dka.lookup[(states, symb)]}"

        # for t in terminal:                    
        #     tmp = []
        #     for s1 in s:
        #         tmp.append(enka.Q[s1])
            
        #     if pocetno2 in tmp and t == '$':
        #         actions[(state, '')] = f'Prihvati()'
        #     else:
        #         if is_reduciraj(enka, s):
        #             for x in s:
        #                 for k in enka.Q[x].parens:
        #                     gg = get_grammar(enka, grammar, s)
        #                     if len(gg) > 0 and (state, k) not in actions:
        #                         actions[(state, k)] = f'r{gg[0]}'
                    
        #             if (state, t) in dka.lookup:
        #                 actions[(state, t)] = f'p{dka.lookup[(state, t)]}'
        #         else:
        #             if (state, t) in dka.lookup:
        #                 actions[(state, t)] = f'p{dka.lookup[(state, t)]}'
        
        # for t in non_terminal:
        #       if (state, t) in dka.lookup:
        #             actions[(state, t)] = f'{dka.lookup[(state, t)]}'

    # print('===actions===')
    # for ac in actions:
    #    print(f'{ac} => {actions[ac]}')
               

    f = open('analizator/SA.py', 'w')
    f.write('from Utils import Util\n')
    f.write('from Utils import Triplet\n')
    f.write('from Utils import Parser\n')

    f.write('lex_units = []\n')
    f.write('if __name__ == \'__main__\':\n')
    f.write('\tUtil.parse_anaylzer_input(lex_units)\n')
    
    f.write('\tactions = {}\n')    
    for key in actions:
        f.write(f'\tactions[("{key[0]}", "{key[1]}")] = "{actions[key]}"\n')

    f.write('\tgrammar = {}\n')
    for key in grammar:
        f.write(f'\tgrammar["{key}"] = {grammar[key]}\n')
    
    f.write('\tsyn = []\n')
    for s in syn:
        f.write(f'\tsyn.append("{s}")\n')
    f.write('\tparser = Parser(lex_units, syn, actions, grammar)\n')
    f.write('\tparser.simulate()\n')
    f.close()

