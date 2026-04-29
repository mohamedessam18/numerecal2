import numpy as np
import re

def lu_decomposition_pivoting():
    # 1. User Input
    n = int(input("Enter the number of equations (n): "))
    
    print("\nEnter the equations one by one.")
    print("Example format: 2x - 3.5y + z = 5 (keep variables on the left, constants on the right)")
    
    eq_strings = []
    for i in range(n):
        eq = input(f"Equation {i+1}: ")
        eq_strings.append(eq)
        
    # Parse equations to find all unique variables
    var_set = set()
    for eq in eq_strings:
        # Look only at the Left Hand Side (LHS) for variables
        lhs = eq.split('=')[0] if '=' in eq else eq
        vars_in_eq = re.findall(r'[a-zA-Z]\w*', lhs)
        var_set.update(vars_in_eq)
        
    # Sort alphabetically so columns are consistent (e.g., x, y, z)
    variables = sorted(list(var_set))
    
    A = np.zeros((n, n))
    b = np.zeros(n)
    
    for i, eq in enumerate(eq_strings):
        if '=' not in eq:
            print(f"Error: Equation {i+1} is missing an '=' sign.")
            return
            
        lhs, rhs = eq.split('=')
        
        # Get the constant (b) from the Right Hand Side (RHS)
        b[i] = float(rhs.strip())
        
        # Clean up LHS for parsing (remove spaces and optional asterisks)
        lhs = lhs.replace(' ', '').replace('*', '')
        if not lhs.startswith(('+', '-')):
            lhs = '+' + lhs # Add leading plus for easier parsing
            
        # Regex extracts: (sign) (number) (variable)
        terms = re.findall(r'([+-])(\d*\.?\d*)([a-zA-Z]\w*)', lhs)
        
        for sign, num, var in terms:
            # If there's no number (e.g., "+x"), the coefficient is 1.0
            coeff = 1.0 if num == '' else float(num)
            if sign == '-':
                coeff = -coeff
                
            if var in variables:
                j = variables.index(var)
                if j < n: # Prevent out-of-bounds if they entered too many unique variables
                    A[i, j] += coeff

    print(f"\nDetected variables in order: {', '.join(variables[:n])}")

    # Initialize L, U, and P
    L = np.zeros((n, n))
    U = A.copy()
    P = np.eye(n) # Identity matrix for permutations

    # 2. Decomposition Process
    for i in range(n):
        # --- Partial Pivoting ---
        # Find the index of the largest element in current column i
        pivot_row = np.argmax(np.abs(U[i:n, i])) + i
        
        # Swap rows in U, P, and L (up to column i)
        if pivot_row != i:
            U[[i, pivot_row]] = U[[pivot_row, i]]
            P[[i, pivot_row]] = P[[pivot_row, i]]
            if i > 0:
                L[[i, pivot_row], :i] = L[[pivot_row, i], :i]
            print(f"Swapped row {i+1} with row {pivot_row+1}")

        # --- Elimination ---
        L[i, i] = 1 # Diagonal of L is 1s
        for j in range(i + 1, n):
            # Avoid division by zero if U[i, i] is exactly 0
            if U[i, i] == 0:
                continue
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]

    # 3. Solving the system PAx = Pb -> LUx = Pb
    # Let Ly = Pb (Forward substitution)
    Pb = np.dot(P, b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = Pb[i] - np.dot(L[i, :i], y[:i])

    # Let Ux = y (Backward substitution)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

    # --- Results ---
    print("\n--- Upper Triangular Matrix (U) ---")
    print(np.round(U, 4))
    print("\n--- Lower Triangular Matrix (L) ---")
    print(np.round(L, 4))
    print("\n--- Permutation Matrix (P) ---")
    print(P)
    
    print("\n--- Solution ---")
    for i in range(n):
        # Dynamically use the detected variable names in the output
        var_name = variables[i] if i < len(variables) else f"x{i+1}"
        print(f"{var_name} = {x[i]:.4f}")

if __name__ == "__main__":
    lu_decomposition_pivoting()
    