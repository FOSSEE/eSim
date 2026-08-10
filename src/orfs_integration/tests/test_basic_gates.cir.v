// Auto-generated Verilog from eSim netlist
// Source: test_basic_gates.cir.out
// Tool  : eSim-ORFS netlist_to_verilog.py

module basic_gates (
    A, B, C, OUT
);

    input  wire A;
    input  wire B;
    input  wire C;
    output wire OUT;

    wire net1;
    wire net2;
    wire net3;
    wire net4;

    nand Xnand1 (A, B, net2);
    nor Xnor1 (A, B, net3);
    and Xand1 (net1, net2, net4);
    or Xor1 (net3, net4, OUT);

endmodule
