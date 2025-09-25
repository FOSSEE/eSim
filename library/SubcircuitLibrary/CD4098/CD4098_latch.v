 module CD4098_latch(
input D,
input C,
input R1,
input R2,
output reg Q);

 

always@(posedge R1 or posedge R2 or posedge C)
begin
if(R1 || R2)
Q<=0;
else
Q<=D;
end
endmodule 

