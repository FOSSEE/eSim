NgspicetoModelica Component
===========================

This module provides the core functionality for converting Ngspice netlists to Modelica models in eSim.

**Features:**
- Parses Ngspice netlists and extracts device, source, and subcircuit information.
- Maps Ngspice components and parameters to Modelica equivalents using a JSON mapping file.
- Generates Modelica code for analog circuits, including support for subcircuits and parameterized models.
- Handles unit conversion and device-specific parameter mapping.

**Usage:**
Refer to the API documentation or user guide for instructions on using the NgspicetoModelica converter. Typically, you will instantiate the `NgMoConverter` class and use its methods to process netlists and generate Modelica files.

.. note::

   Source : ``src/ngspicetoModelica/NgspicetoModelica.py``

.. automodule:: ngspicetoModelica.NgspicetoModelica
   :members: