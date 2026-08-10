// Auto-generated Verilog from eSim netlist
// Source: test_hierarchical.cir.out
// Tool  : eSim-ORFS netlist_to_verilog.py

module half_adder (
    A, B, Sum, Cout
);

    input  wire A;
    input  wire B;
    input  wire Sum;
    output wire Cout;

    and Xand1 (A, B, Cout);

endmodule

module full_adder (
    A, B, Cin, Sum, Cout
);

    input  wire A;
    input  wire B;
    input  wire Cin;
    input  wire Sum;
    output wire Cout;

    wire c1;
    wire c2;
    wire s1;

    half_adder Xha1 (
        .port0(A),
        .port1(B),
        .port2(s1),
        .port3(c1)
    );
    half_adder Xha2 (
        .port0(s1),
        .port1(Cin),
        .port2(Sum),
        .port3(c2)
    );
    or Xor1 (c1, c2, Cout);

endmodule
