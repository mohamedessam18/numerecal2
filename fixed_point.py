import math

def fixed_point_method():
    print("--- Interactive Fixed Point Iteration Solver ---")
    
    # 1. Input the equation as a string
    print("Enter your equation rearranged to x = g(x) (e.g., (x**3 - 2)**(1/2) or (x**2 + 2)/3)")
    print("Original equation example: x^3 - x^2 - 2 = 0")
    print("Rearranged to: x = (x^3 - 2)^(1/2) or x = (x^2 + 2)/x")
    gx_str = input("g(x) = ")
    
    # Define a helper function to evaluate the user's string
    def g(x_val):
        # We allow 'x' and 'math' functions (like math.sin) for flexibility
        return eval(gx_str, {"x": x_val, "math": math})

    # 2. Get numerical parameters from the user
    try:
        x0 = float(input("\nEnter initial guess (x0): "))
        es = float(input("Enter stopping error percentage (es%): "))
        max_iter = int(input("Enter maximum iterations: "))
    
    except Exception as e:
        print(f"Input Error: {e}")
        return

    # 3. Initialization and Table Header
    xr = x0
    xr_old = 0
    print(f"\n{'Iter':<8} {'x_old':<12} {'g(x_old)':<14} {'ea %':<12}")
    print("-" * 50)

    # 4. Calculation Loop
    for i in range(1, max_iter + 1):
        xr_old = xr
        
        # Fixed Point Iteration Formula
        try:
            xr = g(xr_old)
        except Exception as e:
            print(f"Error evaluating g(x) at iteration {i}: {e}")
            print("Make sure your equation is valid and doesn't cause domain errors")
            return
        
        # Calculate Approximate Relative Error (ea)
        if i > 1:
            if xr != 0:
                ea = abs((xr - xr_old) / xr) * 100
            else:
                ea = abs((xr - xr_old) / (xr + 1e-10)) * 100
        else:
            ea = 100 

        print(f"{i:<8} {xr_old:<12.6f} {xr:<14.6f} {ea:<12.4f}")

        # Check for convergence
        if i > 1 and ea < es:
            print("-" * 50)
            print(f"✓ Converged! Root: {xr:.8f} after {i} iterations.")
            print(f"  g({xr:.8f}) = {xr:.8f}")
            return

        # Check for divergence (optional but helpful)
        if i > 10 and ea > 1000:
            print("-" * 50)
            print(f"⚠ Method may be diverging! Error increased to {ea:.2f}%")
            print("  Try a different initial guess or rearrange g(x) differently.")
            return

    print("-" * 50)
    print(f"⚠ Reached max iterations ({max_iter}) without meeting the error criteria.")
    print(f"  Best approximation: x = {xr:.8f}")
    print(f"  g({xr:.8f}) = {g(xr):.8f}")

if __name__ == "__main__":
    fixed_point_method()
