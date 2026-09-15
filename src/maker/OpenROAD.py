import os
import subprocess
from PyQt5 import QtWidgets

class OpenROADLogic:
    def __init__(self, project_path):
        """
        Initialize with the project path from eSim.
        """
        self.project_path = project_path
        self.project_name = os.path.basename(project_path)

    def run(self):
        """
        Main execution flow: Netlist -> Verilog -> OpenROAD Synthesis
        """
        print(f"\n[OpenROAD Flow] Initiating for: {self.project_name}")
        
        # 1. Define Absolute Paths
        # Using expanduser("~") ensures it works for /home/soumy/ on any machine
        home_dir = os.path.expanduser("~")
        
        # Path to your Netlist-to-Verilog script from Task 1
        script_path = os.path.join(home_dir, "eSim", "src", "maker", "netlist_to_verilog.py")
        
        # Path to the circuit netlist inside the project folder
        netlist_path = os.path.join(self.project_path, f"{self.project_name}.cir.out")

        # 2. Validation Check
        if not os.path.exists(netlist_path):
            print(f"[Error] Netlist not found at: {netlist_path}")
            QtWidgets.QMessageBox.critical(
                None, "Error", 
                "Netlist (.cir.out) not found!\n\nPlease run 'Convert KiCad to Ngspice' first."
            )
            return

        # 3. Trigger the actual conversion script using Subprocess
        try:
            print(f"[OpenROAD] Executing: python3 {script_path} {netlist_path}")
            
            # This line officially bridges eSim to your Verilog converter
            result = subprocess.run(['python3', script_path, netlist_path], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"[Success] {result.stdout}")
                QtWidgets.QMessageBox.information(
                    None, "Success", 
                    f"Verilog conversion successful for '{self.project_name}'!\n\nReady for OpenROAD synthesis."
                )
            else:
                print(f"[Script Error] {result.stderr}")
                QtWidgets.QMessageBox.warning(
                    None, "Script Error", 
                    f"The conversion script failed:\n\n{result.stderr}"
                )
                
        except Exception as e:
            print(f"[System Error] {str(e)}")
            QtWidgets.QMessageBox.critical(
                None, "Execution Error", 
                f"Could not trigger the conversion script:\n{str(e)}"
            )