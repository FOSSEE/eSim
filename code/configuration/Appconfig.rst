Configuration Component
=======================

This is the configuration file :

1. Stores default values, such as workspace path, project/subcircuit info, and configuration paths.
2. Loads configuration files (like config.ini).
3. Reads from workspace.txt to determine the current workspace.
4. Provides helper functions to log messages (info, warning, error).
5. Tracks spawned processes and UI elements like dock widgets.

.. note::

   Source : ``/src/configuration/Appconfig.py``

.. automodule:: configuration.Appconfig
	:members:
