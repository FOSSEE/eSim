`timescale 1ns/1ps

// ============================================================
// 4x4 Signed Booth + Wallace (CSA) Multiplier
// ============================================================

module booth_wallace_4x4 (
    input  signed [3:0] A,
    input  signed [3:0] B,
    output signed [7:0] P
);

    // --------------------------------------------------
    // Sign extend A
    // --------------------------------------------------
    wire signed [7:0] A_ext = {{4{A[3]}}, A};
    wire signed [7:0] negA  = -A_ext;

    // --------------------------------------------------
    // Booth Encoding (Radix-2)
    // --------------------------------------------------

    wire signed [7:0] op0 =
        ({B[0],1'b0} == 2'b01) ? A_ext :
        ({B[0],1'b0} == 2'b10) ? negA  :
        8'sd0;

    wire signed [7:0] op1 =
        ({B[1],B[0]} == 2'b01) ? A_ext :
        ({B[1],B[0]} == 2'b10) ? negA  :
        8'sd0;

    wire signed [7:0] op2 =
        ({B[2],B[1]} == 2'b01) ? A_ext :
        ({B[2],B[1]} == 2'b10) ? negA  :
        8'sd0;

    wire signed [7:0] op3 =
        ({B[3],B[2]} == 2'b01) ? A_ext :
        ({B[3],B[2]} == 2'b10) ? negA  :
        8'sd0;

    // Shift partial products
    wire signed [7:0] pp0 = op0 <<< 0;
    wire signed [7:0] pp1 = op1 <<< 1;
    wire signed [7:0] pp2 = op2 <<< 2;
    wire signed [7:0] pp3 = op3 <<< 3;

    // --------------------------------------------------
    // Wallace Tree (CSA Stage 1)
    // --------------------------------------------------
    wire [7:0] s1, c1;
    csa_8bit CSA1 (.x(pp0), .y(pp1), .z(pp2), .sum(s1), .carry(c1));

    // --------------------------------------------------
    // Wallace Tree (CSA Stage 2)
    // --------------------------------------------------
    wire [7:0] s2, c2;
    csa_8bit CSA2 (.x(s1), .y(c1), .z(pp3), .sum(s2), .carry(c2));

    // --------------------------------------------------
    // Final Carry Propagate Adder
    // --------------------------------------------------
    assign P = s2 + c2;

endmodule



// ============================================================
// 8-bit Carry Save Adder (3→2 compressor)
// ============================================================

module csa_8bit (
    input  [7:0] x,
    input  [7:0] y,
    input  [7:0] z,
    output [7:0] sum,
    output [7:0] carry
);

    wire [7:0] c;

    genvar i;
    generate
        for (i = 0; i < 8; i = i + 1) begin : CSA
            full_adder FA (
                .a(x[i]),
                .b(y[i]),
                .cin(z[i]),
                .sum(sum[i]),
                .cout(c[i])
            );
        end
    endgenerate

    // Shift carry left by 1
    assign carry[0]   = 1'b0;
    assign carry[7:1] = c[6:0];

endmodule



// ============================================================
// 1-bit Full Adder
// ============================================================

module full_adder (
    input  a,
    input  b,
    input  cin,
    output sum,
    output cout
);

    assign sum  = a ^ b ^ cin;
   assign cout = (a & b) | (a & cin) | (b & cin);
   endmodule