from z3 import *

def read_dimacs(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    cnf = []
    for line in lines:
        if line.startswith('c'):
            continue  # Skip comment lines
        if line.startswith('p'):
            _, _, num_vars, num_clauses = line.split()
            num_vars = int(num_vars)
            num_clauses = int(num_clauses)
            continue
        clause = [int(x) for x in line.split() if x != '0']
        cnf.append(clause)
    return num_vars, cnf

def solve_sat(filename):
    num_vars, cnf = read_dimacs(filename)
    vars = [Bool(f"L{i}") for i in range(1, num_vars+1)]
    s = Solver()
    for clause in cnf:
        s.add(Or([vars[abs(lit)-1] if lit > 0 else Not(vars[abs(lit)-1]) for lit in clause]))
    if s.check() == sat:
        model = s.model()
        solution = [model[var] for var in vars]
        return [var.decl() for var, val in zip(vars, solution) if is_true(val)]
    else:
        return None

# filename = 'output.cnf'
# solution = solve_sat(filename)
# if solution:
#     print("SAT solution found:")
#     print(solution)
# else:
#     print("No solution")
