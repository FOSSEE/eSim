# ngspiceSimulation/__init__.py
"""
NGSpice Simulation Module

This package provides NGSpice simulation integration including:
- NgspiceWidget: Widget for running NGSpice simulations
- plotWindow: Window for plotting and analyzing simulation results
"""

from .NgspiceWidget import NgspiceWidget
from .plot_window import plotWindow

__all__ = ['NgspiceWidget', 'plotWindow']
__version__ = '1.0.0'
