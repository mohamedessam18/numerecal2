import math
import matplotlib.pyplot as plt
import numpy as np


def plot_bisection(equation_str, f, xl, xu, root):
    """Generates a 2D plot of the function and highlights the bisection root."""
    print("\nGenerating plot...")

    if root is None:
        print("No root available to plot.")
        return

    # Determine plotting range
    margin = max(abs(xu - xl) * 0.2, 1e-3)
    x_min = min(xl, xu) - margin
    x_max = max(xl, xu) + margin
    x_vals = np.linspace(x_min, x_max, 400)

    try:
        y_vals = [f(x) for x in x_vals]
    except Exception as e:
        print(f"Plotting Error: {e}")
        return

    plt.figure(figsize=(9, 6))

    # Plot function
    plt.plot(x_vals, y_vals, label=f'f(x) = {equation_str}', linewidth=2)

    # X-axis
    plt.axhline(0, linewidth=1.2)

    # Bracket lines
    plt.axvline(xl, linestyle='--', alpha=0.7, label=f'xl: {xl:.4f}')
    plt.axvline(xu, linestyle='--', alpha=0.7, label=f'xu: {xu:.4f}')

    # Root point
    root_y = f(root)
    plt.plot(root, root_y, 'o', markersize=8, label=f'Root ≈ {root:.6f}')

    # Formatting
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title('Bisection Method Visualization')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()


def bisection_method():
    print("--- Interactive Bisection Method Solver ---")

    # Input equation
    print("Enter your equation using 'x' (e.g., x**3 - x**2 - 2)")
    equation_str = input("f(x) = ")

    # Safe evaluation function
    def f(x_val):
        allowed_names = {
            "x": x_val,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "exp": math.exp,
            "log": math.log,
            "sqrt": math.sqrt,
            "pi": math.pi,
            "e": math.e
        }
        return eval(equation_str, {"__builtins__": {}}, allowed_names)

    # Inputs
    try:
        xl = float(input("Enter lower guess (xl): "))
        xu = float(input("Enter upper guess (xu): "))
        es = float(input("Enter stopping error percentage (es%): "))
        max_iter = int(input("Enter maximum iterations: "))
    except Exception as e:
        print(f"Input Error: {e}")
        return

    # Initial validation
    try:
        if f(xl) * f(xu) >= 0:
            print("Error: f(xl) and f(xu) must have opposite signs.")
            return
    except Exception as e:
        print(f"Equation Error: {e}")
        return

    # Initialization
    xr = None
    xr_old = None

    print(f"\n{'Iter':<6} {'xl':<12} {'xu':<12} {'xr':<12} {'f(xr)':<14} {'ea (%)':<10}")
    print("-" * 70)

    for i in range(1, max_iter + 1):
        xr_old = xr
        xr = (xl + xu) / 2.0

        try:
            fl = f(xl)
            fxr = f(xr)
        except Exception as e:
            print(f"Evaluation Error: {e}")
            return

        # Error calculation
        ea = None
        if xr_old is not None and xr != 0:
            ea = abs((xr - xr_old) / xr) * 100

        # Print row
        print(f"{i:<6} {xl:<12.6f} {xu:<12.6f} {xr:<12.6f} {fxr:<14.6f} {ea if ea else 0:<10.6f}")

        # Convergence check
        if ea is not None and ea < es:
            print("-" * 70)
            print(f"Converged: Root ≈ {xr:.6f} after {i} iterations")
            plot_bisection(equation_str, f, xl, xu, xr)
            return

        # Root check (numerical tolerance)
        if abs(fxr) < 1e-10:
            print("-" * 70)
            print(f"Exact root found: {xr:.6f}")
            plot_bisection(equation_str, f, xl, xu, xr)
            return

        # Update bounds
        if fl * fxr < 0:
            xu = xr
        else:
            xl = xr

    print("-" * 70)
    print("Max iterations reached without full convergence.")
    plot_bisection(equation_str, f, xl, xu, xr)


if __name__ == "__main__":
    bisection_method()