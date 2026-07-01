module FullAdder (cin,
    cout,
    in1,
    in2,
    sum);
 input cin;
 output cout;
 input in1;
 input in2;
 output sum;

 wire net1;
 wire net4;
 wire net2;
 wire net3;
 wire net5;

 sky130_fd_sc_hd__fa_1 _0_ (.A(net2),
    .B(net3),
    .CIN(net1),
    .COUT(net4),
    .SUM(net5));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input1 (.A(cin),
    .X(net1));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input2 (.A(in1),
    .X(net2));
 sky130_fd_sc_hd__clkdlybuf4s50_1 input3 (.A(in2),
    .X(net3));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output4 (.A(net4),
    .X(cout));
 sky130_fd_sc_hd__clkdlybuf4s50_1 output5 (.A(net5),
    .X(sum));
endmodule
