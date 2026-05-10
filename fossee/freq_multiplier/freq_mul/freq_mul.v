`timescale 1ns/1ps

module freq_x2 (
    input  wire clk,
    output reg  clk2z
);

initial clk2z = 1'b0;

always @(posedge clk or negedge clk)
    clk2z <= ~clk2z;

endmodule