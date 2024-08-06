from tabla import Tabla

def determinant(a_11: float,a_12: float,a_21: float,a_22: float) -> float:
    return (a_11 * a_22) - (a_12 * a_21)

def first_jury_condition(coefficients: list[float]) -> bool:
    return abs(coefficients[len(coefficients) - 1]) < coefficients[0]

def second_jury_condition(coefficients: list[float]) -> bool:
    p = 0
    for i,coefficient in enumerate(coefficients):
        p += coefficient * (1)**(len(coefficients) - 1 - i)
    return p > 0

def third_jury_condition(coefficients: list[float]) -> bool:
    p = 0
    for i,coefficient in enumerate(coefficients):
        p += coefficient * (-1)**(len(coefficients) - 1 - i)
    
    if (len(coefficients) - 1) % 2 == 0:
        return p >= 0
    else:
        return p <= 0

necessary_jury_condition = [first_jury_condition,second_jury_condition,third_jury_condition]

def evaluate_necessary_conditions(coefficients: list[float]) -> bool:
    conditions_satisfaction = []

    for i,function in enumerate(necessary_jury_condition):
        if function(coefficients):
            print(f"- Condicion necesaria {i + 1} se cumple")
            conditions_satisfaction.append(True)
        else:
            print(f"- Condicion necesaria {i + 1} no se cumple")
            conditions_satisfaction.append(False)

    for i,condition in enumerate(conditions_satisfaction):
        if not condition or i == 2 and condition == True:
            return condition

def new_coefficients(coefficients: list[float]) -> list[float]:
    new_coefficients = []
    for i in range(len(coefficients)-1):
        new_coefficients.append(determinant(coefficients[0],coefficients[len(coefficients) - 1 - i],coefficients[len(coefficients) - 1],coefficients[i]))
    return new_coefficients

def jury_criterion(coefficients: list[float]) -> Tabla:
    evaluate_necessary_conditions(coefficients)
    
    indices = []
    for i,_ in enumerate(coeficientes_iniciales):
        indices.append(f"Z^{i}")
    
    table = Tabla(indices)
    final_table = jury_table(coefficients[::-1],table)

    return final_table

def jury_table(coefficients: list[float], table: Tabla) -> list[float] | Tabla:
    table.agregar_fila(["{:.4f}".format(x) for x in coefficients])

    if table.obtener_filas() > 3:
        if abs(coefficients[0]) < abs(coefficients[len(coefficients) -1]) :
            print('\nInestable')
            print(f"|{coefficients[0]}| < |{coefficients[len(coefficients) -1]}|")
        else:
            print('\nEstable')
            print(f"|{coefficients[0]}| > |{coefficients[len(coefficients) -1]}|")

    if len(coefficients) == 3:
        return table
    
    table.agregar_fila(["{:.4f}".format(x) for x in coefficients[::-1]])

    return jury_table(new_coefficients(coefficients),table)

coeficientes_iniciales = [1 , 0 , 1.50 , 0.5 , 0.3125 , 0.125]
#coeficientes_iniciales = [1 , -0.6 ,-0.81 , 0.67 , -0.12]
#coeficientes_iniciales = [1 , -1.2 , 0.07 , 0.3 , -0.08]

tabla = jury_criterion(coeficientes_iniciales)
print(tabla)