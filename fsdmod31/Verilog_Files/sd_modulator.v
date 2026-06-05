// ===========================================================================
// sd_modulator.v
// ===========================================================================

module sd_modulator (
	input wire clk,
	input wire rst_n,
	input wire [7:0] digital_val_in,
	output wire sigma_delta_out
);

// 9-bit accumulator to handle the 8-bit sum + 1-bit overflow
reg [8:0] acc;
always @(posedge clk or negedge rst_n) begin
	if (!rst_n) begin
		acc <= 9'b0;
	end else begin

	// Core Sigma-Delta math: Previous Error + New Input
		acc <= acc[7:0] + digital_val_in;
	end
end

// Direct assignment of the overflow bit to the output
assign sigma_delta_out = acc[8];
endmodule