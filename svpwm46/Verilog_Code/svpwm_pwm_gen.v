// ============================================================================
// svpwm_pwm_gen.v
// ============================================================================

module svpwm_pwm_gen (
    input clk,
    input rst_n,
    input [2:0] sector,
    input [15:0] t1,
    input [15:0] t2,
    input [15:0] t0,
    output u_ideal,
    output v_ideal,
    output w_ideal
);

    parameter DATA_WIDTH = 16;
    parameter PWM_HALF_PERIOD = 16'd500;

    reg [15:0] counter_reg;
    reg dir_reg;
    reg u_reg, v_reg, w_reg;

    reg [15:0] cmp1, cmp2, cmp3;
    reg [15:0] cmp_u, cmp_v, cmp_w;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter_reg <= 0;
            dir_reg <= 1'b1;
            u_reg <= 0;
            v_reg <= 0;
            w_reg <= 0;
        end else begin
            // Calculate compares
            cmp1 = t0 >> 1;               
            cmp2 = (t0 >> 1) + t1;        
            cmp3 = (t0 >> 1) + t1 + t2;   

            // Route compares to phases
            case (sector)
                3'd1: begin cmp_u = cmp1; cmp_v = cmp2; cmp_w = cmp3; end
                3'd2: begin cmp_u = cmp2; cmp_v = cmp1; cmp_w = cmp3; end
                3'd3: begin cmp_u = cmp3; cmp_v = cmp1; cmp_w = cmp2; end
                3'd4: begin cmp_u = cmp3; cmp_v = cmp2; cmp_w = cmp1; end
                3'd5: begin cmp_u = cmp2; cmp_v = cmp3; cmp_w = cmp1; end
                3'd6: begin cmp_u = cmp1; cmp_v = cmp3; cmp_w = cmp2; end
                default: begin cmp_u = PWM_HALF_PERIOD; cmp_v = PWM_HALF_PERIOD; cmp_w = PWM_HALF_PERIOD; end
            endcase

            // Counter Logic
            if (dir_reg == 1'b1) begin
                if (counter_reg >= PWM_HALF_PERIOD - 1) begin
                    counter_reg <= PWM_HALF_PERIOD;
                    dir_reg <= 1'b0; 
                end else begin
                    counter_reg <= counter_reg + 1;
                end
            end else begin
                if (counter_reg <= 1) begin
                    counter_reg <= 0;
                    dir_reg <= 1'b1; 
                end else begin
                    counter_reg <= counter_reg - 1;
                end
            end

            // Output Evaluation
            u_reg <= (counter_reg >= cmp_u) ? 1'b1 : 1'b0;
            v_reg <= (counter_reg >= cmp_v) ? 1'b1 : 1'b0;
            w_reg <= (counter_reg >= cmp_w) ? 1'b1 : 1'b0;
        end
    end

    assign u_ideal = u_reg;
    assign v_ideal = v_reg;
    assign w_ideal = w_reg;

endmodule