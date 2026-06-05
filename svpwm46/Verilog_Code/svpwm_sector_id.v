module svpwm_sector_id (
    input clk,
    input rst_n,
    input [15:0] v_alpha,
    input [15:0] v_beta,
    
    output [2:0] sector,
    output [16:0] v_ref1_out,
    output [16:0] v_ref2_out,
    output [16:0] v_ref3_out
);

    // Cast inputs to signed internally to keep the port list Ngveri-safe
    wire signed [15:0] v_alpha_s = v_alpha;
    wire signed [15:0] v_beta_s  = v_beta;

    reg [2:0] sector_reg;
    reg signed [16:0] ref1, ref2, ref3;
    
    reg signed [31:0] alpha_mul;
    reg signed [15:0] beta_half;
    reg signed [15:0] alpha_term;
    reg a, b, c;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ref1 <= 0;
            ref2 <= 0;
            ref3 <= 0;
            sector_reg <= 0;
        end else begin
            // Using blocking assignments (=) to collapse the AST 
            // into a single execution step for Verilator.
            alpha_mul  = v_alpha_s * 32'sd28378;
            beta_half  = v_beta_s >>> 1;
            alpha_term = alpha_mul >>> 15;
            
            ref1 = v_beta_s;
            ref2 = alpha_term - beta_half;
            ref3 = -alpha_term - beta_half;

            a = (ref1 > 0) ? 1'b1 : 1'b0;
            b = (ref2 > 0) ? 1'b1 : 1'b0;
            c = (ref3 > 0) ? 1'b1 : 1'b0;

            case ({c, b, a})
                3'd3: sector_reg = 3'd1;
                3'd1: sector_reg = 3'd2;
                3'd5: sector_reg = 3'd3;
                3'd4: sector_reg = 3'd4;
                3'd6: sector_reg = 3'd5;
                3'd2: sector_reg = 3'd6;
                default: sector_reg = 3'd0;
            endcase
        end
    end

    // Assign final outputs
    assign sector = sector_reg;
    assign v_ref1_out = ref1;
    assign v_ref2_out = ref2;
    assign v_ref3_out = ref3;

endmodule