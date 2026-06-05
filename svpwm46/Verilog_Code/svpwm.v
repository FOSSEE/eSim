// ============================================================================
// svpwm.v
// ============================================================================

module svpwm (
    input clk,
    input rst_n,
    input [15:0] v_alpha,
    input [15:0] v_beta,
    
    output u_high, output u_low,
    output v_high, output v_low,
    output w_high, output w_low
);

    // Internal interconnect wires hardcoded to match sub-modules
    wire [2:0] sector;
    wire signed [16:0] v_ref1, v_ref2, v_ref3;
    wire [15:0] t1, t2, t0;
    wire u_ideal, v_ideal, w_ideal;

    // Instantiate Sector Identification
    svpwm_sector_id U1_SECTOR (
        .clk(clk),
        .rst_n(rst_n),
        .v_alpha(v_alpha),
        .v_beta(v_beta),
        .sector(sector),
        .v_ref1_out(v_ref1),
        .v_ref2_out(v_ref2),
        .v_ref3_out(v_ref3)
    );

    // Instantiate Dwell Time Calculation
    svpwm_dwell_time U2_DWELL (
        .clk(clk),
        .rst_n(rst_n),
        .sector(sector),
        .v_ref1(v_ref1),
        .v_ref2(v_ref2),
        .v_ref3(v_ref3),
        .t1_out(t1),
        .t2_out(t2),
        .t0_out(t0)
    );

    // Instantiate PWM Generator
    svpwm_pwm_gen U3_PWM (
        .clk(clk),
        .rst_n(rst_n),
        .sector(sector),
        .t1(t1),
        .t2(t2),
        .t0(t0),
        .u_ideal(u_ideal),
        .v_ideal(v_ideal),
        .w_ideal(w_ideal)
    );

    // Instantiate Dead-Time Insertion
    svpwm_dead_time U4_DEADTIME (
        .clk(clk),
        .rst_n(rst_n),
        .u_ideal(u_ideal),
        .v_ideal(v_ideal),
        .w_ideal(w_ideal),
        .u_high(u_high),
        .u_low(u_low),
        .v_high(v_high),
        .v_low(v_low),
        .w_high(w_high),
        .w_low(w_low)
    );

endmodule

// ============================================================================
// SUB MODULE 1: SECTOR IDENTIFICATION
// ============================================================================
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

// ============================================================================
// SUB MODULE 2: DWELL TIME CALCULATION
// ============================================================================
module svpwm_dwell_time (
    input clk,
    input rst_n,
    input [2:0] sector,
    input signed [16:0] v_ref1,
    input signed [16:0] v_ref2,
    input signed [16:0] v_ref3,
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

// ============================================================================
// SUB MODULE 3: CENTER-ALIGNED PWM GENERATOR
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


// ============================================================================
// SUB MODULE 4: DEAD-TIME INSERTION
// ============================================================================
module svpwm_dead_time (
    input clk,
    input rst_n,
    input u_ideal, 
    input v_ideal, 
    input w_ideal,
    output reg u_high, 
    output reg u_low,
    output reg v_high, 
    output reg v_low,
    output reg w_high, 
    output reg w_low
);

    parameter DEAD_TIME_TICKS = 8'd2;

    reg [7:0] counter_u, counter_v, counter_w;
    reg u_ideal_d, v_ideal_d, w_ideal_d;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            u_ideal_d <= 0; v_ideal_d <= 0; w_ideal_d <= 0;
            counter_u <= 0; counter_v <= 0; counter_w <= 0;
            u_high <= 0; u_low <= 0; v_high <= 0; v_low <= 0; w_high <= 0; w_low <= 0;
        end else begin
            u_ideal_d <= u_ideal; 
            v_ideal_d <= v_ideal; 
            w_ideal_d <= w_ideal;

            if (u_ideal != u_ideal_d) begin
                counter_u <= 0; u_high <= 0; u_low <= 0;
            end else if (counter_u < DEAD_TIME_TICKS) begin
                counter_u <= counter_u + 1; u_high <= 0; u_low <= 0;
            end else begin
                u_high <= u_ideal; u_low <= ~u_ideal;
            end

            if (v_ideal != v_ideal_d) begin
                counter_v <= 0; v_high <= 0; v_low <= 0;
            end else if (counter_v < DEAD_TIME_TICKS) begin
                counter_v <= counter_v + 1; v_high <= 0; v_low <= 0;
            end else begin
                v_high <= v_ideal; v_low <= ~v_ideal;
            end

            if (w_ideal != w_ideal_d) begin
                counter_w <= 0; w_high <= 0; w_low <= 0;
            end else if (counter_w < DEAD_TIME_TICKS) begin
                counter_w <= counter_w + 1; w_high <= 0; w_low <= 0;
            end else begin
                w_high <= w_ideal; w_low <= ~w_ideal;
            end
        end
    end

endmodule