import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')  # Or 'Qt5Agg' if you have PyQt installed


def plot_equation(equation_str, f, x0, x1, root):
    """Generates a 2D plot of the function and highlights the root."""
    print("\nGenerating plot...")

    # Determine a good plotting range based on the initial guesses and the root
    points = [x0, x1, root]
    span = max(points) - min(points)
    margin = span * 0.5
    if margin == 0:
        margin = 2.0

    x_min = min(points) - margin
    x_max = max(points) + margin
    x_vals = np.linspace(x_min, x_max, 400)

    # Evaluate the function for all x values safely using a list comprehension
    y_vals = [f(x) for x in x_vals]

    plt.figure(figsize=(8, 6))

    # Plot the main function
    plt.plot(x_vals, y_vals, label=f"f(x) = {equation_str}", color="blue")

    # Plot the x-axis (y=0) to see where the root crosses
    plt.axhline(0, color="black", linewidth=1.2)

    # Mark the initial guesses
    plt.axvline(x0, color="gray", linestyle="--", alpha=0.7, label=f"Initial Guess (x0 = {x0})")
    plt.axvline(x1, color="green", linestyle="--", alpha=0.7, label=f"Initial Guess (x1 = {x1})")

    # Mark the calculated root
    plt.plot(root, f(root), "ro", markersize=8, label=f"Root: x ~= {root:.4f}")

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Secant Method: Root Visualization")
    plt.legend()
    plt.grid(True)
    plt.show()


def secant_method():
    print("--- Interactive Secant Method Solver ---")

    # 1. Input the equation as a string
    print("Enter your equation using 'x' (e.g., x**3 - x**2 - 2)")
    equation_str = input("f(x)  = ")

    # Define helper function to evaluate the user's string
    def f(x_val):
        return eval(equation_str, {"x": x_val, "math": math})

    # 2. Get numerical parameters from the user
    try:
        x0 = float(input("Enter first initial guess (x0): "))
        x1 = float(input("Enter second initial guess (x1): "))
        es = float(input("Enter stopping error percentage (es%): "))
        max_iter = int(input("Enter maximum iterations: "))
    except Exception as e:
        print(f"Input Error: {e}")
        return

    x0_initial = x0
    x1_initial = x1
    xr = x1

    # 3. Initialization and Table Header
    print(f"\n{'Iter':<8} {'x(i-1)':<12} {'x(i)':<12} {'f(x(i-1))':<14} {'f(x(i))':<12} {'ea %':<10}")
    print("-" * 80)

    # 4. Calculation Loop
    for i in range(1, max_iter + 1):
        try:
            fx0 = f(x0)
            fx1 = f(x1)
        except Exception as e:
            print(f"Error evaluating equation: {e}")
            return

        denominator = fx1 - fx0
        if denominator == 0:
            print(f"f(x1) - f(x0) became zero at iteration {i}. Secant method fails.")
            return

        # Secant method formula
        xr = x1 - (fx1 * (x1 - x0) / denominator)

        # Calculate approximate relative error (ea)
        ea = 0
        if xr != 0:
            ea = abs((xr - x1) / xr) * 100

        print(f"{i:<8} {x0:<12.6f} {x1:<12.6f} {fx0:<14.6f} {fx1:<12.6f} {ea:<10.4f}")

        # Check for convergence
        if ea < es or f(xr) == 0:
            print("-" * 80)
            print(f"Converged! Root: {xr:.6f} at {i} iterations.")
            plot_equation(equation_str, f, x0_initial, x1_initial, xr)
            return

        x0, x1 = x1, xr

    print("-" * 80)
    print("Reached max iterations without meeting the error criteria.")
    plot_equation(equation_str, f, x0_initial, x1_initial, xr)


if __name__ == "__main__":
    secant_method()
