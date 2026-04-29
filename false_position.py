import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg') # Or 'Qt5Agg' if you have PyQt installed

def plot_equation(equation_str, f, xl, xu, root):
    """Generates a 2D plot of the function and highlights the root."""
    print("\nGenerating plot...")
    
    # Determine a good plotting range (adding a 20% margin around the initial bracket)
    margin = abs(xu - xl) * 0.2
    # Ensure we don't end up with a zero-width range if xl == xu
    if margin == 0:
        margin = 1.0 
        
    x_min = min(xl, xu) - margin
    x_max = max(xl, xu) + margin
    x_vals = np.linspace(x_min, x_max, 400)
    
    # Evaluate the function for all x values safely using a list comprehension
    y_vals = [f(x) for x in x_vals]
    
    plt.figure(figsize=(8, 6))
    
    # Plot the main function
    plt.plot(x_vals, y_vals, label=f'f(x) = {equation_str}', color='blue')
    
    # Plot the x-axis (y=0) to see where the root crosses
    plt.axhline(0, color='black', linewidth=1.2)
    
    # Mark the initial boundary guesses
    plt.axvline(xl, color='gray', linestyle='--', alpha=0.7, label=f'Initial xl ({xl})')
    plt.axvline(xu, color='gray', linestyle='--', alpha=0.7, label=f'Initial xu ({xu})')
    
    # Mark the calculated root
    plt.plot(root, f(root), 'ro', markersize=8, label=f'Root: x ≈ {root:.4f}')
    
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('False Position Method: Root Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()

def false_position_method():
    print("--- Interactive False Position Method Solver ---")
    
    # 1. Input the equation as a string
    print("Enter your equation using 'x' (e.g., x**3 - x**2 - 2)")
    equation_str = input("f(x) = ")

    # Define a helper function to evaluate the user's string
    def f(x_val):
        # We allow 'x' and 'math' functions (like math.sin) for flexibility
        return eval(equation_str, {"x": x_val, "math": math})

    # 2. Get numerical parameters from the user
    try:
        xl = float(input("Enter lower guess (xl): "))
        xu = float(input("Enter upper guess (xu): "))
        es = float(input("Enter stopping error percentage (es%): "))
        max_iter = int(input("Enter maximum iterations: "))
    except Exception as e:
        print(f"Input Error: {e}")
        return

    # Store the initial boundaries for the plot later
    xl_initial = xl
    xu_initial = xu

    # 3. Initial Validity Check
    try:
        if f(xl) * f(xu) >= 0:
            print("Error: f(xl) and f(xu) must have opposite signs.")
            return
    except Exception as e:
        print(f"Error evaluating equation: {e}")
        return

    # 4. Initialization and Table Header
    xr = 0
    xr_old = 0
    print(f"\n{'Iter':<8} {'xl':<10} {'xu':<10} {'xr':<10} {'f(xr)':<12} {'ea %':<10}")
    print("-" * 65)

    # 5. Calculation Loop
    for i in range(1, max_iter + 1):
        xr_old = xr
        
        fl = f(xl)
        fu = f(xu)
        
        # False Position Formula
        xr = xu - (fu * (xl - xu)) / (fl - fu)
        fxr = f(xr)
        
        # Calculate Approximate Relative Error (ea)
        ea = 0
        if i > 1:
            ea = abs((xr - xr_old) / xr) * 100

        print(f"{i:<8} {xl:<10.4f} {xu:<10.4f} {xr:<10.4f} {fxr:<12.4f} {ea:<10.4f}")

        # Check for convergence
        if i > 1 and ea < es:
            print("-" * 65)
            print(f"Converged! Root: {xr:.6f} at {i} iterations.")
            plot_equation(equation_str, f, xl_initial, xu_initial, xr)
            return

        # Update bounds based on signs
        if fl * fxr < 0:
            xu = xr
        else:
            xl = xr

    print("-" * 65)
    print("Reached max iterations without meeting the error criteria.")
    # Plot it anyway to show where it stopped
    plot_equation(equation_str, f, xl_initial, xu_initial, xr)

if __name__ == "__main__":
    false_position_method()