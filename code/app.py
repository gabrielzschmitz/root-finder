"""
Main Application Entry Point.

This module initializes and runs the root-finding methods comparison application.
"""

# Third-Party Library Imports
import ttkbootstrap as ttk

# Local Imports
from ui import RootFinderUI

if __name__ == "__main__":
    """
    Initializes and runs the root-finding methods comparison application.
    """
    root = ttk.Window(themename="darkly")
    app = RootFinderUI(root)
    root.mainloop()
