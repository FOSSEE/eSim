`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 02.03.2026 21:11:33
// Design Name: 
// Module Name: tb
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////

module sync_fifo_tb;

    reg clk;
    reg rst;
    reg wr_en;
    reg rd_en;
    reg [7:0] din;

    wire [7:0] dout;
    wire full;
    wire empty;

    // DUT
    sync_fifo uut (
        .clk(clk),
        .rst(rst),
        .wr_en(wr_en),
        .rd_en(rd_en),
        .din(din),
        .dout(dout),
        .full(full),
        .empty(empty)
    );

    // clock
    always begin
        clk = 0; #5;
        clk = 1; #5;
    end

    integer i;

    initial begin
        rst = 1;
        wr_en = 0;
        rd_en = 0;
        din = 0;

        #20;
        rst = 0;

        // WRITE 8 values
        for (i=0; i<8; i=i+1) begin
            @(posedge clk);
            wr_en = 1;
            din = i;
        end

        @(posedge clk);
        wr_en = 0;

        // READ 8 values
        for (i=0; i<8; i=i+1) begin
            @(posedge clk);
            rd_en = 1;
        end

        @(posedge clk);
        rd_en = 0;

        #50;
        $finish;
    end

endmodule