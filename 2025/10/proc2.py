from scipy.optimize import linprog

test_lines = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
expected_test_result = 33

# (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

# a (3)
# b (1,3)
# c (2)
# d (2,3)
# e (0,2)
# f (0,1)
# ---{3,5,4,7}

# a [0, 0, 0, 1]
# b [0, 1, 0, 1]
# c [0, 0, 1, 0]
# d [0, 0, 1, 1]
# e [1, 0, 1, 0]
# f [1, 1, 0, 0]
# --[3, 5, 4, 7]

# 0*a + 0*b + 0*c + 0*d + 1*e + 1*f = 3
# 0*a + 1*b + 0*c + 0*d + 0*e + 1*f = 5
# 0*a + 0*b + 1*c + 1*d + 1*e + 0*f = 4
# 1*a + 1*b + 0*c + 1*d + 0*e + 0*f = 7

# programación lineal!


def parse(line):
    _, *raw_buttons, raw_joltages = line.split()

    assert raw_joltages[0] == "{" and raw_joltages[-1] == "}"
    raw_joltages = raw_joltages[1:-1]
    joltages = [int(x) for x in raw_joltages.split(",")]
    joltages_width = len(joltages)

    buttons = []
    for raw_button in raw_buttons:
        assert raw_button[0] == "(" and raw_button[-1] == ")"
        raw_button = raw_button[1:-1]
        butraw_digs = {int(x) for x in raw_button.split(",")}
        button = ["1" if x in butraw_digs else "0" for x in range(joltages_width)]
        buttons.append(button)

    return buttons, joltages


def process(line):
    buttons, joltages = parse(line)
    print("\n\n========== btu", buttons)
    print("========= jt", joltages)

    # Coeficientes de la función objetivo: minimizar a + b + c + d + e + f
    c = [1] * len(buttons)

    # Matriz de restricciones de igualdad: M * x = r
    A_eq = list(zip(*buttons))
    b_eq = joltages

    # Límites: todas las variables >= 0
    bounds = [(0, None) for _ in range(len(buttons))]  # (0, infinito)

    # Resolver el problema de programación lineal
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')
    print("======= result", result.x, result.fun)

    # validate it was ok and that elements are integer
    assert result.success
    for value in result.x:
        assert value.is_integer()
    assert result.fun.is_integer()
    return int(result.fun)


def run(lines):
    total = 0
    for line in lines:
        pushes = process(line)
        total += pushes
    return total
