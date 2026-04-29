import numpy as np
import re

def cramers_rule():
    print("--- Interactive Cramer's Rule Solver ---")
    
    # 1. User Input and Parsing
    try:
        n_input = input("Enter the number of equations (n): ")
        if not n_input.strip():
            return
        n = int(n_input)
    except ValueError:
        print("Error: Please enter a valid integer for the number of equations.")
        return
    
    print("\nEnter the equations one by one.")
    print("Example: 2x + 3y = 5")
    
    eq_strings = []
    for i in range(n):
        eq = input(f"Equation {i+1}: ")
        eq_strings.append(eq)
        
    # Find all unique variables
    var_set = set()
    for eq in eq_strings:
        lhs = eq.split('=')[0] if '=' in eq else eq
        vars_in_eq = re.findall(r'[a-zA-Z]\w*', lhs)
        var_set.update(vars_in_eq)
        
    variables = sorted(list(var_set))
    
    # Check if we have enough variables
    if len(variables) < n:
        print(f"Warning: Only detected {len(variables)} variables for {n} equations.")
    
    A = np.zeros((n, n))
    b = np.zeros(n)
    
    try:
        for i, eq in enumerate(eq_strings):
            if '=' not in eq:
                print(f"Error: Equation {i+1} is missing an '=' sign.")
                return
                
            lhs, rhs = eq.split('=')
            b[i] = float(rhs.strip())
            
            lhs = lhs.replace(' ', '').replace('*', '')
            if not lhs.startswith(('+', '-')):
                lhs = '+' + lhs 
                
            # Regex: (sign) (number) (variable)
            terms = re.findall(r'([+-])(\d*\.?\d*)([a-zA-Z]\w*)', lhs)
            
            for sign, num, var in terms:
                coeff = 1.0 if num == '' else float(num)
                if sign == '-':
                    coeff = -coeff
                    
                if var in variables:
                    j = variables.index(var)
                    if j < n: 
                        A[i, j] += coeff
    except Exception as e:
        print(f"Error parsing equations: {e}")
        return

    # 2. Cramer's Rule Calculations
    det_A = np.linalg.det(A)
    
    print("\n--- Coefficient Matrix (A) ---")
    print(A)
    print(f"\nMain Determinant (D) = {det_A:.4f}")
    
    if np.isclose(det_A, 0):
        print("Error: Determinant is zero. The system has no unique solution.")
        return

    results = {}
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b # Replace column i with constants b
        det_Ai = np.linalg.det(Ai)
        
        var_name = variables[i] if i < len(variables) else f"x{i+1}"
        results[var_name] = det_Ai / det_A
        print(f"D_{var_name} = {det_Ai:.4f}")

    # 3. Final Output
    print("\n--- Final Solution ---")
    for var, val in results.items():
        print(f"{var} = {val:.4f}")

# THIS PART IS CRITICAL: It tells Python to actually run the function
if __name__ == "__main__":
    cramers_rule()