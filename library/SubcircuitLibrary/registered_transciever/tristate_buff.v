module tristate_buff(input wire a, input wire enable, output wire y);
assign y = (enable) ? a : 1'bz;
endmodule