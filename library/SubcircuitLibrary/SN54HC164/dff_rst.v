module dff_rst(d,rst,clk,q);
input d,clk,rst;
output reg q;
always @(posedge clk) begin
if(rst) begin
q<=1'b0;
end
else begin
q<=d;
end
end
endmodule