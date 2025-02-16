"""
Root-Finding Methods Implementation.

This module provides implementations of various root-finding methods.

Classes:
    RootFinderMethods: Contains static methods for root-finding algorithms.
    FunctionSolver: Handles the evaluation and solving of functions.
"""

# Standard Library Imports
import math
import time
from tkinter import messagebox


class RootFinderMethods:
    """
    Contains static methods for root-finding algorithms.

    Methods:
        numerical_derivative: Computes the numerical derivative of a function.
        bisection: Finds a root using the bisection method.
        newton_raphson: Finds a root using the Newton-Raphson method.
        false_position: Finds a root using the false position method.
        fixed_point: Finds a root using the fixed-point iteration method.
        secant: Finds a root using the secant method.
    """

    @staticmethod
    def numerical_derivative(f, x, h=1e-5):
        """
        Computes the numerical derivative of a function.

        Args:
            f (callable): The function to differentiate.
            x (float): The point at which to compute the derivative.
            h (float): The step size for the numerical derivative.

        Returns:
            float: The numerical derivative of the function at the given point.
        """
        return (f(x + h) - f(x - h)) / (2 * h)

    @staticmethod
    def bisection(f, a, b, tol=1e-6, max_iter=100):
        """
        Finds a root using the bisection method.

        Args:
            f (callable): The function to find the root of.
            a (float): The start of the interval.
            b (float): The end of the interval.
            tol (float): The tolerance for the root.
            max_iter (int): The maximum number of iterations.

        Returns:
            tuple: The root and the number of iterations.
        """
        if f(a) * f(b) >= 0:
            raise ValueError("The function must have opposite signs at the endpoints.")
        iterations = 0
        while (b - a) / 2 > tol and iterations < max_iter:
            c = (a + b) / 2
            if f(c) == 0:
                break
            elif f(c) * f(a) < 0:
                b = c
            else:
                a = c
            iterations += 1
        return (a + b) / 2, iterations

    @staticmethod
    def newton_raphson(f, x0, tol=1e-6, max_iter=100):
        """
        Finds a root using the Newton-Raphson method.

        Args:
            f (callable): The function to find the root of.
            x0 (float): The initial guess.
            tol (float): The tolerance for the root.
            max_iter (int): The maximum number of iterations.

        Returns:
            tuple: The root and the number of iterations.
        """
        iterations = 0
        while abs(f(x0)) > tol and iterations < max_iter:
            df = RootFinderMethods.numerical_derivative(f, x0)
            if abs(df) < 1e-10:
                raise ValueError(
                    "Derivative is too close to zero. Choose a better interval or initial guess."
                )
            x0 = x0 - f(x0) / df
            iterations += 1
        return x0, iterations

    @staticmethod
    def false_position(f, a, b, tol=1e-6, max_iter=100):
        """
        Finds a root using the false position method.

        Args:
            f (callable): The function to find the root of.
            a (float): The start of the interval.
            b (float): The end of the interval.
            tol (float): The tolerance for the root.
            max_iter (int): The maximum number of iterations.

        Returns:
            tuple: The root and the number of iterations.
        """
        if f(a) * f(b) >= 0:
            raise ValueError("The function must have opposite signs at the endpoints.")
        iterations = 0
        c = a
        while abs(b - a) > tol and iterations < max_iter:
            c = b - f(b) * (b - a) / (f(b) - f(a))
            if abs(f(c)) < tol:
                break
            if f(c) * f(a) < 0:
                b = c
            else:
                a = c
            iterations += 1
        return c, iterations

    @staticmethod
    def fixed_point(_, g, x0, tol=1e-6, max_iter=100):
        """
        Finds a root using the fixed-point iteration method.

        Args:
            _: Placeholder for the function (not used).
            g (callable): The function for fixed-point iteration.
            x0 (float): The initial guess.
            tol (float): The tolerance for the root.
            max_iter (int): The maximum number of iterations.

        Returns:
            tuple: The root and the number of iterations.
        """
        iterations = 0
        x1 = x0
        while iterations < max_iter:
            x1 = g(x0)
            if abs(x1 - x0) < tol:
                return x1, iterations
            x0 = x1
            iterations += 1
        raise ValueError("Fixed-point iteration did not converge.")

    @staticmethod
    def secant(f, a, b, tol=1e-6, max_iter=100):
        """
        Finds a root using the secant method.

        Args:
            f (callable): The function to find the root of.
            a (float): The start of the interval.
            b (float): The end of the interval.
            tol (float): The tolerance for the root.
            max_iter (int): The maximum number of iterations.

        Returns:
            tuple: The root and the number of iterations.
        """
        iterations = 0
        c = b
        while abs(b - a) > tol and iterations < max_iter:
            c = b - f(b) * (b - a) / (f(b) - f(a))
            if abs(f(c)) < tol:
                break
            a = b
            b = c
            iterations += 1
        return c, iterations


class FunctionSolver:
    """
    Handles the evaluation and solving of functions.

    Attributes:
        finder (RootFinderMethods): An instance of RootFinderMethods for root-finding.
    """

    def __init__(self):
        """
        Initializes the FunctionSolver.
        """
        self.finder = RootFinderMethods()

    def solve(self, f_str, a, b, tol, method_name, g_str=None):
        """
        Solves the function using the selected method.

        Args:
            f_str (str): The function as a string.
            a (float): The start of the interval or initial guess.
            b (float): The end of the interval.
            tol (float): The tolerance for the root.
            method_name (str): The name of the method to use.
            g_str (str): The g(x) function as a string (for fixed-point iteration).

        Returns:
            tuple: The root, the number of iterations, and the computation time.
        """
        f_str = f_str.replace("^", "**")

        def f(x):
            try:
                return eval(
                    f_str,
                    {
                        "x": x,
                        "sin": math.sin,
                        "cos": math.cos,
                        "tan": math.tan,
                        "exp": math.exp,
                        "log": math.log,
                        "sqrt": math.sqrt,
                        "pi": math.pi,
                    },
                )
            except Exception as e:
                raise ValueError(f"Invalid function: {e}")

        # Get the method from RootFinderMethods
        method = getattr(self.finder, method_name, None)
        if not method:
            raise ValueError(f"Invalid method selected: {method_name}")

        # Solve using the selected method
        start_time = time.time()
        if method_name in ["bisection", "false_position", "secant"]:
            root, iterations = method(f, a, b, tol)
        elif method_name == "newton_raphson":
            interval_adjusted = False
            while a < b:
                try:
                    root, iterations = method(f, a, tol)
                    if a <= root <= b:
                        break
                    else:
                        a += 0.1
                        b -= 0.1
                        interval_adjusted = True
                except ValueError as e:
                    messagebox.showwarning(
                        "Warning",
                        f"Newton-Raphson failed: {e}\nFalling back to Bisection.",
                    )
                    root, iterations = self.finder.bisection(f, a, b, tol)
                    break
            else:
                raise ValueError(
                    "Newton-Raphson could not find a root within the interval. Try another method or adjust the interval."
                )
            if interval_adjusted:
                messagebox.showinfo(
                    "Interval Adjusted",
                    f"Root was outside the interval. Final interval used: [{a:.2f}, {b:.2f}]",
                )
        elif method_name == "fixed_point":
            if not g_str:
                raise ValueError("g(x) is required for Fixed-Point Iteration.")
            g_str = g_str.replace("^", "**")

            def g(x):
                try:
                    return eval(
                        g_str,
                        {
                            "x": x,
                            "sin": math.sin,
                            "cos": math.cos,
                            "tan": math.tan,
                            "exp": math.exp,
                            "log": math.log,
                            "sqrt": math.sqrt,
                            "pi": math.pi,
                        },
                    )
                except Exception as e:
                    raise ValueError(f"Invalid g(x): {e}")

            root, iterations = method(f, g, a, tol)
        else:
            raise ValueError(f"Invalid method selected: {method_name}")

        computation_time = time.time() - start_time
        return root, iterations, computation_time
