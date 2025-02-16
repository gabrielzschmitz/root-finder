"""
Root-Finding Methods Comparison Application.

This module provides a graphical user interface (GUI) for comparing different root-finding methods.
It uses the `ttkbootstrap` library for the UI and `matplotlib` for plotting.

Classes:
    RootFinderUI: The main application class.
    PlotManager: Manages plotting functionality.
    ThemeManager: Manages theme and color settings.
"""

# Standard Library Imports
import math, csv, os
from tkinter import messagebox, filedialog

# Third-Party Library Imports
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyperclip

# Local Imports
from functions import FunctionSolver, RootFinderMethods


class RootFinderUI:
    """
    The main application class for the root-finding methods comparison tool.

    Attributes:
        root (ttk.Window): The root window of the application.
        theme_manager (ThemeManager): Manages the application's theme.
        plot_manager (PlotManager): Manages plotting functionality.
        function_solver (FunctionSolver): Handles root-finding computations.
        f_entry (ttk.Entry): Input field for the function.
        g_entry (ttk.Entry): Input field for g(x) (used in fixed-point iteration).
        a_entry (ttk.Entry): Input field for the interval start or initial guess.
        b_entry (ttk.Entry): Input field for the interval end.
        tol_entry (ttk.Entry): Input field for the tolerance.
        method_var (ttk.StringVar): Stores the selected method.
        method_combobox (ttk.Combobox): Dropdown for selecting the method.
        solve_button (ttk.Button): Button to trigger the solve operation.
        close_button (ttk.Button): Button to close the application.
        save_button (ttk.Button): Button to save the plot.
        theme_button (ttk.Button): Button to toggle the theme.
        result_label (ttk.Label): Displays the results.
        copy_button (ttk.Button): Button to copy the results to the clipboard.
    """

    def __init__(self, root):
        """
        Initializes the RootFinderApp.

        Args:
            root (ttk.Window): The root window of the application.
        """
        self.root = root
        self.root.title("Root-Finding Methods Comparison")
        self.root.geometry("800x1024")
        self.root.resizable(0, 0)

        self.theme_manager = ThemeManager()
        self.plot_manager = PlotManager(root, self.theme_manager)
        self.function_solver = FunctionSolver()

        # Input Frame
        input_frame = ttk.LabelFrame(root, text="Input", padding=10)
        input_frame.pack(fill=X, padx=10, pady=10)

        ttk.Label(input_frame, text="f(x):").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.f_entry = ttk.Entry(input_frame, width=40)
        self.f_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=3)
        self.f_entry.insert(0, "sin(x) + cos(x) + 1")

        ttk.Label(input_frame, text="g(x) (for Fixed-Point Iteration):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.g_entry = ttk.Entry(input_frame, width=40, state=DISABLED)
        self.g_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
        self.g_entry.insert(0, "x - (sin(x) + cos(x) + 1) / 2")

        ttk.Label(input_frame, text="Interval [a, b] or Initial Guess:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.a_entry = ttk.Entry(input_frame, width=10)
        self.a_entry.grid(row=2, column=1, padx=5, pady=5)
        self.a_entry.insert(0, "1")
        self.b_entry = ttk.Entry(input_frame, width=10)
        self.b_entry.grid(row=2, column=2, padx=5, pady=5)
        self.b_entry.insert(0, "4")

        ttk.Label(input_frame, text="Target Error (Tolerance):").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.tol_entry = ttk.Entry(input_frame, width=10)
        self.tol_entry.grid(row=3, column=1, padx=5, pady=5)
        self.tol_entry.insert(0, "1e-6")

        ttk.Label(input_frame, text="Method:").grid(
            row=4, column=0, sticky="w", padx=5, pady=5
        )
        self.method_var = ttk.StringVar()
        self.method_var.trace_add(
            "write", self._on_method_change
        )  # Track method changes

        self.methods = self._get_root_finding_methods()
        self.method_combobox = ttk.Combobox(
            input_frame,
            textvariable=self.method_var,
            values=list(self.methods.keys()),
        )
        self.method_combobox.grid(row=4, column=1, padx=5, pady=5, columnspan=3)
        self.method_combobox.current(0)

        for i in range(5):
            input_frame.grid_columnconfigure(i, weight=1)

        self.solve_button = ttk.Button(
            input_frame, text="Solve", command=self.solve, bootstyle=PRIMARY, width=15
        )
        self.solve_button.grid(row=5, column=0, padx=5, pady=10, sticky="ew")

        self.close_button = ttk.Button(
            input_frame,
            text="Close",
            command=self.root.quit,
            bootstyle=DANGER,
            width=15,
        )
        self.close_button.grid(row=5, column=1, padx=5, pady=10, sticky="ew")

        self.save_button = ttk.Button(
            input_frame,
            text="Save Plot",
            command=self.plot_manager.save_plot,
            bootstyle=SUCCESS,
            state=DISABLED,
            width=15,
        )
        self.save_button.grid(row=5, column=2, padx=5, pady=10, sticky="ew")

        self.theme_button = ttk.Button(
            input_frame,
            text="Toggle Theme",
            command=self.toggle_theme,
            bootstyle=INFO,
            width=15,
        )
        self.theme_button.grid(row=5, column=3, padx=5, pady=10, sticky="ew")

        output_frame = ttk.LabelFrame(root, text="Output", padding=10)
        output_frame.pack(fill=X, padx=10, pady=10)

        self.result_label = ttk.Label(
            output_frame, text="Results will be displayed here."
        )
        self.result_label.pack(fill=X, padx=5, pady=5)

        self.copy_button = ttk.Button(
            output_frame,
            text="Copy Output",
            command=self.copy_output,
            bootstyle=INFO,
            state=DISABLED,
        )
        self.copy_button.pack(fill=X, padx=5, pady=5)

    def _get_root_finding_methods(self):
        """
        Retrieves all root-finding methods from the RootFinderMethods class.

        Returns:
            dict: A dictionary mapping display names to method names.
        """
        methods = {}
        blacklist = ["numerical_derivative"]
        for name, method in RootFinderMethods.__dict__.items():
            if isinstance(method, staticmethod) and name not in blacklist:
                display_name = name.replace("_", " ").title()
                methods[display_name] = name
        return methods

    def _on_method_change(self, *args):
        """
        Enables or disables the g(x) field based on the selected method.
        """
        method_display_name = self.method_var.get()
        if method_display_name == "Fixed Point":
            self.g_entry.config(state=NORMAL)
        else:
            self.g_entry.config(state=DISABLED)

    def save_to_csv(self, method, function, iterations, interval, root, comp_time):
        file_exists = os.path.isfile("results.csv")
        with open("results.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    [
                        "method",
                        "function",
                        "iterations",
                        "interval",
                        "root",
                        "comp_time",
                    ]
                )
            writer.writerow(
                [method, f'"{function}"', iterations, interval, root, comp_time]
            )

    def solve(self):
        """
        Solves the function using the selected method and displays the results.
        """
        try:
            f_str = self.f_entry.get()
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
            method_display_name = self.method_var.get()

            method_name = self.methods.get(method_display_name)
            if not method_name:
                raise ValueError("Invalid method selected.")

            if method_name == "fixed_point":
                g_str = self.g_entry.get()
                if not g_str:
                    raise ValueError("g(x) is required for Fixed-Point Iteration.")
            else:
                g_str = None

            root, iterations, computation_time = self.function_solver.solve(
                f_str, a, b, tol, method_name, g_str
            )

            if root is not None:
                result_text = f"Root: {root:.6f}\nIterations: {iterations}\nComputation Time: {computation_time:.6f} seconds"
                self.result_label.config(text=result_text)
            else:
                self.result_label.config(text="No root found.")

            self.plot_manager.update_plot(f_str, a, b, root, method_display_name)

            interval = f"[{a}, {b}]"
            self.save_to_csv(
                method_display_name, f_str, iterations, interval, root, computation_time
            )

            self.save_button.config(state=NORMAL)
            self.copy_button.config(state=NORMAL)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def copy_output(self):
        """
        Copies the results to the clipboard.
        """
        result_text = self.result_label.cget("text")
        if result_text != "Results will be displayed here.":
            pyperclip.copy(result_text)
            messagebox.showinfo("Copied", "Output copied to clipboard!")

    def toggle_theme(self):
        """
        Toggles the application's theme between light and dark modes.
        """
        self.theme_manager.toggle_theme()
        self.plot_manager.update_plot_colors()


class PlotManager:
    """
    Manages plotting functionality for the application.

    Attributes:
        theme_manager (ThemeManager): Manages the application's theme.
        fig (matplotlib.figure.Figure): The figure for the plot.
        ax (matplotlib.axes.Axes): The axes for the plot.
        canvas (FigureCanvasTkAgg): The canvas for embedding the plot in the UI.
    """

    def __init__(self, root, theme_manager):
        """
        Initializes the PlotManager.

        Args:
            root (ttk.Window): The root window of the application.
            theme_manager (ThemeManager): Manages the application's theme.
        """
        self.theme_manager = theme_manager
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=YES)
        self.update_plot_colors()

    def update_plot(self, f_str, a, b, root, method):
        """
        Updates the plot with the given function and root.

        Args:
            f_str (str): The function as a string.
            a (float): The start of the interval.
            b (float): The end of the interval.
            root (float): The root found by the method.
            method (str): The name of the method used.
        """
        self.ax.clear()

        # Ensure the root is included in the plotting range
        if root is not None:
            a, b = min(a, root), max(b, root)

        x = np.linspace(a, b, 400)
        y = [self._eval_function(f_str, xi) for xi in x]
        colors = self.theme_manager.get_colors()
        self.ax.plot(x, y, label=f"f(x) = {f_str}", color=colors["primary"])
        self.ax.axhline(0, color=colors["danger"], linewidth=0.5)
        if root is not None:
            self.ax.scatter([root], [0], color=colors["success"], label="Root")
        self.ax.set_xlabel("x", color=colors["fg"])
        self.ax.set_ylabel("f(x)", color=colors["fg"])
        self.ax.set_title(f"{method} Method", color=colors["fg"])
        self.ax.legend()
        self.ax.grid(color=colors["inputfg"], linestyle="--", linewidth=0.5)
        self.ax.set_facecolor(colors["bg"])
        self.fig.patch.set_facecolor(colors["bg"])
        self.canvas.draw()

    def save_plot(self):
        """
        Saves the current plot to a file.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
        )
        if file_path:
            self.fig.savefig(file_path)
            messagebox.showinfo("Success", f"Plot saved successfully at {file_path}")

    def _eval_function(self, f_str, x):
        """
        Evaluates the function at a given point.

        Args:
            f_str (str): The function as a string.
            x (float): The point at which to evaluate the function.

        Returns:
            float: The value of the function at the given point.
        """
        f_str = f_str.replace("^", "**")
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

    def update_plot_colors(self):
        """
        Updates the plot colors based on the current theme.
        """
        colors = self.theme_manager.get_colors()
        self.ax.set_facecolor(colors["bg"])
        self.fig.patch.set_facecolor(colors["bg"])
        for spine in self.ax.spines.values():
            spine.set_edgecolor(colors["fg"])
        self.ax.xaxis.label.set_color(colors["fg"])
        self.ax.yaxis.label.set_color(colors["fg"])
        self.ax.title.set_color(colors["fg"])
        self.ax.tick_params(axis="x", colors=colors["fg"])
        self.ax.tick_params(axis="y", colors=colors["fg"])
        self.ax.grid(color=colors["inputfg"], linestyle="--", linewidth=0.5)
        self.canvas.draw()


class ThemeManager:
    """
    Manages the application's theme and color settings.

    Attributes:
        current_theme (str): The current theme ("darkly" or "minty").
        theme_colors (dict): A dictionary of color schemes for the themes.
        style (ttk.Style): The style object for the application.
    """

    def __init__(self):
        """
        Initializes the ThemeManager.
        """
        self.current_theme = "darkly"
        self.theme_colors = {
            "minty": {
                "type": "light",
                "colors": {
                    "primary": "#78c2ad",
                    "secondary": "#f3969a",
                    "success": "#56cc9d",
                    "info": "#6cc3d5",
                    "warning": "#ffce67",
                    "danger": "#ff7851",
                    "light": "#F8F9FA",
                    "dark": "#343A40",
                    "bg": "#ffffff",
                    "fg": "#5a5a5a",
                    "selectbg": "#f3969a",
                    "selectfg": "#ffffff",
                    "border": "#ced4da",
                    "inputfg": "#696969",
                    "inputbg": "#fff",
                },
            },
            "darkly": {
                "type": "dark",
                "colors": {
                    "primary": "#375a7f",
                    "secondary": "#444444",
                    "success": "#00bc8c",
                    "info": "#3498db",
                    "warning": "#f39c12",
                    "danger": "#e74c3c",
                    "light": "#ADB5BD",
                    "dark": "#303030",
                    "bg": "#222222",
                    "fg": "#ffffff",
                    "selectbg": "#555555",
                    "selectfg": "#ffffff",
                    "border": "#222222",
                    "inputfg": "#ffffff",
                    "inputbg": "#2f2f2f",
                },
            },
        }
        self.style = ttk.Style(theme=self.current_theme)

    def toggle_theme(self):
        """
        Toggles the application's theme between light and dark modes.
        """
        self.current_theme = "minty" if self.current_theme == "darkly" else "darkly"
        self.style.theme_use(self.current_theme)

    def get_colors(self):
        """
        Retrieves the color scheme for the current theme.

        Returns:
            dict: A dictionary of colors for the current theme.
        """
        return self.theme_colors[self.current_theme]["colors"]
