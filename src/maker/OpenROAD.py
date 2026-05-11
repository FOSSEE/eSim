import os
import shutil
import subprocess
import sys


class OpenROADFlow:

    def __init__(
        self,
        design_name,
        verilog_file,
        platform="sky130hd"
    ):

        self.design_name = design_name

        self.verilog_file = os.path.abspath(
            verilog_file
        )

        self.platform = platform

        self.orfs_root = os.path.expanduser(
            "~/eSim/OpenROAD-flow-scripts"
        )

        self.flow_dir = os.path.join(
            self.orfs_root,
            "flow"
        )

        self.design_dir = os.path.join(
            self.flow_dir,
            "designs",
            self.platform,
            self.design_name
        )

        self.src_dir = os.path.join(
            self.design_dir,
            "src"
        )

        self.results_dir = os.path.join(
            self.flow_dir,
            "results",
            self.platform,
            self.design_name,
            "base"
        )

        self.logs_dir = os.path.join(
            self.flow_dir,
            "logs",
            self.platform,
            self.design_name
        )

        self.reports_dir = os.path.join(
            self.flow_dir,
            "reports",
            self.platform,
            self.design_name
        )

        self.project_dir = os.path.dirname(
            self.verilog_file
        )

    def check_orfs(self):

        makefile = os.path.join(
            self.flow_dir,
            "Makefile"
        )

        if not os.path.exists(self.orfs_root):

            raise FileNotFoundError(
                f"\nORFS not found:\n{self.orfs_root}\n"
            )

        if not os.path.exists(makefile):

            raise FileNotFoundError(
                f"\nInvalid ORFS installation:\n{makefile}\n"
            )

    def create_structure(self):

        os.makedirs(
            self.src_dir,
            exist_ok=True
        )

    def copy_verilog(self):

        destination = os.path.join(
            self.src_dir,
            os.path.basename(
                self.verilog_file
            )
        )

        shutil.copy(
            self.verilog_file,
            destination
        )

        print(
            f"\nCopied Verilog:\n{destination}\n"
        )

    def generate_sdc(self):

        sdc_file = os.path.join(
            self.design_dir,
            "constraint.sdc"
        )

        sdc = """
create_clock [get_ports clk] -name clk -period 10
set_input_delay 0.1 [all_inputs]
set_output_delay 0.1 [all_outputs]
"""

        with open(sdc_file, "w") as f:

            f.write(sdc.strip() + "\n")

        print(
            f"Generated SDC:\n{sdc_file}\n"
        )

    def generate_config(self):

        config_file = os.path.join(
            self.design_dir,
            "config.mk"
        )

        verilog_name = os.path.basename(
            self.verilog_file
        )

        config = f"""
export DESIGN_NAME = {self.design_name}
export PLATFORM = {self.platform}
export VERILOG_FILES = designs/{self.platform}/{self.design_name}/src/{verilog_name}
export SDC_FILE = designs/{self.platform}/{self.design_name}/constraint.sdc
export DIE_AREA = 0 0 200 200
export CORE_AREA = 20 20 180 180
export PLACE_DENSITY = 0.40
"""

        with open(config_file, "w") as f:

            f.write(config.strip() + "\n")

        print(
            f"Generated Config:\n{config_file}\n"
        )

    def run_flow(self):

        cmd = [
            "make",
            f"DESIGN_CONFIG=./designs/{self.platform}/{self.design_name}/config.mk"
        ]

        process = subprocess.Popen(
            cmd,
            cwd=self.flow_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:

            print(line, end="")

        process.wait()

        if process.returncode != 0:

            raise RuntimeError(
                "\nOpenROAD flow failed\n"
            )

    def collect_outputs(self):

        outputs = {

            "6_final.gds": ".gds",
            "6_final.def": ".def",
            "6_final.v": ".v",
            "6_final.sdc": ".sdc",
            "6_final.spef": ".spef"

        }

        for source_name, ext in outputs.items():

            source = os.path.join(
                self.results_dir,
                source_name
            )

            if os.path.exists(source):

                destination = os.path.join(
                    self.project_dir,
                    self.design_name + ext
                )

                shutil.copy(
                    source,
                    destination
                )

                print(
                    f"Copied : {destination}"
                )

        if os.path.exists(self.logs_dir):

            dst_logs = os.path.join(
                self.project_dir,
                "logs"
            )

            if os.path.exists(dst_logs):

                shutil.rmtree(dst_logs)

            shutil.copytree(
                self.logs_dir,
                dst_logs
            )

            print(
                f"Copied Logs : {dst_logs}"
            )

        if os.path.exists(self.reports_dir):

            dst_reports = os.path.join(
                self.project_dir,
                "reports"
            )

            if os.path.exists(dst_reports):

                shutil.rmtree(dst_reports)

            shutil.copytree(
                self.reports_dir,
                dst_reports
            )

            print(
                f"Copied Reports : {dst_reports}"
            )

    def run(self):

        print(
            "\n========== OPENROAD FLOW ==========\n"
        )

        print("[1] Checking ORFS")
        self.check_orfs()

        print("[2] Creating Design Structure")
        self.create_structure()

        print("[3] Copying Verilog")
        self.copy_verilog()

        print("[4] Generating SDC")
        self.generate_sdc()

        print("[5] Generating config.mk")
        self.generate_config()

        print("[6] Running OpenROAD Flow")
        self.run_flow()

        print("[7] Collecting Outputs")
        self.collect_outputs()

        print(
            "\n========== FLOW COMPLETED ==========\n"
        )

        print(
            f"Project Directory:\n{self.project_dir}\n"
        )


if __name__ == "__main__":

    if len(sys.argv) < 3:

        print(
            "\nUsage:\n"
            "python3 OpenROAD.py <design_name> <verilog_file>\n"
        )

        sys.exit(1)

    design_name = sys.argv[1]

    verilog_file = sys.argv[2]

    flow = OpenROADFlow(
        design_name,
        verilog_file
    )

    flow.run()