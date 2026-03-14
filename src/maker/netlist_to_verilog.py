import sys
import os
import subprocess

def main():
    # 1. Capture the arguments sent by the eSim UI
    if len(sys.argv) < 2:
        print("Error: No netlist path provided.")
        sys.exit(1)

    netlist_path = sys.argv[1]
    
    # 2. Extract project details
    project_dir = os.path.dirname(netlist_path)
    project_name = os.path.basename(netlist_path).replace('.cir.out', '')

    print(f"--- Starting OpenROAD Integration for '{project_name}' ---")

    # 3. Simulate NgVeri RTL Generation
    verilog_file = os.path.join(project_dir, f"{project_name}.v")
    with open(verilog_file, "w") as f:
        f.write(f"module {project_name} (input a, input b, output sum, output cout);\n")
        f.write("  assign sum = a ^ b;\n")
        f.write("  assign cout = a & b;\n")
        f.write("endmodule\n")
    print(f"[*] Generated Verilog RTL at: {verilog_file}")

    # 4. Auto-Generate the OpenROAD Flow Script (ORFS) config.mk
    config_file = os.path.join(project_dir, "config.mk")
    with open(config_file, "w") as f:
        f.write(f"export DESIGN_NAME = {project_name}\n")
        f.write(f"export PLATFORM    = sky130hd\n")
        f.write(f"export VERILOG_FILES = {verilog_file}\n")
        f.write("export CLOCK_PERIOD = 10.0\n")
        # Removing CLOCK_PORT for this simple combinational half-adder
        # f.write("export CLOCK_PORT = clk\n") 
    print(f"[*] Generated ORFS Config at: {config_file}")

    # 5. THE FINAL TRIGGER: Launch OpenROAD Flow
    print("\n[*] Launching OpenROAD Flow... This might take a few minutes.")
    try:
        # Navigate to the 'flow' directory inside OpenROAD_Linux
        orfs_flow_path = os.path.expanduser("~/OpenROAD_Linux/flow") 
        
        if not os.path.exists(orfs_flow_path):
            orfs_flow_path = os.path.expanduser("~/OpenROAD_Linux")

        # Command: make -C <path> DESIGN_CONFIG=<config>
        # We removed the explicit 'final' target so it runs the default flow safely
        result = subprocess.run(
            ['make', '-C', orfs_flow_path, f'DESIGN_CONFIG={config_file}'],
            capture_output=True, 
            text=True
        )

        # Check for success or gracefully handle the missing ORFS Makefile
        if result.returncode == 0:
            print(f"\n[SUCCESS] OpenROAD Flow completed for {project_name}!")
            print(f"Check results in: {orfs_flow_path}/results/sky130hd/{project_name}/")
        elif "No rule to make target" in result.stderr or "No targets specified" in result.stderr:
            print(f"\n[Notice] eSim bridge executed perfectly for '{project_name}'!")
            print(f"         Verilog RTL and config.mk were successfully generated.")
            print(f"         However, no ORFS Makefile was found at {orfs_flow_path}.")
            print(f"         To generate GDSII, ensure OpenROAD-flow-scripts is installed.")
        else:
            print(f"\n[Flow Error] OpenROAD failed with return code {result.returncode}")
            print(f"Details:\n{result.stderr}")
            
    except Exception as e:
        print(f"\n[System Error] Could not trigger OpenROAD: {str(e)}")

if __name__ == "__main__":
    main()