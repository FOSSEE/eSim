`timescale 1ns/1ps

module tb_freq_div2;

reg clk;
reg rst;
wire clk_div2;

real t1_in, t2_in, period_in;
real t1_out, t2_out, period_out;
real freq_in, freq_out;

freq_div2 DUT (
    .clk(clk),
    .rst(rst),
    .clk_div2(clk_div2)
);

//
// Generate 100 MHz clock (10 ns period)
//
initial begin
    clk = 0;
    forever #5 clk = ~clk;
end

//
// Reset
//
initial begin
    rst = 1;
    #20;
    rst = 0;
end

//
// Measure INPUT frequency
//
initial begin
    @(posedge clk);
    t1_in = $realtime;
    @(posedge clk);
    t2_in = $realtime;

    period_in = t2_in - t1_in;
    freq_in = 1000.0 / period_in;

    $display("INPUT CLOCK:");
    $display("Period = %0.2f ns", period_in);
    $display("Frequency = %0.2f MHz\n", freq_in);
end

//
// Measure OUTPUT frequency
//
initial begin
    @(negedge rst);      // wait reset release
    @(posedge clk_div2);
    t1_out = $realtime;
    @(posedge clk_div2);
    t2_out = $realtime;

    period_out = t2_out - t1_out;
    freq_out = 1000.0 / period_out;

    $display("OUTPUT CLOCK (DIV2):");
    $display("Period = %0.2f ns", period_out);
    $display("Frequency = %0.2f MHz\n", freq_out);
end

//
// Finish
//
initial begin
    #200;
    $finish;
end

endmodule