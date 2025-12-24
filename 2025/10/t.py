import pulp
import numpy as np

def solve_min_sum_pulp(A_rows, b_eq):
    """Solve a system A*x = b with x >= 0 integers, minimizing sum(x)."""
    A = np.array(A_rows)
    b_eq = np.array(b_eq, dtype=int)
    A_m, A_n = A.shape
    var_names = [f'x{i}' for i in range(A_n)]

    # the problem itself
    prob = pulp.LpProblem("Maximize sum", pulp.LpMinimize)

    # create non-negative integer variables
    variables = []
    for name in var_names:
        variables.append(pulp.LpVariable(name, lowBound=0, cat='Integer'))

    # target function: minimize the sum of all variables
    prob += pulp.lpSum(variables)

    # the equality restrictions
    for eq_line_idx in range(A_m):
        # build linear expression: A[i,0]*x0 + A[i,1]*x1 + ... = result
        sum_expression = [value * variable for value, variable in zip(A[eq_line_idx], variables)]
        line_result = b_eq[eq_line_idx]

        # feed into the problem
        prob += pulp.lpSum(sum_expression) == line_result

    # solve it!
    prob.solve()

    # Extraer resultados
    solution = 0
    f
    solution = sum(var.varValue for var in variables)
    solution = sum(var.varValue for var in variables)
    breakpoint()

    # Convertir a array numpy

    return {
        'problem': prob,
        'variables': variables,
        'solution_dict': solution,
        'solution_array': sol_array,
        'sum': sum(sol_array),
        'status': pulp.LpStatus[prob.status]
    }

A_rows = [
    (0, 0, 0, 0, 1, 1),
    (0, 1, 0, 0, 0, 1),
    (0, 0, 1, 1, 1, 0),
    (1, 1, 0, 1, 0, 0)
]
b_eq = [3, 5, 4, 7]
result = solve_min_sum_pulp(A_rows, b_eq)

print(f"Estado: {result['status']}")
print("\nSolución óptima:")
for name, val in result['solution_dict'].items():
    print(f"{name} = {val}")

print(f"\nSuma mínima = {result['sum']}")
