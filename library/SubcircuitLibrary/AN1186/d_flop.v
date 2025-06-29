module d_flop(d, clk, rst, q);
input d, clk, rst;
output reg q;
always @(posedge clk) begin
	if(rst) begin
		q <= 0;
	end
	else begin
		q <= d;
	end
end
endmodule