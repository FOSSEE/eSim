# eSim Architecture & Workflows

This document contains detailed flowcharts and diagrams mapping out the inner workings, simulation pipelines, and data transformations within eSim.

---

## 1. Standard Simulation Workflow

This flowchart details the end-to-end user journey for a standard analog/digital simulation in eSim, from project creation to waveform analysis.

```mermaid
flowchart TD
    %% Styling
    classDef startend fill:#2ECC71,stroke:#27AE60,stroke-width:2px,color:#fff
    classDef process fill:#3498DB,stroke:#2980B9,stroke-width:2px,color:#fff
    classDef decision fill:#F1C40F,stroke:#F39C12,stroke-width:2px,color:#333
    classDef io fill:#9B59B6,stroke:#8E44AD,stroke-width:2px,color:#fff
    
    START([Start eSim Project]):::startend --> CREATE{New or Existing?}:::decision
    CREATE -- New --> PROJ[Create Project Structure]:::process
    CREATE -- Existing --> OPEN[Open Project Workspace]:::process
    
    PROJ --> SCHEM[Draw Schematic in KiCad]:::process
    OPEN --> SCHEM
    
    SCHEM --> CHECK{Mixed Signal?}:::decision
    CHECK -- Yes --> VHDL[Write VHDL/Verilog Models]:::process
    VHDL --> GHDL[Compile via NGHDL/NgVeri]:::process
    GHDL --> SYM[Generate KiCad Symbol]:::process
    SYM --> SCHEM
    
    CHECK -- No --> K2N[Run KiCad-to-Ngspice]:::process
    K2N --> PARSE[Parse XML Netlist]:::process
    PARSE --> SRC[Configure Sources & Analysis]:::process
    SRC --> DEV[Configure Device Models]:::process
    
    DEV --> SPICE[Generate .cir SPICE Netlist]:::io
    SPICE --> NGSPICE[Execute Ngspice Simulation]:::process
    
    NGSPICE --> OUT{Simulation Success?}:::decision
    OUT -- No --> ERR[View Error Log & Debug]:::process
    ERR --> SCHEM
    
    OUT -- Yes --> RAW[Generate RAW Output Data]:::io
    RAW --> PLOT[Extract Data for Plotting]:::process
    PLOT --> MAT[Render matplotlib Waveforms]:::process
    
    MAT --> END([Analyze Results]):::startend
```

---

## 2. Mixed-Signal Simulation Flow (NGHDL)

This diagram breaks down how eSim bridges digital logic (VHDL/Verilog) with analog simulation using GHDL and Ngspice code models.

```mermaid
flowchart TD
    %% Styling
    classDef input fill:#34495E,stroke:#2C3E50,stroke-width:2px,color:#fff
    classDef process fill:#16A085,stroke:#1ABC9C,stroke-width:2px,color:#fff
    classDef output fill:#8E44AD,stroke:#9B59B6,stroke-width:2px,color:#fff
    
    VHDL([Write VHDL/Verilog Code]):::input --> UPLOAD[Upload via NGHDL/NgVeri UI]:::process
    UPLOAD --> COMPILE[GHDL/Verilator Compiles Code to Shared Lib]:::process
    COMPILE --> MODEL[Create Ngspice Code Model .cm]:::process
    MODEL --> KICAD[Generate KiCad Component Symbol]:::output
    
    KICAD --> SCHEM([Place Symbol in Schematic]):::input
    SCHEM --> BRIDGE[ADC/DAC Bridge Insertion]:::process
    BRIDGE --> SIM[Execute Mixed-Signal Co-Simulation]:::output
```

---

## 3. KiCad-to-Ngspice Netlist Conversion

A deep dive into the `Convert.py` backend pipeline, showing how KiCad's XML data is processed into an executable SPICE netlist.

```mermaid
flowchart TD
    %% Styling
    classDef input fill:#34495E,stroke:#2C3E50,stroke-width:2px,color:#fff
    classDef process fill:#E67E22,stroke:#D35400,stroke-width:2px,color:#fff
    classDef io fill:#9B59B6,stroke:#8E44AD,stroke-width:2px,color:#fff
    
    XML([KiCad XML Netlist]):::input --> PARSE[Parse XML DOM]:::process
    PARSE --> EXTRACT[Extract Components & Connections]:::process
    EXTRACT --> MAP[Map Pins to Ngspice Nodes]:::process
    MAP --> SUB[Resolve Subcircuits & Macros]:::process
    SUB --> INJECT[Inject Device Parameters & Models]:::process
    INJECT --> SPICE([Generate .cir SPICE Netlist]):::io
```

---

## 4. Device Model Generation Pipeline

Outlining how user-defined models (Diodes, BJTs, MOSFETs) are integrated via the Model Editor.

```mermaid
flowchart LR
    %% Styling
    classDef input fill:#2C3E50,stroke:#1A252F,stroke-width:2px,color:#fff
    classDef process fill:#E74C3C,stroke:#C0392B,stroke-width:2px,color:#fff
    classDef output fill:#F39C12,stroke:#E67E22,stroke-width:2px,color:#fff
    
    UI([Model Editor UI]):::input --> VAL[Validate Parameters]:::process
    VAL --> TEMPLATE[Inject Data into SPICE Template]:::process
    TEMPLATE --> LIB([Save to project .lib file]):::output
    LIB --> K2N([Attached during Netlist Conversion]):::output
```

---

## 5. Further reading

- [`docs/NGVERI_ACCURACY.md`](docs/NGVERI_ACCURACY.md) — correctness record for
  the NgVeri / NGHDL / d_cosim digital co-simulation backends: what the
  generated `cfunc.mod` contract with ngspice is, the silent-wrong-value
  defects that have been fixed in it, and the open work (notably
  `cm_irreversible()` on generated models).
- **Verilog design identity.** A model is named after the **top module in the
  design**, never after the file holding it (`ModelGeneration.resolve_identity`).
  eSim copies the design into its own build tree, so that copy is named for the
  pipeline and the user's file name is irrelevant — which is why there is no
  longer any "file name and module name are not same" refusal to hit. Three
  cases still take the name from the file, deliberately: `.tlv` (sandpiper has
  not run and always emits `module top`), a top module literally called `top`,
  and a source no parser can read. Designs live in
  `<workspace>/VerilogLibrary/<module>/`, written by `DesignBus`'s debounced
  autosave (`maker/verilog_library.py`).
- [`docs/MAKERCHIP_INTEGRATION.md`](docs/MAKERCHIP_INTEGRATION.md) — the
  browser-plugin bridge behind **Edit in Makerchip IDE**, including file sync,
  conflict handling, loopback security and the boundary between Makerchip and
  eSim Verify/Convert.
- [`docs/AI_ASSISTANT.md`](docs/AI_ASSISTANT.md) — the optional local AI
  Assistant (Ollama): installing, using and troubleshooting it. Developer
  notes — how it hooks into the main window, Project Explorer and simulation
  errors, the theme gotcha, models and packaging — are in
  [`src/chatbot/README_CHATBOT.md`](src/chatbot/README_CHATBOT.md).
- [`docs/UPSTREAM_DECISIONS.md`](docs/UPSTREAM_DECISIONS.md) — the defects in
  eSim's core converter and the NgVeri backend that are **measured, fixed, and
  deliberately switched off**, because turning them on would change results
  eSim has produced since 2.5. Read this before wiring any of that code back
  in. The rule it records: the converter and NgVeri behave as 2.5 did, and
  d_cosim matches NgVeri bug-for-bug so that swapping backends never changes a
  number.
