import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
matplotlib.use('TkAgg')
import re

# --- Custom Animated Button ---
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.hoverBackground = kw.get("activebackground", "#45a049")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = self.hoverBackground

    def on_leave(self, e):
        self["background"] = self.defaultBackground

# --- Main Application ---
class NumericalSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Methods Root Finder Pro")
        self.root.geometry("950x650")
        self.root.minsize(800, 600)
        self.root.configure(bg="#2c3e50") # Dark main background

        # Variables
        self.method_var = tk.StringVar(value="Bisection")
        self.eq_var = tk.StringVar()
        self.df_var = tk.StringVar()  # For Newton
        self.val1_var = tk.StringVar() # xl, x0, or xi-1
        self.val2_var = tk.StringVar() # xu, or xi
        self.system_size_var = tk.StringVar(value="2")
        self.es_var = tk.StringVar(value="0.01")
        self.iter_var = tk.StringVar(value="50")
        self.eq_text = None
        
        # Store animation reference to prevent garbage collection
        self.current_animation = None

        self.setup_ui()
        self.update_input_fields()

    def setup_ui(self):
        # Main Layout Frames with Colors
        left_frame = tk.Frame(self.root, bg="#ecf0f1", padx=15, pady=15, bd=2, relief=tk.FLAT)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=10, pady=10)
        
        right_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Style configuration for ttk elements
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#ecf0f1", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 11, "bold"), foreground="#2980b9")
        style.configure("TCombobox", padding=5)

        # --- LEFT FRAME (Inputs) ---
        ttk.Label(left_frame, text="1. Select Method:", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))
        methods = [
            "Bisection",
            "Fixed Point",
            "False Position",
            "Newton-Raphson",
            "Secant",
            "Gauss Elimination",
            "Gauss-Jordan",
            "Cramer-Rule",
            "LU-Decomposition",
        ]
        self.method_cb = ttk.Combobox(left_frame, textvariable=self.method_var, values=methods, state="readonly", width=25)
        self.method_cb.pack(anchor=tk.W, pady=(0, 15))
        self.method_cb.bind("<<ComboboxSelected>>", self.update_input_fields)

        # Dynamic Input Frame
        self.dynamic_frame = tk.Frame(left_frame, bg="#ecf0f1")
        self.dynamic_frame.pack(fill=tk.X, pady=5)

        # Stopping Criteria
        self.criteria_label = ttk.Label(left_frame, text="3. Stopping Criteria:", style="Header.TLabel")
        self.criteria_label.pack(anchor=tk.W, pady=(15, 5))

        self.crit_frame = tk.Frame(left_frame, bg="#ecf0f1")
        self.crit_frame.pack(fill=tk.X)
        ttk.Label(self.crit_frame, text="Error (es %):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.crit_frame, textvariable=self.es_var, width=12).grid(row=0, column=1, sticky=tk.W, pady=2, padx=5)

        ttk.Label(self.crit_frame, text="Max Iterations:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(self.crit_frame, textvariable=self.iter_var, width=12).grid(row=1, column=1, sticky=tk.W, pady=2, padx=5)

        # Animated Solve Button (Green)
        self.solve_btn = HoverButton(left_frame, text="Solve & Plot", command=self.solve, 
                                     font=("Segoe UI", 12, "bold"), bg="#27ae60", fg="white", 
                                     activebackground="#1e8449", activeforeground="white",
                                     relief=tk.FLAT, pady=8, cursor="hand2")
        self.solve_btn.pack(fill=tk.X, pady=25)

        self.clear_inputs_btn = HoverButton(
            left_frame,
            text="Clear Inputs",
            command=self.clear_input_fields,
            font=("Segoe UI", 11, "bold"),
            bg="#c0392b",
            fg="white",
            activebackground="#922b21",
            activeforeground="white",
            relief=tk.FLAT,
            pady=8,
            cursor="hand2",
        )
        self.clear_inputs_btn.pack(fill=tk.X, pady=(0, 15))

        # --- RIGHT FRAME (Outputs) ---
        output_header = tk.Frame(right_frame, bg="#2c3e50")
        output_header.pack(fill=tk.X, pady=(0, 5))

        output_lbl = tk.Label(output_header, text="Iteration Output Engine", font=("Segoe UI", 12, "bold"), bg="#2c3e50", fg="white")
        output_lbl.pack(side=tk.LEFT)

        self.clear_output_btn = HoverButton(
            output_header,
            text="Clear Output",
            command=self.clear_output,
            font=("Segoe UI", 10, "bold"),
            bg="#8e44ad",
            fg="white",
            activebackground="#6c3483",
            activeforeground="white",
            relief=tk.FLAT,
            padx=10,
            pady=4,
            cursor="hand2",
        )
        self.clear_output_btn.pack(side=tk.RIGHT)
        
        # Styled Terminal Output
        self.output_text = scrolledtext.ScrolledText(
            right_frame,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white",
            bd=0,
            padx=10,
            pady=10,
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def update_input_fields(self, event=None):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        method = self.method_var.get()
        is_linear_method = self.is_linear_system_method(method)
        self.eq_text = None
        ttk.Label(self.dynamic_frame, text="2. Input Parameters:", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 5))

        if is_linear_method:
            self.solve_btn.config(text="Solve")
            self.criteria_label.pack_forget()
            self.crit_frame.pack_forget()
        else:
            self.solve_btn.config(text="Solve & Plot")
            if not self.criteria_label.winfo_manager():
                self.criteria_label.pack(anchor=tk.W, pady=(15, 5), before=self.solve_btn)
            if not self.crit_frame.winfo_manager():
                self.crit_frame.pack(fill=tk.X, before=self.solve_btn)

        def create_power_buttons(parent, entry_widget):
            btn_frame = tk.Frame(parent, bg="#ecf0f1")
            btn_frame.pack(fill=tk.X, pady=(2, 10))
            ttk.Label(btn_frame, text="Powers:").pack(side=tk.LEFT, padx=(0, 5))
            for p in ["*x**2", "*x**3", "*x**4","*x**5"]:
                HoverButton(btn_frame, text=f"x{p[-1]}", width=4, bg="#bdc3c7", activebackground="#95a5a6",
                            relief=tk.FLAT, cursor="hand2",
                            command=lambda p=p: self.insert_text(entry_widget, p)).pack(side=tk.LEFT, padx=2)

        if method in ["Bisection", "False Position"]:
            ttk.Label(self.dynamic_frame, text="f(x) =").pack(anchor=tk.W)
            eq_entry = ttk.Entry(self.dynamic_frame, textvariable=self.eq_var, width=32)
            eq_entry.pack(anchor=tk.W)
            create_power_buttons(self.dynamic_frame, eq_entry)

            ttk.Label(self.dynamic_frame, text="Lower Guess (xl):").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.val1_var, width=15).pack(anchor=tk.W, pady=(0, 5))
            
            ttk.Label(self.dynamic_frame, text="Upper Guess (xu):").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.val2_var, width=15).pack(anchor=tk.W)

        elif method == "Fixed Point":
            ttk.Label(self.dynamic_frame, text="g(x) =  (Rearranged from f(x)=0)").pack(anchor=tk.W)
            eq_entry = ttk.Entry(self.dynamic_frame, textvariable=self.eq_var, width=32)
            eq_entry.pack(anchor=tk.W)
            create_power_buttons(self.dynamic_frame, eq_entry)

            ttk.Label(self.dynamic_frame, text="Initial Guess (x0):").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.val1_var, width=15).pack(anchor=tk.W)

        elif method == "Newton-Raphson":
            ttk.Label(self.dynamic_frame, text="f(x) =").pack(anchor=tk.W)
            eq_entry = ttk.Entry(self.dynamic_frame, textvariable=self.eq_var, width=32)
            eq_entry.pack(anchor=tk.W)
            create_power_buttons(self.dynamic_frame, eq_entry)

            ttk.Label(self.dynamic_frame, text="f'(x) = (Derivative)").pack(anchor=tk.W)
            df_entry = ttk.Entry(self.dynamic_frame, textvariable=self.df_var, width=32)
            df_entry.pack(anchor=tk.W, pady=(0, 10))

            ttk.Label(self.dynamic_frame, text="Initial Guess (x0):").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.val1_var, width=15).pack(anchor=tk.W)

        elif method == "Secant":
            ttk.Label(self.dynamic_frame, text="f(x) =").pack(anchor=tk.W)
            eq_entry = ttk.Entry(self.dynamic_frame, textvariable=self.eq_var, width=32)
            eq_entry.pack(anchor=tk.W)
            create_power_buttons(self.dynamic_frame, eq_entry)

            ttk.Label(self.dynamic_frame, text="Guess 1 (xi-1):").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.val1_var, width=15).pack(anchor=tk.W, pady=(0, 5))
            
            ttk.Label(self.dynamic_frame, text="Guess 2 (xi):").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.val2_var, width=15).pack(anchor=tk.W)

        elif is_linear_method:
            ttk.Label(self.dynamic_frame, text="Number of Equations:").pack(anchor=tk.W)
            ttk.Entry(self.dynamic_frame, textvariable=self.system_size_var, width=15).pack(anchor=tk.W, pady=(0, 8))
            ttk.Label(
                self.dynamic_frame,
                text="Enter one equation per line using x1, x2, x3, ...\nExample: 2x1 - 3x2 + x3 = 5"
            ).pack(anchor=tk.W)
            self.eq_text = scrolledtext.ScrolledText(self.dynamic_frame, height=6)
            self.eq_text.pack(fill=tk.X, pady=(5, 0))

    def is_linear_system_method(self, method=None):
        if method is None:
            method = self.method_var.get()
        return method in {"Gauss Elimination", "Gauss-Jordan", "Cramer-Rule", "LU-Decomposition"}

    def insert_text(self, widget, text):
        widget.insert(tk.INSERT, text)
        widget.focus()

    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def safe_eval(self, eq_str, x_val):
        allowed_names = {
            "x": x_val, "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
            "pi": math.pi, "e": math.e, "math": math
        }
        return eval(eq_str, {"__builtins__": {}}, allowed_names)

    def parse_linear_system(self, equations, n):
        cleaned_equations = [eq.strip() for eq in equations if eq.strip()]
        if len(cleaned_equations) != n:
            raise ValueError(f"Expected {n} equations, but received {len(cleaned_equations)}.")

        variables = [f"x{i + 1}" for i in range(n)]
        coeff_pattern = re.compile(r"([+-])(\d*\.?\d*)(x\d+)")

        A = np.zeros((n, n), dtype=float)
        b = np.zeros(n, dtype=float)

        for i, equation in enumerate(cleaned_equations):
            if "=" not in equation:
                raise ValueError(f"Equation {i + 1} is missing '='.")

            lhs, rhs = equation.split("=", 1)
            b[i] = float(rhs.strip())

            lhs = lhs.replace(" ", "").replace("*", "")
            if not lhs.startswith(("+", "-")):
                lhs = "+" + lhs

            position = 0
            found_term = False
            for match in coeff_pattern.finditer(lhs):
                if match.start() != position:
                    raise ValueError(f"Could not parse equation {i + 1}. Use terms like 2x1 - 3x2 + x3.")

                sign, number, variable = match.groups()
                if variable not in variables:
                    raise ValueError(f"Use only variables from {', '.join(variables)}.")

                coefficient = 1.0 if number == "" else float(number)
                if sign == "-":
                    coefficient *= -1

                A[i, variables.index(variable)] += coefficient
                position = match.end()
                found_term = True

            if not found_term or position != len(lhs):
                raise ValueError(f"Could not parse equation {i + 1}. Use terms like 2x1 - 3x2 + x3.")

        return A, b, variables

    def format_matrix(self, matrix):
        return np.array2string(np.round(matrix, 6), precision=6, suppress_small=True)

    def clear_input_fields(self):
        self.eq_var.set("")
        self.df_var.set("")
        self.val1_var.set("")
        self.val2_var.set("")
        self.system_size_var.set("2")
        self.es_var.set("0.01")
        self.iter_var.set("50")

        self.update_input_fields()

        if self.eq_text is not None:
            self.eq_text.delete("1.0", tk.END)

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

    def solve(self):
        self.output_text.delete(1.0, tk.END)
        method = self.method_var.get()

        try:
            if self.is_linear_system_method(method):
                n = int(self.system_size_var.get())
                if n <= 0:
                    raise ValueError("Number of equations must be a positive integer.")

                equations = self.eq_text.get("1.0", tk.END).splitlines() if self.eq_text else []
                A, b, variables = self.parse_linear_system(equations, n)

                self.log(f"--- Solving using {method} ---")
                self.log(f"Variables order: {', '.join(variables)}")
                self.log("Coefficient Matrix A:")
                self.log(self.format_matrix(A))
                self.log("Constants Vector b:")
                self.log(self.format_matrix(b))
                self.log("")

                if method == "Gauss Elimination":
                    self.run_gauss_elimination(A, b, variables)
                elif method == "Gauss-Jordan":
                    self.run_gauss_jordan(A, b, variables)
                elif method == "Cramer-Rule":
                    self.run_cramers(A, b, variables)
                elif method == "LU-Decomposition":
                    self.run_lu_pivot(A, b, variables)
                return

            eq_str = self.eq_var.get().replace("^", "**")
            if not eq_str:
                messagebox.showerror("Input Error", "Equation field cannot be empty.")
                return

            es = float(self.es_var.get())
            max_iter = int(self.iter_var.get())
            val1 = float(self.val1_var.get())
            val2 = float(self.val2_var.get()) if self.val2_var.get() else 0.0
            f = lambda x: self.safe_eval(eq_str, x)

            self.log(f"--- Solving using {method} ---")
            self.log(f"Equation: {eq_str}\n")

            if method == "Bisection":
                self.run_bisection(f, eq_str, val1, val2, es, max_iter)
            elif method == "Fixed Point":
                self.run_fixed_point(f, eq_str, val1, es, max_iter)
            elif method == "False Position":
                self.run_false_position(f, eq_str, val1, val2, es, max_iter)
            elif method == "Newton-Raphson":
                df_str = self.df_var.get().replace("^", "**")
                df = lambda x: self.safe_eval(df_str, x)
                self.run_newton(f, df, eq_str, val1, es, max_iter)
            elif method == "Secant":
                self.run_secant(f, eq_str, val1, val2, es, max_iter)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            self.log(f"\nCRITICAL ERROR:\n{str(e)}\nCheck equation syntax (e.g., use 2*x instead of 2x).")

    # ================= MATH METHODS =================
    # (Math logic remains exactly as you wrote it)
    
    def run_bisection(self, f, eq_str, xl, xu, es, max_iter):
        if f(xl) * f(xu) >= 0:
            self.log("Error: f(xl) and f(xu) must have opposite signs.")
            return

        self.log(f"{'Iter':<6} {'xl':<12} {'xu':<12} {'xr':<12} {'f(xr)':<14} {'ea (%)':<10}")
        self.log("-" * 70)

        xr, xr_old = None, None
        for i in range(1, max_iter + 1):
            xr_old = xr
            xr = (xl + xu) / 2.0
            fl, fxr = f(xl), f(xr)

            ea = abs((xr - xr_old) / xr) * 100 if (xr_old is not None and xr != 0) else 0
            self.log(f"{i:<6} {xl:<12.6f} {xu:<12.6f} {xr:<12.6f} {fxr:<14.6f} {ea:<10.6f}")

            if ea != 0 and ea < es:
                self.log("-" * 70)
                self.log(f"Converged: Root ≈ {xr:.6f} after {i} iterations")
                self.animated_plot(eq_str, f, min(xl, xu), max(xl, xu), xr, "Bisection Method")
                return

            if fl * fxr < 0: xu = xr
            else: xl = xr

        self.log("Max iterations reached.")
        self.animated_plot(eq_str, f, xl, xu, xr, "Bisection Method")

    def run_fixed_point(self, g, eq_str, x0, es, max_iter):
        xr, xr_old = x0, 0
        self.log(f"{'Iter':<8} {'x_old':<12} {'g(x_old)':<14} {'ea %':<12}")
        self.log("-" * 50)

        for i in range(1, max_iter + 1):
            xr_old = xr
            xr = g(xr_old)

            if i > 1: ea = abs((xr - xr_old) / xr) * 100 if xr != 0 else abs((xr - xr_old) / (xr + 1e-10)) * 100
            else: ea = 100 

            self.log(f"{i:<8} {xr_old:<12.6f} {xr:<14.6f} {ea:<12.4f}")

            if i > 1 and ea < es:
                self.log("-" * 50)
                self.log(f"Converged! Root ≈ {xr:.8f} after {i} iterations.")
                f_plot = lambda x: x - g(x)
                self.animated_plot(f"x - ({eq_str})", f_plot, x0-2, x0+2, xr, "Fixed Point Iteration (f(x) = x - g(x))")
                return
                
            if i > 10 and ea > 1000:
                self.log("Method diverging! Error is growing.")
                return

        self.log("Reached max iterations.")

    def run_false_position(self, f, eq_str, xl, xu, es, max_iter):
        if f(xl) * f(xu) >= 0:
            self.log("Error: f(xl) and f(xu) must have opposite signs.")
            return

        xl_init, xu_init = xl, xu
        xr, xr_old = 0, 0
        self.log(f"{'Iter':<8} {'xl':<10} {'xu':<10} {'xr':<10} {'f(xr)':<12} {'ea %':<10}")
        
        for i in range(1, max_iter + 1):
            xr_old = xr
            fl, fu = f(xl), f(xu)
            xr = xu - (fu * (xl - xu)) / (fl - fu)
            fxr = f(xr)
            ea = abs((xr - xr_old) / xr) * 100 if (i > 1 and xr != 0) else 0

            self.log(f"{i:<8} {xl:<10.4f} {xu:<10.4f} {xr:<10.4f} {fxr:<12.4f} {ea:<10.4f}")

            if i > 1 and ea < es:
                self.log(f"Converged! Root: {xr:.6f} at {i} iterations.")
                self.animated_plot(eq_str, f, xl_init, xu_init, xr, "False Position Method")
                return

            if fl * fxr < 0: xu = xr
            else: xl = xr

        self.log("Reached max iterations.")
        self.animated_plot(eq_str, f, xl_init, xu_init, xr, "False Position Method")

    def run_newton(self, f, df, eq_str, x0, es, max_iter):
        x0_init, xr = x0, x0
        self.log(f"{'Iter':<8} {'xi':<12} {'f(xi)':<12} {'f\'(xi)':<12} {'ea %':<10}")
        
        for i in range(1, max_iter + 1):
            xr_old = xr
            fx, dfx = f(xr_old), df(xr_old)
            
            if dfx == 0:
                self.log("Derivative is zero. Newton-Raphson fails.")
                return

            xr = xr_old - (fx / dfx)
            ea = abs((xr - xr_old) / xr) * 100 if xr != 0 else 0

            self.log(f"{i:<8} {xr_old:<12.6f} {fx:<12.6f} {dfx:<12.6f} {ea:<10.4f}")

            if ea < es:
                self.log(f"Converged! Root: {xr:.6f} at {i} iterations.")
                self.animated_plot(eq_str, f, x0_init-2, x0_init+2, xr, "Newton-Raphson")
                return

        self.log("Reached max iterations.")
        self.animated_plot(eq_str, f, x0_init-2, x0_init+2, xr, "Newton-Raphson")

    def run_secant(self, f, eq_str, x_minus_1, x0, es, max_iter):
        xi_minus_1, xi = x_minus_1, x0
        self.log(f"{'Iter':<8} {'xi-1':<12} {'xi':<12} {'f(xi)':<12} {'ea %':<10}")
        
        for i in range(1, max_iter + 1):
            f_xi, f_xi_minus_1 = f(xi), f(xi_minus_1)

            if f_xi - f_xi_minus_1 == 0:
                self.log("Division by zero error.")
                return

            xi_plus_1 = xi - (f_xi * (xi - xi_minus_1)) / (f_xi - f_xi_minus_1)
            ea = abs((xi_plus_1 - xi) / xi_plus_1) * 100 if xi_plus_1 != 0 else 0

            self.log(f"{i:<8} {xi_minus_1:<12.6f} {xi:<12.6f} {f_xi:<12.6f} {ea:<10.4f}")

            if ea < es:
                self.log(f"Converged! Root: {xi_plus_1:.6f} at {i} iterations.")
                self.animated_plot(eq_str, f, x_minus_1, xi_plus_1, xi_plus_1, "Secant Method")
                return

            xi_minus_1, xi = xi, xi_plus_1

        self.log("Reached max iterations.")
        self.animated_plot(eq_str, f, x_minus_1, xi, xi, "Secant Method")

    def run_gauss_elimination(self, A, b, variables):
        n = len(b)
        augmented = np.hstack((A.astype(float).copy(), b.reshape(-1, 1)))

        self.log("Forward Elimination:")
        for i in range(n):
            pivot_row = np.argmax(np.abs(augmented[i:, i])) + i
            if np.isclose(augmented[pivot_row, i], 0.0):
                raise ValueError("The system has no unique solution.")

            if pivot_row != i:
                augmented[[i, pivot_row]] = augmented[[pivot_row, i]]
                self.log(f"Swapped row {i + 1} with row {pivot_row + 1}")

            for j in range(i + 1, n):
                factor = augmented[j, i] / augmented[i, i]
                augmented[j, i:] -= factor * augmented[i, i:]
                augmented[j, i] = 0.0

            self.log(f"After pivot step {i + 1}:")
            self.log(self.format_matrix(augmented))

        x = np.zeros(n, dtype=float)
        for i in range(n - 1, -1, -1):
            rhs = augmented[i, -1] - np.dot(augmented[i, i + 1:n], x[i + 1:n])
            x[i] = rhs / augmented[i, i]

        self.log("")
        self.log("Upper Triangular Matrix:")
        self.log(self.format_matrix(augmented[:, :-1]))
        self.log("Updated Constants:")
        self.log(self.format_matrix(augmented[:, -1]))
        self.log("Solution:")
        for variable, value in zip(variables, x):
            self.log(f"{variable} = {value:.6f}")

    def run_gauss_jordan(self, A, b, variables):
        n = len(b)
        augmented = np.hstack((A.astype(float).copy(), b.reshape(-1, 1)))

        self.log("Gauss-Jordan Elimination:")
        for i in range(n):
            pivot_row = np.argmax(np.abs(augmented[i:, i])) + i
            if np.isclose(augmented[pivot_row, i], 0.0):
                raise ValueError("The system has no unique solution.")

            if pivot_row != i:
                augmented[[i, pivot_row]] = augmented[[pivot_row, i]]
                self.log(f"Swapped row {i + 1} with row {pivot_row + 1}")

            augmented[i, i:] = augmented[i, i:] / augmented[i, i]

            for j in range(n):
                if j == i:
                    continue
                factor = augmented[j, i]
                augmented[j, i:] -= factor * augmented[i, i:]
                augmented[j, i] = 0.0

            self.log(f"After pivot step {i + 1}:")
            self.log(self.format_matrix(augmented))

        self.log("")
        self.log("Reduced Row Echelon Form:")
        self.log(self.format_matrix(augmented[:, :-1]))
        self.log("Solution:")
        for variable, value in zip(variables, augmented[:, -1]):
            self.log(f"{variable} = {value:.6f}")

    def run_cramers(self, A, b, variables):
        determinant = np.linalg.det(A)
        if np.isclose(determinant, 0.0):
            raise ValueError("Cramer's Rule requires a non-zero determinant.")

        self.log(f"D = {determinant:.6f}")
        self.log("")

        for i, variable in enumerate(variables):
            replaced_matrix = A.copy()
            replaced_matrix[:, i] = b
            determinant_i = np.linalg.det(replaced_matrix)
            self.log(f"D_{i + 1} = {determinant_i:.6f}")
            self.log(f"{variable} = {determinant_i / determinant:.6f}")

    def run_lu_pivot(self, A, b, variables):
        n = len(b)
        L = np.zeros((n, n), dtype=float)
        U = A.astype(float).copy()
        P = np.eye(n, dtype=float)

        self.log("LU Decomposition with Partial Pivoting:")
        for i in range(n):
            pivot = np.argmax(np.abs(U[i:, i])) + i
            if np.isclose(U[pivot, i], 0.0):
                raise ValueError("The system has no unique solution.")

            if pivot != i:
                U[[i, pivot]] = U[[pivot, i]]
                P[[i, pivot]] = P[[pivot, i]]
                if i > 0:
                    L[[i, pivot], :i] = L[[pivot, i], :i]
                self.log(f"Swapped row {i + 1} with row {pivot + 1}")

            L[i, i] = 1.0
            for j in range(i + 1, n):
                factor = U[j, i] / U[i, i]
                L[j, i] = factor
                U[j, i:] -= factor * U[i, i:]
                U[j, i] = 0.0

        Pb = P @ b
        y = np.zeros(n, dtype=float)
        for i in range(n):
            y[i] = Pb[i] - np.dot(L[i, :i], y[:i])

        x = np.zeros(n, dtype=float)
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]

        self.log("P Matrix:")
        self.log(self.format_matrix(P))
        self.log("L Matrix:")
        self.log(self.format_matrix(L))
        self.log("U Matrix:")
        self.log(self.format_matrix(U))
        self.log("Solution:")
        for variable, value in zip(variables, x):
            self.log(f"{variable} = {value:.6f}")
 

    # ================= ANIMATED PLOTTING =================
    
    def animated_plot(self, equation_str, f, bounds_low, bounds_high, root, title):
        margin = max(abs(bounds_high - bounds_low) * 0.5, 2.0)
        x_min = min(bounds_low, root) - margin
        x_max = max(bounds_high, root) + margin
        x_vals = np.linspace(x_min, x_max, 250) # 250 frames for animation
        
        try:
            y_vals = [f(x) for x in x_vals]
        except Exception as e:
            self.log(f"Plotting Error: {e}")
            return

        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#ecf0f1') # Match UI Theme
        ax.set_facecolor('#ffffff')

        # Formatting limits
        ax.set_xlim(x_min, x_max)
        y_min, y_max = min(y_vals), max(y_vals)
        margin_y = max((y_max - y_min) * 0.1, 1.0)
        ax.set_ylim(y_min - margin_y, y_max + margin_y)

        # Baseline and Elements
        ax.axhline(0, color='black', linewidth=1.2)
        line, = ax.plot([], [], label=f'f(x) = {equation_str}', color='#2980b9', linewidth=2.5)
        
        if root is not None:
            ax.plot(root, f(root), marker='o', color='#e74c3c', markersize=8, label=f'Root ≈ {root:.4f}')

        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title(title, fontweight="bold", color="#2c3e50")
        ax.legend()
        ax.grid(True, linestyle=':', alpha=0.7)

        # Animation Initialization
        def init():
            line.set_data([], [])
            return line,

        # Frame Updater
        def animate(i):
            line.set_data(x_vals[:i], y_vals[:i])
            return line,

        # Save reference to animation to stop it from being garbage collected
        self.current_animation = animation.FuncAnimation(
            fig, animate, init_func=init, frames=len(x_vals), 
            interval=10, blit=True, repeat=False
        )

        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = NumericalSolverApp(root)
    root.mainloop()
