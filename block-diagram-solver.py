from sympy import Symbol, solve, simplify, sympify, pprint

class Block:
    def __init__(self, function: str, is_defined: bool, input: str, output: str):
        self.function = function
        self.is_defined = is_defined
        self.input = input
        self.output = output
    
    def get_equation(self):
        function = sympify(self.function) if self.is_defined else Symbol(self.function)
        return Symbol(self.output) - Symbol(self.input) * function

    def get_unknown_symbols(self) -> tuple[Symbol]:
        return Symbol(self.input),Symbol(self.output)

class SumPoint:
    def __init__(self, inputs: list[tuple[str]], output: str):
        self.inputs = inputs
        self.output = output

    def __get_input_symbol(self, input_symbol: tuple[str]):
        return Symbol(input_symbol[1]) if input_symbol[0] == '+' else Symbol(input_symbol[1]) * -1

    def get_equation(self):
        total_input = 0
        for input_item in self.inputs:
            total_input += self.__get_input_symbol(input_item)
        return Symbol(self.output) - total_input
    
    def get_unknown_symbols(self) -> tuple[Symbol]:
        return tuple(Symbol(input_item[1]) for input_item in self.inputs)

def flatten_list(list: list[list]) -> list:
    return [item for sublist in list for item in sublist]

def get_equations_list(sum_point_list: list[SumPoint], block_list: list[Block]) -> list:
    equations: list = []
    equations.append([sum_point.get_equation() for sum_point in sum_point_list])
    equations.append([block.get_equation() for block in block_list])    
    return flatten_list(equations)

def get_unknowns_list(sum_point_list: list[SumPoint], block_list: list[Block]) -> set:
    unknowns: set = set()
    unknowns.update(flatten_list([block.get_unknown_symbols() for block in block_list]))
    unknowns.update(flatten_list([sum_point.get_unknown_symbols() for sum_point in sum_point_list]))
    unknowns.remove(Symbol('R'))
    return unknowns

def simplify_block_diagram(sum_point_list: list[SumPoint], block_list: list[Block]):
    equations = get_equations_list(sum_point_list,block_list)
    unknowns = get_unknowns_list(sum_point_list,block_list)

    #Solve equation system for all unknows
    solutions = solve(equations,tuple(unknowns))
    
    #Get the solution for the value of Y (the output of the block diagram)
    y_solution = solutions[Symbol('Y')]

    #Divide the y function by R to get the value of M
    M = y_solution / Symbol('R')
    
    pprint(simplify(M))

def main():
    s = Symbol('s')
    
    G1 = Block('G_1',False,'V6','V5')
    G2 = Block('G_2',False,'V1','V2')
    G3 = Block('G_3',False,'V2','V3')
    G4 = Block('G_4',False,'V2','V4')
    G5 = Block('G_5',False,'V6','Y')

    SP1 = SumPoint([['+','R'],['+','V5'],['-','V3']],'V1')
    SP2 = SumPoint([['+','V4'],['+','V2'],['-','Y']],'V6')
    
    block_list = [G1,G2,G3,G4,G5]
    sum_point_list = [SP1,SP2]

    simplify_block_diagram(sum_point_list,block_list)

if __name__ == '__main__':
    main()


"""
from sympy import Symbol, solve, simplify, sympify, pprint
from math import e,cos,sin,sqrt,radians,pow,atan,degrees

a0 = 64
a1 = 6
t = 1
omega = sqrt(a0-(a1/2)**2)

a = 1 / a0

b = 1 - e**(-(a1/2)*t)

c = cos(radians(omega * t)) + ((a1/2)/omega) * sin(radians(omega*t))
#print(a )
#print(b)
#print(c)
#print(a*b*c*(64/3))

wn = 8
lamda = 0.375
w = 7,4162

uno = 1 - ((pow(e,-lamda*wn*t))/sqrt(1-lamda**2))
a = uno 
theta = atan((sqrt(1-lamda**2)/lamda))
tres = sin(radians(wn * sqrt(1-lamda**2) * t + theta))

print(tres)

print(uno*tres)
"""