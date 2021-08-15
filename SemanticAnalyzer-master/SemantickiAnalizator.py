import sys

class Response():
    tip = ''
    ime = ''
    l_izraz = ''
    br_elem = 0

    def __init__(self, tip, ime, l_izraz, br_elem):
        self.tip = tip
        self.ime = ime
        self.l_izraz = l_izraz
        self.br_elem = br_elem

class Function():
    name = None
    pov = None
    args = None
    tip = 'dec'
    l_izraz = None

    def __init__(self, name, pov, args, tip):
        self.name = name
        self.args = args
        self.pov = pov
        self.tip = tip
        if tip == 'char' or tip == 'int':
            self.l_izraz = 1

    def __eq__(self, other):
        if isinstance(other, Function):
            return self.tip + '_' + self.name
        return False

    def __str__(self):
        return f'{self.pov} {self.name}({self.args})'
    
    def __hash__(self):
        return hash(self.tip + '_' + self.name + str(self.args))

class Variable():
    ime = None
    tip = None
    l_izraz = 0

    def __init__(self, ime, tip):
        self.ime = ime
        self.tip = tip
        if tip == 'char' or tip == 'int':
            self.l_izraz = 1

    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.ime
        return False

    def __str__(self):
        return f'{self.tip} {self.ime}'

    def __hash__(self):
        return hash(f'{self.tip} {self.ime}')

class Node():
    children = []
    data = ''
    depth = -1
    parent = None
    var = []
    functions = []

    def __init__(self, data, depth):
        self.data = data
        self.depth = depth
        self.children = []
        self.var = []
        self.functions = []

    def __str__(self):
        tmp = f'lvl:{self.depth} | {self.data}\n'
        tmp += f'parent : {self.parent}'
        for child in self.children:
            tmp += f'\t{child.data}\n'
        return tmp

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.data.split(' ')[0] == other.data.split(' ')[0] and self.data.detph == other.depth
        return False

    def print(self, tab):
        print(f"{' ' * tab}{self.data} {self.var}")
        for child in self.children:
            child.print(tab + 1)

def connect_parent_nodes(node, prev):
    node.parent = prev
    for child in node.children:
        connect_parent_nodes(child, node)

def read_input():
    stack = []
    for line in sys.stdin:
        depth = len(line) - len(line.lstrip())
        n = Node(line.strip(), depth)
        stack.append(n)

    poped = None
    while len(stack) > 0:
        poped = stack.pop()
        for i in range(len(stack) - 1, -1, -1):
            if stack[i].depth == (poped.depth - 1):
                stack[i].children.insert(0, poped)
                break
    connect_parent_nodes(poped, None)
    return poped

def print_err(node):
    err_msg = f'{node.data} ::='
    for i in range(0, len(node.children)):
        if len(node.children[i].children) == 0:
            err_msg += f' {node.children[i].data.split(" ")[0]}({node.children[i].data.split(" ")[1]},{node.children[i].data.split(" ")[2]})'
        else:
            err_msg += f' {node.children[i].data.split(" ")[0]}'
    print(err_msg)
    exit(1)

def check_type_is(actual, expected):
    if actual != expected:
        return False
    return True

def check_type_not(actual, not_expected):
    return ~check_type_is(actual, not_expected)

def check_int_range(value):
    if value < -2147483648 or value > 2147483647:
        return False
    return True

def check_char_valid(value):
    if len(value) == 4:
        if value[3] != 't' or value[3] != 'n' or value[3] != '0' or value[3] != '\'' or value[3] != "\"" or value[3] != "\\":
            return False
    return True

def check_string_valid(value):
    for i in range(0, len(value)):
        if value[i] == '\\':
            val = check_char_valid(f'\'{value[i]}{value[i + 1]}\'')
            i = i + 1
        else:
            val = check_char_valid(f'\'{value[i]}\'')
        if val == False:
            return False
    return True

def check_cast_valid(ltip, rtip):
    if ltip == rtip:
        return True
    if 'niz' in ltip and 'niz' in rtip and 'const' in rtip:
        if ltip[4:-1] == rtip[10:-2]:
            return True
        ltip = ltip[4:-1]
        rtip = rtip[4:-1]
    if 'const' in ltip:
        ltip = ltip[6:-1]
        if ltip == rtip:
            return True
    if 'const' in rtip:
        rtip = rtip[6:-1]
        if ltip == rtip:
            return True
    if ltip == 'char' and rtip == 'int':
        return True
    return False

def check_exp_cast_valid(ltip, rtip):
    if ltip[0:5] == 'const':
        ltip = ltip[:-1]
        ltip = ltip[6:]
    if rtip[0:5] == 'const':
        rtip = rtip[:-1]
        rtip = rtip[6:]
    if ltip == 'int' and rtip == 'char':
        return True
    elif ltip == 'char' and rtip == 'int':
        return True
    elif ltip == rtip:
        return True
    else:
        return False

def inicijalizator_to_niz_znakova(node):
    while len(node.children) != 0:
        node = node.children[0]
    if node.data.split(' ')[0] == "NIZ_ZNAKOVA":
        return len(node.data.split(' ')[2])
    else:
        return None

def check_functions(func, args, pov):
    if len(func) == 0:
        return False
    br = 0
    for f in func:
        if f.args != args or f.pov != pov:
            br = br + 1
    return br > 0

def ret_function(functions, name, tip):
    tmp = []
    for func in functions:
        if func.name == name and func.tip == tip:
            tmp.append(func)
    return tmp

def ret_variable(variables, var_name):
    for var in variables:
        if var.ime == var_name:
            return var
    return None

def check_function_definied(node, func_name):
    if node == None:
        return None
    func = ret_function(node.functions, func_name, 'def')
    if func != []:
        return func
    return check_function_definied(node.parent, func_name)

def check_function_declared_global(node, func_name):
    func = ret_function(node.functions, func_name, 'dec')
    return func

def check_function_declared_local(node, func_name):
    if node == None or node.data == '<slozena_naredba>':
        return []
    func = ret_function(node.functions, func_name, 'dec')
    if func != []:
        return func
    return check_function_declared_local(node.parent, func_name)

def save_function(node, function):
    if node == None:
        return
    node.functions.insert(0, function)
    node.functions = list(dict.fromkeys(node.functions))
    save_function(node.parent, function)

def check_if_declared(node, var_name):
    if node == None:
        return False
    var = ret_variable(node.var, var_name)
    if var != None:
        return var
    func = check_function_declared_local(node, var_name)
    if func != []:
        return func
    return check_if_declared(node.parent, var_name)

def check_if_main_correct():
    main = ret_function(head.functions, 'main', 'dec')
    if main == []:
        print('main')
        exit(1)
    if check_functions(main, "void", "int") != False:
        print('main')
        exit(1)

def save_variable(node, variable):
    if node == None:
        return
    if node.data == '<slozena_naredba>':
        node.var.insert(0, variable)
        node.var = list(dict.fromkeys(node.var))
        return
    node.var.insert(0, variable)
    node.var = list(dict.fromkeys(node.var))
    save_variable(node.parent, variable)

def check_variable_local(node, var_name):
    if node == None:
        return None
    if node.data == '<slozena_naredba>':
        var = ret_variable(node.var, var_name)
        return var
    var = ret_variable(node.var, var_name)
    if var != None:
        return var
    return check_variable_local(node.parent, var_name)

def check_inside_loop(node):
    if node == None:
        return False
    if node.data == '<naredba_petlje>':
        return True
    return check_inside_loop(node.parent)

def check_inside_function(node):
    if node == None:
        return None
    if node.functions != None:
        for func in node.functions:
            if func.tip == 'def':
                return func
    return check_inside_function(node.parent)

def undecleared_function():
    print('funkcija')
    exit(1)

def check_if_all_functions_declared():
    res = False
    for fun1 in head.functions:
        for fun2 in head.functions:
            if fun1.name == fun2.name and fun1.tip == 'dec' and fun2.tip == 'def':
                res = True
                continue
        if res == False:
            undecleared_function()
        res = False
    return True

def primarni_izraz_check(node, lside):
    if lside[0].data.split(' ')[0] == 'IDN':
        IDN = check_if_declared(node, lside[0].data.split(" ")[2])
        if IDN == False:
            print_err(node)
        if isinstance(IDN, Variable): 
            return Response(IDN.tip, None, IDN.l_izraz, None)
        else:
            return Response(IDN, None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'BROJ':
        num = int(lside[0].data.split(" ")[2])
        if check_int_range(num) == False:
            print_err(node)
        return Response("int", None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'ZNAK':
        if check_char_valid(lside[0].data.split(" ")[2]) == False:
            print_err(node)
        return Response("char", None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'NIZ_ZNAKOVA':
        if check_string_valid(lside[0].data.split(" ")[2]) == False:
            print_err(node)
        return Response("niz(const(char))", None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'L_ZAGRADA' and lside[1].data == '<izraz>' and lside[2].data.split(' ')[0] == 'D_ZAGRADA':
        izraz = izraz_check(lside[1], lside[1].children)
        return izraz

def postfiks_izraz_check(node, lside):
    if lside[0].data == '<primarni_izraz>':
        primarni_izraz = primarni_izraz_check(lside[0], lside[0].children)
        return primarni_izraz
    
    elif lside[0].data == '<postfiks_izraz>' and lside[1].data.split(' ')[0] == 'L_UGL_ZAGRADA' and lside[2].data == '<izraz>' and lside[3].data.split(' ')[0] == 'D_UGL_ZAGRADA':
        postfiks_izraz = postfiks_izraz_check(lside[0], lside[0].children)
        if check_type_is(postfiks_izraz.tip[0:3], "niz") == False:
            print_err(node)
        izraz = izraz_check(lside[2], lside[2].children)
        if check_cast_valid(izraz.tip, "int") == False:
            print_err(node)
        return Response(izraz.tip, None, 1, None)
    
    elif lside[0].data == '<postfiks_izraz>' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data.split(' ')[0] == 'D_ZAGRADA':
        postfiks_izraz = postfiks_izraz_check(lside[0], lside[0].children)    
        func = postfiks_izraz.tip[0]
        if isinstance(func, Function) == False:
            undecleared_function()
        if func.args != 'void':
            print_err(node)
        return Response(func.pov, None, 0, None)

    elif lside[0].data == '<postfiks_izraz>' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<lista_argumenata>' and lside[3].data.split(' ')[0] == 'D_ZAGRADA':
        postfiks_izraz = postfiks_izraz_check(lside[0], lside[0].children)
        lista_arugmenata = lista_argumenata_check(lside[2], lside[2].children)
        func = postfiks_izraz.tip[0]
        if isinstance(func, Function) == False:
            undecleared_function()
        if len(lista_arugmenata.tip) != len(func.args):
            print_err(node)
        for i in range(0, len(lista_arugmenata.tip)):
            arg_tip = lista_arugmenata.tip[i]
            param_tip = lista_arugmenata.tip[i]
            if check_cast_valid(arg_tip, param_tip) == False:
                print_err(node)
        return Response(func.pov, None, 0, None)
    
    elif lside[0].data == '<postfiks_izraz>' and (lside[1].data.split(' ')[0] == 'OP_INC' or lside[1].data.split(' ')[0] == 'OP_DEC'):
        postfiks_izraz = postfiks_izraz_check(lside[0], lside[0].children)
        if postfiks_izraz.l_izraz != 1 or check_cast_valid(postfiks_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def lista_argumenata_check(node, lside):
    if lside[0].data == '<izraz_pridruzivanja>':
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[0], lside[0].children)
        return Response([izraz_pridruzivanja.tip], None, 0, None)
    
    elif lside[0].data == '<lista_argumenata>' and lside[1].data.split(' ')[0] == 'ZAREZ' and lside[2].data == '<izraz_pridruzivanja>':
        lista_argumenata = lista_argumenata_check(lside[0], lside[0].children)
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[2], lside[2].children)
        return Response(lista_argumenata.tip + [izraz_pridruzivanja.tip], None, 0, None)

def unarni_izraz_check(node, lside):
    if lside[0].data == '<postfiks_izraz>':
        res = postfiks_izraz_check(lside[0], lside[0].children)
        return res
    
    elif (lside[0].data.split(' ')[0] == 'OP_INC' or lside[0].data.split(' ')[0] == 'OP_DEC') and lside[1].data == '<unarni_izraz>':
        unarni_izraz = unarni_izraz_check(lside[1], lside[1].children)
        if unarni_izraz.l_izraz != 1 or check_cast_valid(unarni_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)
    
    elif lside[0].data == '<unarni_operator>' and lside[1].data == '<cast_izraz>':
        cast_izraz = cast_izraz_check(lside[1], lside[1].children)
        if check_cast_valid(cast_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def cast_izraz_check(node, lside):
    if lside[0].data == '<unarni_izraz>':
        unarni_izraz = unarni_izraz_check(lside[0], lside[0].children)
        return unarni_izraz
    
    elif lside[0].data.split(' ')[0] == 'L_ZAGRADA' and lside[1].data == '<ime_tipa>' and lside[2].data.split(' ')[0] == 'D_ZAGRADA' and lside[3].data == '<cast_izraz>':
        ime_tipa = ime_tipa_check(lside[1], lside[1].children)
        cast_izraz = cast_izraz_check(lside[3], lside[3].children)
        if isinstance(ime_tipa.tip, Function) or isinstance(cast_izraz.tip, Function):
            return print_err(node)
        if check_exp_cast_valid(cast_izraz.tip, ime_tipa.tip) == False:
            return print_err(node)
        return Response(ime_tipa.tip, None, 0, None)

def ime_tipa_check(node, lside):
    if lside[0].data == '<specifikator_tipa>':
        tip = specifikator_tipa_check(lside[0], lside[0].children)
        return Response(tip, None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'KR_CONST' and lside[1].data == '<specifikator_tipa>':
        tip = specifikator_tipa_check(lside[1], lside[1].children)
        if check_type_is(tip, "void") == True:
            print_err(node)
        return Response(f'const({tip})', None, 0, None)

def specifikator_tipa_check(node, lside):    
    if lside[0].data.split(' ')[0] == 'KR_VOID': 
        return "void"
    elif lside[0].data.split(' ')[0] == 'KR_CHAR':
        return "char"
    elif lside[0].data.split(' ')[0] == 'KR_INT':
        return "int"

def multiplikativni_izraz_check(node, lside):
    if lside[0].data == '<cast_izraz>':
        cast_izraz = cast_izraz_check(lside[0], lside[0].children)
        return cast_izraz
    
    elif lside[0].data == '<multiplikativni_izraz>' and (lside[1].data.split(' ')[0] == 'OP_PUTA' or lside[1].data.split(' ')[0] == 'OP_DIJELI' or lside[1].data.split(' ')[0] == 'OP_MOD') and lside[2].data == '<cast_izraz>':
        multiplikativni_izraz = multiplikativni_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(multiplikativni_izraz.tip, 'int') == False:
            print_err(node)
        cast_izraz = cast_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(cast_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def aditivni_izraz_check(node, lside):
    if lside[0].data == '<multiplikativni_izraz>':
        multiplikativni_izraz = multiplikativni_izraz_check(lside[0], lside[0].children)
        return multiplikativni_izraz
    
    elif lside[0].data == '<aditivni_izraz>' and (lside[1].data.split(' ')[0] == 'PLUS' or lside[1].data.split(' ')[0] == 'MINUS') and lside[2].data == '<multiplikativni_izraz>':
        aditivni_izraz = aditivni_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(aditivni_izraz.tip, 'int') == False:
            print_err(node)
        multiplikativni_izraz = multiplikativni_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(multiplikativni_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def odnosni_izraz_check(node, lside):
    if lside[0].data == '<aditivni_izraz>':
        aditivni_izraz = aditivni_izraz_check(lside[0], lside[0].children)
        return aditivni_izraz
    elif lside[0].data == '<odnosni_izraz>' and (lside[1].data.split(' ')[0] == 'OP_LT' or lside[1].data.split(' ')[0] == 'OP_GT' or lside[1].data.split(' ')[0] == 'OP_LTE' or lside[1].data.split(' ')[0] == 'OP_GTE') and lside[2].data == '<aditivni_izraz>':
        odnosni_izraz = odnosni_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(odnosni_izraz.tip, 'int') == False:
            print_err(node)
        aditivni_izraz = aditivni_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(aditivni_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def jednakosni_izraz_check(node, lside):
    if lside[0].data == '<odnosni_izraz>':
        odnosni_izraz = odnosni_izraz_check(lside[0], lside[0].children)
        return odnosni_izraz
    
    elif lside[0].data == '<jednakosni_izraz>' and (lside[1].data.split(' ')[0] == 'OP_EQ' or lside[1].data.split(' ')[0] == 'OP_NEQ') and lside[2].data == '<odnosni_izraz>':
        jednakosni_izraz = jednakosni_izraz_check(lside[0], lside[0].children)
        if isinstance(jednakosni_izraz.tip, Function) or check_cast_valid(jednakosni_izraz.tip, 'int') == False:
            print_err(node)
        odnosni_izraz = odnosni_izraz_check(lside[2], lside[2].children)
        if isinstance(odnosni_izraz.tip, Function) or check_cast_valid(odnosni_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def bin_i_izraz_check(node, lside):
    if lside[0].data == '<jednakosni_izraz>':
        jednakosni_izraz = jednakosni_izraz_check(lside[0], lside[0].children)
        return jednakosni_izraz
    
    elif lside[0].data == '<bin_i_izraz>' and lside[1].data.split(' ')[0] == 'OP_BIN_I' and lside[2].data == '<jednakosni_izraz>':
        bin_i_izraz = bin_i_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(bin_i_izraz.tip, 'int') == False:
            print_err(node)
        jednakosni_izraz = jednakosni_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(jednakosni_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def bin_xili_izraz_check(node, lside):
    if lside[0].data == '<bin_i_izraz>':
        bin_i_izraz = bin_i_izraz_check(lside[0], lside[0].children)
        return bin_i_izraz
    
    elif lside[0].data == '<bin_xili_izraz>' and lside[1].data.split(' ')[0] == 'OP_BIN_XILI' and lside[2].data == '<bin_i_izraz>':
        bin_xili_izraz = bin_xili_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(bin_xili_izraz.tip, 'int') == False:
            print_err(node)
        bin_i_izraz = bin_i_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(bin_i_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def bin_ili_izraz_check(node, lside):
    if lside[0].data == '<bin_xili_izraz>':
        bin_xili_izraz = bin_xili_izraz_check(lside[0], lside[0].children)
        return bin_xili_izraz
    elif lside[0].data == '<bin_ili_izraz>' and lside[1].data.split(' ')[0] == 'OP_BIN_ILI' and lside[2].data == '<bin_xili_izraz>':
        bin_ili_izraz = bin_ili_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(bin_ili_izraz.tip, 'int') == False:
            print_err(node)
        bin_xili_izraz = bin_xili_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(bin_xili_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def log_i_izraz_check(node, lside):
    if lside[0].data == '<bin_ili_izraz>':
        bin_ili_izraz = bin_ili_izraz_check(lside[0], lside[0].children)
        return bin_ili_izraz
    elif lside[0].data == '<log_i_izraz>' and lside[1].data.split(' ')[0] == 'OP_I' and lside[2].data == '<bin_ili_izraz>':
        log_i_izraz = log_i_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(log_i_izraz.tip, 'int') == False:
            print_err(node)
        bin_ili_izraz = bin_ili_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(bin_ili_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def log_ili_izraz_check(node, lside):
    if lside[0].data == '<log_i_izraz>':
        log_i_izraz = log_i_izraz_check(lside[0], lside[0].children)
        return log_i_izraz
    elif lside[0].data == '<log_ili_izraz>' and lside[1].data.split(' ')[0] == 'OP_ILI' and lside[2].data == '<log_i_izraz>':
        log_ili_izraz = log_ili_izraz_check(lside[0], lside[0].children)
        if check_cast_valid(log_ili_izraz.tip, 'int') == False:
            print_err(node)
        log_i_izraz = log_i_izraz_check(lside[2], lside[2].children)
        if check_cast_valid(log_i_izraz.tip, 'int') == False:
            print_err(node)
        return Response("int", None, 0, None)

def izraz_pridruzivanja_check(node, lside):
    if lside[0].data == '<log_ili_izraz>':
        log_ili_izraz = log_ili_izraz_check(lside[0], lside[0].children)
        return log_ili_izraz

    elif lside[0].data == '<postfiks_izraz>' and lside[1].data.split(' ')[0] == 'OP_PRIDRUZI' and lside[2].data == '<izraz_pridruzivanja>':
        postfiks_izraz = postfiks_izraz_check(lside[0], lside[0].children)
        if postfiks_izraz.l_izraz != 1:
            print_err(node)
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[2], lside[2].children)
        if check_cast_valid(izraz_pridruzivanja.tip, postfiks_izraz.tip) == False:
            print_err(node)
        return Response(postfiks_izraz.tip, None, 0, None)

def izraz_check(node, lside):
    if lside[0].data == '<izraz_pridruzivanja>':
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[0], lside[0].children)
        return izraz_pridruzivanja
    
    elif lside[0].data == '<izraz>' and lside[1].data.split(' ')[0] == 'ZAREZ' and lside[2].data == '<izraz_pridruzivanja>':
        izraz_check(lside[0], lside[0].children)
        res = izraz_pridruzivanja_check(lside[2], lside[2].children)
        return Response(res.tip, None, 0, None)

def slozena_naredba_check(node, lside, lista_tipova, lista_imena):
    for i in range(0, len(lista_tipova)):
        save_variable(node, Variable(lista_imena[i], lista_tipova[i]))

    if lside[0].data.split(' ')[0] == 'L_VIT_ZAGRADA' and lside[1].data == '<lista_naredbi>' and lside[2].data.split(' ')[0] == 'D_VIT_ZAGRADA':
        lista_naredbi_check(lside[1], lside[1].children)
    elif lside[0].data.split(' ')[0] == 'L_VIT_ZAGRADA' and lside[1].data == '<lista_deklaracija>' and lside[2].data == '<lista_naredbi>' and lside[3].data.split(' ')[0] == 'D_VIT_ZAGRADA':
        lista_deklaracija_check(lside[1], lside[1].children)
        lista_naredbi_check(lside[2], lside[2].children)

def lista_naredbi_check(node, lside):
    if lside[0].data == '<naredba>':
        naredba_check(lside[0], lside[0].children)
    elif lside[0].data == '<lista_naredbi>' and lside[1].data == '<naredba>':
        lista_naredbi_check(lside[0], lside[0].children)
        naredba_check(lside[1], lside[1].children)

def naredba_check(node, lside):
    if lside[0].data == '<slozena_naredba>':
        slozena_naredba_check(lside[0], lside[0].children, [], [])
    elif lside[0].data == '<izraz_naredba>':
        izraz_naredba_check(lside[0], lside[0].children)
    elif lside[0].data == '<naredba_grananja>':
        naredba_grananja_check(lside[0], lside[0].children)
    elif lside[0].data == '<naredba_petlje>':
        naredba_petlje_check(lside[0], lside[0].children)
    elif lside[0].data == '<naredba_skoka>':
        naredba_skoka_check(lside[0], lside[0].children)

def izraz_naredba_check(node, lside):
    if lside[0].data.split(' ')[0] == 'TOCKAZAREZ':
        return Response("int", None, 0, None)
    elif lside[0].data == '<izraz>' and lside[1].data.split(' ')[0] == 'TOCKAZAREZ':
        res = izraz_check(lside[0], lside[0].children)
        return Response(res.tip, None, 0, None)

def naredba_grananja_check(node, lside):
    if len(lside) == 7 and lside[0].data.split(' ')[0] == 'KR_IF' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<izraz>' and lside[3].data.split(' ')[0] == 'D_ZAGRADA' and lside[4].data == '<naredba>' and lside[5].data.split(' ')[0] == 'KR_ELSE' and lside[6].data == '<naredba>':
        izraz = izraz_check(lside[2], lside[2].children)
        if isinstance(izraz, Function) or check_cast_valid(izraz.tip, 'int') == False:
            print_err(node)
        naredba_check(lside[4], lside[4].children)
        naredba_check(lside[6], lside[6].children)

    elif lside[0].data.split(' ')[0] == 'KR_IF' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<izraz>' and lside[3].data.split(' ')[0] == 'D_ZAGRADA' and lside[4].data == '<naredba>':
        izraz = izraz_check(lside[2], lside[2].children)
        if isinstance(izraz.tip, Function) or check_cast_valid(izraz.tip, 'int') == False:
            print_err(node)
        naredba_check(lside[4], lside[4].children)
    
def naredba_petlje_check(node, lside):
    if lside[0].data.split(' ')[0] == 'KR_WHILE' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<izraz>' and lside[3].data.split(' ')[0] == 'D_ZAGRADA' and lside[4].data == '<naredba>':
        izraz = izraz_check(lside[2], lside[2].children)
        if check_cast_valid(izraz.tip, 'int') == False:
            print_err(node)
        naredba_check(lside[4], lside[4].children)
    
    elif lside[0].data.split(' ')[0] == 'KR_FOR' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<izraz_naredba>' and lside[3].data == '<izraz_naredba>' and lside[4].data.split(' ')[0] == 'D_ZAGRADA' and lside[5].data == '<naredba>':
        izraz_naredba_check(lside[2], lside[2].children)
        izraz_naredba2 = izraz_naredba_check(lside[3], lside[3].children)
        if check_cast_valid(izraz_naredba2.tip, 'int') == False:
            print_err(node)
        naredba_check(lside[5], lside[5].children)
    
    elif lside[0].data.split(' ')[0] == 'KR_FOR' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<izraz_naredba>' and lside[3].data == '<izraz_naredba>' and lside[4].data == '<izraz>' and lside[5].data.split(' ')[0] == 'D_ZAGRADA' and lside[6].data == '<naredba>':
        izraz_naredba_check(lside[2], lside[2].children)
        izraz_naredba2 = izraz_naredba_check(lside[3], lside[3].children)
        if check_cast_valid(izraz_naredba2.tip, 'int') == False:
            print_err(node)
        izraz_check(lside[4], lside[4].children)
        naredba_check(lside[6], lside[6].children)

def naredba_skoka_check(node, lside):
    if (lside[0].data.split(' ')[0] == 'KR_CONTINUE' or lside[0].data.split(' ')[0] == 'KR_BREAK') and lside[1].data.split(' ')[0] == 'TOCKAZAREZ':
        if check_inside_loop(node) == False:
            print_err(node)

    elif lside[0].data.split(' ')[0] == 'KR_RETURN' and lside[1].data.split(' ')[0] == 'TOCKAZAREZ':
        func = head.functions[0]
        if func == None or func.pov != 'void':
            print_err(node)

    elif lside[0].data.split(' ')[0] == 'KR_RETURN' and lside[1].data == '<izraz>' and lside[2].data.split(' ')[0] == 'TOCKAZAREZ':
        izraz = izraz_check(lside[1], lside[1].children)
        func = check_inside_function(node)
        
        if isinstance(izraz.tip[0], Function) == True:
            tip = izraz.tip[0].pov
            if func.args != izraz.tip[0].args:
                print_err(node)
        else:
            tip = izraz.tip
        if func == None or check_cast_valid(tip, func.pov) == False:
            print_err(node)

def prijevodna_jedinica_check(node, lside):
    if lside[0].data == '<vanjska_deklaracija>':
        vanjska_deklaracija_check(lside[0], lside[0].children)
    
    elif lside[0].data == '<prijevodna_jedinica>' and lside[1].data == '<vanjska_deklaracija>':
        prijevodna_jedinica_check(lside[0], lside[0].children)
        vanjska_deklaracija_check(lside[1], lside[1].children)

def vanjska_deklaracija_check(node, lside):
    if lside[0].data == '<definicija_funkcije>':
        definicija_funkcije_check(lside[0], lside[0].children)
    
    elif lside[0].data == '<deklaracija>':
        deklaracija_check(lside[0], lside[0].children)

def definicija_funkcije_check(node, lside):
    if lside[0].data == '<ime_tipa>' and lside[1].data.split(' ')[0] == 'IDN' and lside[2].data.split(' ')[0] == 'L_ZAGRADA' and lside[3].data.split(' ')[0] == 'KR_VOID' and lside[4].data.split(' ')[0] == 'D_ZAGRADA' and lside[5].data == '<slozena_naredba>':
        ime_tipa = ime_tipa_check(lside[0], lside[0].children)
        if check_type_is(ime_tipa.tip[0:5], "const") == True:
            print_err(node)
        if check_function_definied(node, lside[1].data.split(' ')[2]) != None:
            print_err(node)
        func = check_function_declared_global(head, lside[1].data.split(' ')[2])
        if func != []:
            if check_functions(func, "void", ime_tipa.tip) == False:
                print_err(node)
        save_function(node, Function(lside[1].data.split(' ')[2], ime_tipa.tip, "void", 'def'))
        save_function(node, Function(lside[1].data.split(' ')[2], ime_tipa.tip, "void", 'dec'))
        slozena_naredba_check(lside[5], lside[5].children, [], [])

    elif lside[0].data == '<ime_tipa>' and lside[1].data.split(' ')[0] == 'IDN' and lside[2].data.split(' ')[0] == 'L_ZAGRADA' and lside[3].data == '<lista_parametara>' and lside[4].data.split(' ')[0] == 'D_ZAGRADA' and lside[5].data == '<slozena_naredba>':
        ime_tipa = ime_tipa_check(lside[0], lside[0].children)
        if check_type_is(ime_tipa.tip[0:5], "const") == True:
            print_err(node)
        if check_function_definied(node, lside[1].data.split(' ')[2]) != None:
            print_err(node)
        lista_parametara = lista_parametara_check(lside[3], lside[3].children)
        func = check_function_declared_global(head, lside[1].data.split(' ')[2])
        if func != []:
            if check_functions(func, lista_parametara.tip, ime_tipa.tip) == False:
                print_err(node)
        save_function(node, Function(lside[1].data.split(' ')[2], ime_tipa.tip, lista_parametara.tip, 'def'))
        save_function(node, Function(lside[1].data.split(' ')[2], ime_tipa.tip, lista_parametara.tip, 'dec'))
        slozena_naredba_check(lside[5], lside[5].children, lista_parametara.tip, lista_parametara.ime)

def lista_parametara_check(node, lside):
    if lside[0].data == '<deklaracija_parametra>':
        deklaracija_parametra = deklaracija_parametra_check(lside[0], lside[0].children)
        return Response([deklaracija_parametra.tip], [deklaracija_parametra.ime], None, None)
   
    elif lside[0].data == '<lista_parametara>' and lside[1].data.split(' ')[0] == 'ZAREZ' and lside[2].data == '<deklaracija_parametra>':
        lista_parametara = lista_parametara_check(lside[0], lside[0].children)
        deklaracija_parametra = deklaracija_parametra_check(lside[2], lside[2].children)
        if deklaracija_parametra.ime in lista_parametara.ime:
            print_err(node)
        return Response([deklaracija_parametra.tip] + lista_parametara.tip, [deklaracija_parametra.ime] + lista_parametara.ime, None, None)

def deklaracija_parametra_check(node, lside):
    if len(lside) == 2 and lside[0].data == '<ime_tipa>' and lside[1].data.split(' ')[0] == 'IDN':
        ime_tipa = ime_tipa_check(lside[0], lside[0].children)
        return Response(ime_tipa.tip, lside[1].data.split(' ')[2], None, None)
    
    elif lside[0].data == '<ime_tipa>' and lside[1].data.split(' ')[0] == 'IDN' and lside[2].data.split(' ')[0] == 'L_UGL_ZAGRADA' and lside[3].data.split(' ')[0] == 'D_UGL_ZAGRADA':
        ime_tipa = ime_tipa_check(lside[0], lside[0].children)
        if check_type_not(ime_tipa.tip, "void") == False:
            print_err(node)
        return Response(f'niz({ime_tipa.tip})', lside[1].data.split(' ')[2], None, None)

def lista_deklaracija_check(node, lside):
    if lside[0].data == '<deklaracija>':
        deklaracija_check(lside[0], lside[0].children)
    
    elif lside[0].data == '<lista_deklaracija>' and lside[1].data == '<deklaracija>':
        lista_deklaracija_check(lside[0], lside[0].children)
        deklaracija_check(lside[1], lside[1].children)

def deklaracija_check(node, lside):
    if lside[0].data == '<ime_tipa>' and lside[1].data == '<lista_init_deklaratora>' and lside[2].data.split(' ')[0] == 'TOCKAZAREZ':
        ime_tipa = ime_tipa_check(lside[0], lside[0].children)
        lista_init_deklaratora_check(lside[1], lside[1].children, ime_tipa.tip)

def lista_init_deklaratora_check(node, lside, ntip):
    if lside[0].data == '<init_deklarator>':
        init_deklarator_check(lside[0], lside[0].children, ntip)
    
    elif lside[0].data == '<lista_init_deklaratora>' and lside[1].data.split(' ')[0] == 'ZAREZ' and lside[2].data == '<init_deklarator>':
        lista_init_deklaratora_check(lside[0], lside[0].children, ntip)
        init_deklarator_check(lside[2], lside[2].children, ntip)

def init_deklarator_check(node, lside, ntip):   
    if len(lside) == 1 and lside[0].data == '<izravni_deklarator>':
        izravni_deklarator = izravni_deklarator_check(lside[0], lside[0].children, ntip)
        if isinstance(izravni_deklarator.tip,Function):
            tip = izravni_deklarator.tip.pov
        else:
            tip = izravni_deklarator.tip   
        if check_type_is(tip[0:5], "const") == True or check_type_is(tip[0:9], "niz(const") == True:
            print_err(node)
    
    elif lside[0].data == '<izravni_deklarator>' and lside[1].data.split(' ')[0] == 'OP_PRIDRUZI' and lside[2].data == '<inicijalizator>':
        izravni_deklarator = izravni_deklarator = izravni_deklarator_check(lside[0], lside[0].children, ntip)
        inicijalizator = inicijalizator_check(lside[2], lside[2].children)
        if isinstance(izravni_deklarator.tip,Function):
            br_elem = len(izravni_deklarator.tip.args)
        else:
            br_elem = izravni_deklarator.br_elem

        if izravni_deklarator.tip == ntip or izravni_deklarator.tip == f'const({ntip})':
            if check_cast_valid(inicijalizator.tip, ntip) == False:
                print_err(node)
        elif izravni_deklarator.tip == f'niz({ntip})' or izravni_deklarator.tip == f'niz(const({ntip}))':
            if inicijalizator.br_elem > br_elem:
                print_err(node)
            for tip in inicijalizator.tip:
                if check_cast_valid(tip, ntip) == False:
                    print_err(node)
        else:
            print_err(node)

def izravni_deklarator_check(node, lside, ntip):
    if len(lside) == 1 and lside[0].data.split(' ')[0] == 'IDN':
        if check_type_is(ntip, "void") == True:
            print_err(node)
        if check_variable_local(node, lside[0].data.split(' ')[2]) != None:
            print_err(node)
        save_variable(node, Variable(lside[0].data.split(' ')[2], ntip))
        return Response(ntip, None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'IDN' and lside[1].data.split(' ')[0] == 'L_UGL_ZAGRADA' and lside[2].data.split(' ')[0] == 'BROJ' and lside[3].data.split(' ')[0] == 'D_UGL_ZAGRADA':
        if check_type_is(ntip, "void") == True:
            print_err(node)
        if check_variable_local(node, lside[0].data.split(' ')[2]) != None:
            print_err(node)
        if int(lside[2].data.split(' ')[2]) <= 0 or int(lside[2].data.split(' ')[2]) > 1024:
            print_err(node)
        save_variable(node, Variable(lside[0].data.split(' ')[2], f'niz({ntip})'))
        return Response(f'niz({ntip})', None, 0, int(lside[2].data.split(' ')[2]))
    
    elif lside[0].data.split(' ')[0] == 'IDN' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data.split(' ')[0] == 'KR_VOID' and lside[3].data.split(' ')[0] == 'D_ZAGRADA':
        func = check_function_declared_local(node, lside[0].data.split(' ')[2])
        if func != []:
            if check_functions(func, "void", ntip) == False:
                print_err(node)
        else:
            save_function(node, Function(lside[0].data.split(' ')[2], ntip, 'void', 'dec'))
        return Response(Function(lside[0].data.split(' ')[2], ntip, 'void', 'dec'), None, 0, None)
    
    elif lside[0].data.split(' ')[0] == 'IDN' and lside[1].data.split(' ')[0] == 'L_ZAGRADA' and lside[2].data == '<lista_parametara>' and lside[3].data.split(' ')[0] == 'D_ZAGRADA':
        lista_parametara = lista_parametara_check(lside[2], lside[2].children)
        func = check_function_declared_local(node, lside[0].data.split(' ')[2])
        if func != []:
            if check_functions(func, lista_parametara.tip, ntip) == False:
                print_err(node)
        else:
            save_function(node, Function(lside[0].data.split(' ')[2], ntip, lista_parametara.tip, 'dec'))
        return Response(Function(lside[0].data.split(' ')[2], ntip, lista_parametara.tip, 'dec'), None, 0, None)

def inicijalizator_check(node, lside):
    if lside[0].data == '<izraz_pridruzivanja>':
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[0], lside[0].children)
        br_elem = inicijalizator_to_niz_znakova(node)
        if br_elem != None:
            list_el = []
            for i in range(0, br_elem):
                list_el.append('char')
            return Response(list_el, None, 0, br_elem)
        else:
            return Response(izraz_pridruzivanja.tip, None, 0, None) 

    elif lside[0].data.split(' ')[0] == 'L_VIT_ZAGRADA' and lside[1].data == '<lista_izraza_pridruzivanja>' and lside[2].data.split(' ')[0] == 'D_VIT_ZAGRADA':
        lista_izraza_pridruzivanja = lista_izraza_pridruzivanja_check(lside[1], lside[1].children)
        return Response(lista_izraza_pridruzivanja.tip, None, 0, lista_izraza_pridruzivanja.br_elem)
    
def lista_izraza_pridruzivanja_check(node, lside):
    if lside[0].data == '<izraz_pridruzivanja>':
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[0], lside[0].children)
        return Response([izraz_pridruzivanja.tip], None, 0, 1)

    elif lside[0].data == '<lista_izraza_pridruzivanja>' and lside[1].data.split(' ')[0] == 'ZAREZ' and lside[2].data == '<izraz_pridruzivanja>':
        lista_izraza_pridruzivanja = lista_izraza_pridruzivanja_check(lside[0], lside[0].children)
        izraz_pridruzivanja = izraz_pridruzivanja_check(lside[2], lside[2].children)
        return Response(lista_izraza_pridruzivanja.tip + [izraz_pridruzivanja.tip], None, 0, lista_izraza_pridruzivanja.br_elem + 1)

if __name__ == "__main__":
    head = read_input()
    prijevodna_jedinica_check(head, head.children)
    check_if_main_correct()
    check_if_all_functions_declared()