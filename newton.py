import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') # Or 'Qt5Agg' if you have PyQt installed

def plot_equation(equation_str, f, x0, root):
    """Generates a 2D plot of the function and highlights the root."""
    print("\nGenerating plot...")
    
    # Determine a good plotting range based on the initial guess and the root
    margin = abs(x0 - root) * 0.5
    # Ensure we don't end up with a zero-width range if x0 is already the exact root
    if margin == 0:
        margin = 2.0 
        
    x_min = min(x0, root) - margin
    x_max = max(x0, root) + margin
    x_vals = np.linspace(x_min, x_max, 400)
    
    # Evaluate the function for all x values safely using a list comprehension
    y_vals = [f(x) for x in x_vals]
    
    plt.figure(figsize=(8, 6))
    
    # Plot the main function
    plt.plot(x_vals, y_vals, label=f'f(x) = {equation_str}', color='blue')
    
    # Plot the x-axis (y=0) to see where the root crosses
    plt.axhline(0, color='black', linewidth=1.2)
    
    # Mark the initial guess
    plt.axvline(x0, color='gray', linestyle='--', alpha=0.7, label=f'Initial Guess (x0 = {x0})')
    
    # Mark the calculated root
    plt.plot(root, f(root), 'ro', markersize=8, label=f'Root: x ≈ {root:.4f}')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Newton-Raphson Method: Root Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()

def newton_raphson_method():
    print("--- Interactive Newton-Raphson Method Solver ---")
    
    # 1. Input the equation and its derivative as strings
    print("Enter your equation using 'x' (e.g., x**3 - x**2 - 2)")
    equation_str = input("f(x)  = ")
    
    print("Enter the derivative of your equation (e.g., 3*x**2 - 2*x)")
    derivative_str = input("f'(x) = ")

    # Define helper functions to evaluate the user's strings
    def f(x_val):
        return eval(equation_str, {"x": x_val, "math": math})

    def df(x_val):
        return eval(derivative_str, {"x": x_val, "math": math})

    # 2. Get numerical parameters from the user
    try:
        x0 = float(input("Enter initial guess (x0): "))
        es = float(input("Enter stopping error percentage (es%): "))
        max_iter = int(input("Enter maximum iterations: "))
    except Exception as e:
        print(f"Input Error: {e}")
        return

    x0_initial = x0
    xr = x0

    # 3. Initialization and Table Header
    print(f"\n{'Iter':<8} {'xi':<12} {'f(xi)':<12} {'f(xi)':<12} {'ea %':<10}")
    print("-" * 65)

    # 4. Calculation Loop
    for i in range(1, max_iter + 1):
        xr_old = xr
        
        try:
            fx = f(xr_old)
            dfx = df(xr_old)
        except Exception as e:
            print(f"Error evaluating equation: {e}")
            return
            
        # Check for division by zero
        if dfx == 0:
            print(f"Derivative is zero at x = {xr_old}. Newton-Raphson fails.")
            return

        # Newton-Raphson Formula
        xr = xr_old - (fx / dfx)
        
        # Calculate Approximate Relative Error (ea)
        ea = 0
        if xr != 0:
            ea = abs((xr - xr_old) / xr) * 100

        print(f"{i:<8} {xr_old:<12.6f} {fx:<12.6f} {dfx:<12.6f} {ea:<10.4f}")

        # Check for convergence
        if ea < es:
            print("-" * 65)
            print(f"Converged! Root: {xr:.6f} at {i} iterations.")
            plot_equation(equation_str, f, x0_initial, xr)
            return

    print("-" * 65)
    print("Reached max iterations without meeting the error criteria.")
    # Plot it anyway to show where it stopped
    plot_equation(equation_str, f, x0_initial, xr)

if __name__ == "__main__":
    newton_raphson_method()