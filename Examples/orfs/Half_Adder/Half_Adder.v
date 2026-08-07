module Half_Adder (cout,
    in1,
    in2,
    sum);
 output cout;
 input in1;
 input in2;
 output sum;

 wire net3;
 wire net1;
 wire net2;
 wire net4;

 sky130_fd_sc_hd__ha_1 _0_ (.A(net1),
    .B(net2),
    .COUT(net3),
    .SUM(net4));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input1 (.A(in1),
    .X(net1));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input2 (.A(in2),
    .X(net2));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output3 (.A(net3),
    .X(cout));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output4 (.A(net4),
    .X(sum));
endmodule
