

module booth_wallace_mul (
    input  [3:0] A,      // 4-bit 2's complement
    input  [3:0] B,      // 4-bit 2's complement
    output [7:0] P       // 8-bit 2's complement product
);

    // Treat inputs as signed internally
    wire signed [3:0] As = A;
    wire signed [3:0] Bs = B;

    // Sign extend multiplicand
    wire signed [7:0] A_ext = {{4{As[3]}}, As};
    wire signed [7:0] negA  = -A_ext;

    // Booth radix-2 ops (no function; safest for tools)
    wire signed [7:0] op0 =
        ({Bs[0],1'b0} == 2'b01) ? A_ext :
        ({Bs[0],1'b0} == 2'b10) ? negA  :
        8'sd0;

    wire signed [7:0] op1 =
        ({Bs[1],Bs[0]} == 2'b01) ? A_ext :
        ({Bs[1],Bs[0]} == 2'b10) ? negA  :
        8'sd0;

    wire signed [7:0] op2 =
        ({Bs[2],Bs[1]} == 2'b01) ? A_ext :
        ({Bs[2],Bs[1]} == 2'b10) ? negA  :
        8'sd0;

    wire signed [7:0] op3 =
        ({Bs[3],Bs[2]} == 2'b01) ? A_ext :
        ({Bs[3],Bs[2]} == 2'b10) ? negA  :
        8'sd0;

    // Partial products (left shifts)
    wire [7:0] pp0 = op0 <<< 0;
    wire [7:0] pp1 = op1 <<< 1;
    wire [7:0] pp2 = op2 <<< 2;
    wire [7:0] pp3 = op3 <<< 3;

    // Wallace tree using CSA (2 stages for 4 rows)
    wire [7:0] s1, c1;
    wire [7:0] s2, c2;

    csa_8bit CSA1 (.x(pp0), .y(pp1), .z(pp2), .sum(s1), .carry(c1));
    csa_8bit CSA2 (.x(s1),  .y(c1),  .z(pp3), .sum(s2), .carry(c2));

    // Final carry-propagate add
    assign P = s2 + c2;

endmodule


//============================================================
// 8-bit Carry Save Adder (3→2 compressor)
// carry output is already shifted left by 1
//============================================================
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
        for (i=0; i<8; i=i+1) begin : CSA
            full_adder FA (
                .a(x[i]),
                .b(y[i]),
                .cin(z[i]),
                .sum(sum[i]),
                .cout(c[i])
            );
        end
    endgenerate

    assign carry[0]   = 1'b0;
    assign carry[7:1] = c[6:0];

endmodule


//============================================================
// 1-bit Full Adder
//============================================================
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