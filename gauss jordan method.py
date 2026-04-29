import re
import numpy as np


def parse_equations(equations, n):
    variables = [f"x{i + 1}" for i in range(n)]

    a = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)

    for i, equation in enumerate(equations):
        if "=" not in equation:
            raise ValueError(f"Equation {i + 1} is missing '='.")

        lhs, rhs = equation.split("=")
        b[i] = float(rhs.strip())

        lhs = lhs.replace(" ", "").replace("*", "")
        if not lhs.startswith(("+", "-")):
            lhs = "+" + lhs

        terms = re.findall(r"([+-])(\d*\.?\d*)([a-zA-Z]\w*)", lhs)
        for sign, number, variable in terms:
            if variable not in variables:
                raise ValueError(
                    f"Use only variables from {', '.join(variables)}."
                )
            coefficient = 1.0 if number == "" else float(number)
            if sign == "-":
                coefficient = -coefficient
            a[i, variables.index(variable)] += coefficient

    return a, b, variables


def gauss_jordan_method(a, b):
    n = len(b)
    augmented = np.hstack((a.astype(float), b.reshape(-1, 1)))

    for i in range(n):
        pivot_row = np.argmax(np.abs(augmented[i:, i])) + i
        if np.isclose(augmented[pivot_row, i], 0.0):
            raise ValueError("The system has no unique solution.")

        if pivot_row != i:
            augmented[[i, pivot_row]] = augmented[[pivot_row, i]]
            print(f"Swapped row {i + 1} with row {pivot_row + 1}")

        augmented[i, i:] = augmented[i, i:] / augmented[i, i]

        for j in range(n):
            if j == i:
                continue
            factor = augmented[j, i]
            augmented[j, i:] -= factor * augmented[i, i:]

    return augmented[:, :-1], augmented[:, -1]


def main():
    n = int(input("Enter the number of equations: "))

    print("\nEnter the equations one by one.")
    print("Use only variables in the form x1, x2, x3, ...")
    print("Example: 2x1 - 3x2 + x3 = 5")

    equations = []
    for i in range(n):
        equations.append(input(f"Equation {i + 1}: "))

    try:
        a, b, variables = parse_equations(equations, n)
        reduced_matrix, solution = gauss_jordan_method(a, b)
    except ValueError as error:
        print(f"\nError: {error}")
        return

    print(f"\nVariables in order: {', '.join(variables)}")
    print("\nReduced matrix:")
    print(np.round(reduced_matrix, 4))
    print("\nSolution:")
    for variable, value in zip(variables, solution):
        print(f"{variable} = {value:.4f}")


if __name__ == "__main__":
    main()
