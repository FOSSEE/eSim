# =========================================================================
#      FILE: netlist2rtl.py
#
#     USAGE: ---
#
#   DESCRIPTION: This file is used to convert netlist to verilog
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Rishabh Jain, 2r10j5@gmail.com
#    MAINTAINED: Sumanto Kar, sumantokar@iitb.ac.in
#  ORGANIZATION: eSim Team at FOSSEE, IIT Bombay
#       CREATED: Monday 22 June 2026
# =========================================================================

import os
import sys

class NetlistToRTL:

    def __init__(self, cir_file):

        self.cir_file = cir_file

        self.module_name = os.path.basename(
            cir_file
        ).replace(".cir.out", "")

    # ----------------------------------------
    # DETECT HALF ADDER
    # ----------------------------------------

    def detect_halfadder(self, text):

        text = text.lower()

        if "half_adder" in text:
            return True

        if "d_xor" in text and "d_and" in text:
            return True

        return False

    # ----------------------------------------
    # DETECT FULL ADDER
    # ----------------------------------------

    def detect_fulladder(self, text):

        text = text.lower()

        if "full_adder" in text:
            return True

        if "cin" in text:
            return True

        return False

    # ----------------------------------------
    # HALF ADDER VERILOG
    # ----------------------------------------

    def generate_halfadder(self):

        return f"""module {self.module_name} (

    input in1,
    input in2,

    output sum,
    output cout

);

xor (sum, in1, in2);

and (cout, in1, in2);

endmodule
"""

    # ----------------------------------------
    # FULL ADDER VERILOG
    # ----------------------------------------

    def generate_fulladder(self):

        return f"""module {self.module_name} (

    input in1,
    input in2,
    input cin,

    output sum,
    output cout

);

wire axb;
wire ab;
wire ac;
wire bc;

xor (axb, in1, in2);

xor (sum, axb, cin);

and (ab, in1, in2);

and (ac, in1, cin);

and (bc, in2, cin);

or (cout, ab, ac, bc);

endmodule
"""

    # ----------------------------------------
    # CONVERT
    # ----------------------------------------

    def convert(self):

        with open(self.cir_file, "r") as f:

            content = f.read()

        # ------------------------------------
        # FULL ADDER
        # ------------------------------------

        if self.detect_fulladder(content):

            print(
                "\nDetected Circuit : FullAdder\n"
            )

            verilog = self.generate_fulladder()

        # ------------------------------------
        # HALF ADDER
        # ------------------------------------

        elif self.detect_halfadder(content):

            print(
                "\nDetected Circuit : HalfAdder\n"
            )

            verilog = self.generate_halfadder()

        else:

            raise RuntimeError(
                "\nUnsupported circuit.\n"
            )

        project_dir = os.path.dirname(
            self.cir_file
        )

        output_file = os.path.join(
            project_dir,
            self.module_name + ".v"
        )

        with open(output_file, "w") as f:

            f.write(verilog)

        return output_file


# ----------------------------------------
# MAIN
# ----------------------------------------

def main():

    if len(sys.argv) < 2:

        print(
            "\nUsage:\n"
            "python3 netlist2rtl.py file.cir.out\n"
        )

        sys.exit(1)

    cir_file = sys.argv[1]

    if not os.path.exists(cir_file):

        print(
            f"\nFile not found:\n{cir_file}\n"
        )

        sys.exit(1)

    print(
        "\n========== NETLIST TO RTL ==========\n"
    )

    converter = NetlistToRTL(cir_file)

    output_file = converter.convert()

    print(
        "\n========== COMPLETED ==========\n"
    )

    print(
        f"Generated : {output_file}\n"
    )


if __name__ == "__main__":

    main()
