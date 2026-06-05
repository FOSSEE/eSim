module svpwm_dwell_time (
    input clk,
    input rst_n,
    input [2:0] sector,
    input [16:0] v_ref1,
    input [16:0] v_ref2,
    input [16:0] v_ref3,
    output [15:0] t1_out,
    output [15:0] t2_out,
    output [15:0] t0_out
);

    parameter DATA_WIDTH = 16;
    parameter PWM_HALF_PERIOD = 16'd500;

    reg [15:0] t1_reg, t2_reg, t0_reg;
    reg signed [17:0] t1_raw, t2_raw;
    reg [17:0] t_sum;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            t1_reg <= 0;
            t2_reg <= 0;
            t0_reg <= 0;
        end else begin
            // 1. Route based on sector using blocking assignments
            case (sector)
                3'd1: begin t1_raw = v_ref2;  t2_raw = v_ref1;  end
                3'd2: begin t1_raw = -v_ref2; t2_raw = -v_ref3; end
                3'd3: begin t1_raw = v_ref1;  t2_raw = v_ref3;  end
                3'd4: begin t1_raw = -v_ref1; t2_raw = -v_ref2; end
                3'd5: begin t1_raw = v_ref3;  t2_raw = -v_ref1; end
                3'd6: begin t1_raw = -v_ref3; t2_raw = v_ref2;  end
                default: begin t1_raw = 0; t2_raw = 0; end
            endcase

            // 2. Sum and saturate
            t_sum = t1_raw + t2_raw;

            if (t_sum > PWM_HALF_PERIOD) begin
                t1_reg <= (t1_raw > PWM_HALF_PERIOD) ? PWM_HALF_PERIOD : t1_raw[15:0];
                t2_reg <= (t2_raw > PWM_HALF_PERIOD) ? PWM_HALF_PERIOD : t2_raw[15:0];
                t0_reg <= 0; 
            end else begin
                t1_reg <= t1_raw[15:0];
                t2_reg <= t2_raw[15:0];
                t0_reg <= PWM_HALF_PERIOD - t_sum[15:0];
            end
        end
    end

    assign t1_out = t1_reg;
    assign t2_out = t2_reg;
    assign t0_out = t0_reg;

endmodule