module fir_filter (
    input clk,
    input rst,
    input signed [7:0] x,
    output signed [15:0] y
);

    // coefficients (symmetric low-pass)
    parameter signed [7:0] b0  = 8'd1;
    parameter signed [7:0] b1  = 8'd3;
    parameter signed [7:0] b2  = 8'd6;
    parameter signed [7:0] b3  = 8'd10;
    parameter signed [7:0] b4  = 8'd15;
    parameter signed [7:0] b5  = 8'd18;
    parameter signed [7:0] b6  = 8'd18;
    parameter signed [7:0] b7  = 8'd15;
    parameter signed [7:0] b8  = 8'd10;
    parameter signed [7:0] b9  = 8'd6;
    parameter signed [7:0] b10 = 8'd3;
    parameter signed [7:0] b11 = 8'd1;

    // delay line
    reg signed [7:0] x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11;

    // multipliers
    wire signed [15:0]
        m0,m1,m2,m3,m4,m5,
        m6,m7,m8,m9,m10,m11;

    assign m0  = b0  * x;
    assign m1  = b1  * x1;
    assign m2  = b2  * x2;
    assign m3  = b3  * x3;
    assign m4  = b4  * x4;
    assign m5  = b5  * x5;
    assign m6  = b6  * x6;
    assign m7  = b7  * x7;
    assign m8  = b8  * x8;
    assign m9  = b9  * x9;
    assign m10 = b10 * x10;
    assign m11 = b11 * x11;

    // sum
    assign y = m0+m1+m2+m3+m4+m5+
               m6+m7+m8+m9+m10+m11;

    // shift register
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            x1<=0; x2<=0; x3<=0; x4<=0; x5<=0; x6<=0;
            x7<=0; x8<=0; x9<=0; x10<=0; x11<=0;
        end else begin
            x1<=x;
            x2<=x1;
            x3<=x2;
            x4<=x3;
            x5<=x4;
            x6<=x5;
            x7<=x6;
            x8<=x7;
            x9<=x8;
            x10<=x9;
            x11<=x10;
        end
    end

endmodule