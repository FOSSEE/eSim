module soft_start_limiter (
    input  wire       clk,             // 10 MHz system clock
    input  wire       rst_n,           // Active-low asynchronous reset
    input  wire [7:0] target_duty,     // 8-bit target PWM duty cycle
    input  wire [7:0] ramp_rate_delay, // Delay cycles before each step
    output reg  [7:0] safe_duty_out    // Smoothed 8-bit duty cycle output
);

    // Internal 8-bit counter for the delay loop
    reg [7:0] delay_counter;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Hardware reset: immediately kill the PWM and clear counters
            safe_duty_out <= 8'd0;
            delay_counter <= 8'd0;
        end else begin
            // Condition 1: Ramp Up (Soft-Start)
            if (safe_duty_out < target_duty) begin
                if (delay_counter >= ramp_rate_delay) begin
                    safe_duty_out <= safe_duty_out + 1'b1;
                    delay_counter <= 8'd0;
                end else begin
                    delay_counter <= delay_counter + 1'b1;
                end
            end
            
            // Condition 2: Ramp Down (Soft-Stop / Speed Reduction)
            else if (safe_duty_out > target_duty) begin
                if (delay_counter >= ramp_rate_delay) begin
                    safe_duty_out <= safe_duty_out - 1'b1;
                    delay_counter <= 8'd0;
                end else begin
                    delay_counter <= delay_counter + 1'b1;
                end
            end
            
            // Condition 3: Steady State (Target Reached)
            else begin
                delay_counter <= 8'd0; // Reset counter to be ready for the next change
            end
        end
    end

endmodule