// =============================================================================
// pid_core.v - Discrete Fixed-Point PID Controller
// =============================================================================

module pid_core #(
    // Fractional scaling factor (Right shift by 8 = dividing by 256)
    // This allows Kp, Ki, Kd to act as fractional values (e.g., Kp=128 means 0.5)
    parameter SHIFT_VAL = 8,
    
    // Anti-Windup Limits for the Integral accumulator (32-bit signed)
    parameter signed I_MAX = 32'sd500000,
    parameter signed I_MIN = -32'sd500000,
    
    // Output Clamping Limits (16-bit signed)
    parameter signed OUT_MAX = 16'sd32767,
    parameter signed OUT_MIN = -16'sd32767
)(
    input  wire        clk,
    input  wire        rst_n,
    input  wire        enable,
    
    // Tuning Parameters (Unsigned, treated as fractional numerators)
    input  wire [7:0]  kp,
    input  wire [7:0]  ki,
    input  wire [7:0]  kd,
    
    // Data Inputs
    input  wire signed [15:0] setpoint,
    input  wire signed [15:0] feedback,
    
    // Control Output
    output reg  signed [15:0] control_out
);

    // -------------------------------------------------------------------------
    // Internal State Registers (32-bit to prevent multiplication overflow)
    // -------------------------------------------------------------------------
    reg signed [15:0] prev_error;
    reg signed [31:0] integral;
    
    // Combinational math wires
    wire signed [15:0] error;
    wire signed [31:0] p_term;
    wire signed [31:0] i_term_next;
    wire signed [31:0] d_term;
    wire signed [31:0] pid_total;
    wire signed [31:0] pid_scaled;

    // -------------------------------------------------------------------------
    // The Math Pipeline
    // -------------------------------------------------------------------------
    // 1. Error Calculation
    assign error = setpoint - feedback;
    
    // 2. Proportional: P = Kp * error
    // Note: $signed() ensures the unsigned 8-bit Kp doesn't corrupt the sign bit
    assign p_term = $signed({1'b0, kp}) * error;
    
    // 3. Integral Next State: I_next = I_current + (Ki * error)
    assign i_term_next = integral + ($signed({1'b0, ki}) * error);
    
    // 4. Derivative: D = Kd * (error - prev_error)
    assign d_term = $signed({1'b0, kd}) * (error - prev_error);
    
    // 5. Summation
    assign pid_total = p_term + integral + d_term;
    
    // 6. Fractional Scaling (Bit-shift right to divide)
    assign pid_scaled = pid_total >>> SHIFT_VAL;

    // -------------------------------------------------------------------------
    // Clocked State Machine (Updates & Clamping)
    // -------------------------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            prev_error  <= 16'sd0;
            integral    <= 32'sd0;
            control_out <= 16'sd0;
        end else if (enable) begin
            
            // --- Update History ---
            prev_error <= error;
            
            // --- Integral Anti-Windup Clamping ---
            if (i_term_next > I_MAX)
                integral <= I_MAX;
            else if (i_term_next < I_MIN)
                integral <= I_MIN;
            else
                integral <= i_term_next;
                
            // --- Output Clamping (Saturation) ---
            if (pid_scaled > OUT_MAX)
                control_out <= OUT_MAX;
            else if (pid_scaled < OUT_MIN)
                control_out <= OUT_MIN;
            else
                control_out <= pid_scaled[15:0]; // Safe to truncate after clamp
                
        end
    end

endmodule