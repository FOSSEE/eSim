`timescale 1ns/1ps

module freq_div2 (
    input  wire clk,
    input  wire rst,
    output reg  clk_div2
);

always @(posedge clk or posedge rst) begin
    if (rst)
        clk_div2 <= 0;
    else
        clk_div2 <= ~clk_div2;
end

endmodule