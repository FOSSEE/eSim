module advanced_pwm (
    input wire clk,
    input wire rst_n,
    input wire enable,
    input wire fault_n,
    
    input wire [15:0] period,
    input wire [15:0] duty_cycle,
    input wire [7:0] dead_time,
    
    output wire pwm_h,
    output wire pwm_l
);

    // Internal Registers
    reg [15:0] counter;
    reg [7:0]  dt_counter;
    
    // Pipelined PWM tracking
    reg raw_pwm;
    
    reg pwm_h_reg;
    reg pwm_l_reg;
    
    // Assign outputs
    assign pwm_h = pwm_h_reg;
    assign pwm_l = pwm_l_reg;

    //Safety Guard 
    wire [15:0] safe_duty = (duty_cycle > period) ? period : duty_cycle;

    //Combinational raw_pwm calculation
    wire raw_pwm_next = (counter < safe_duty);

    // Time-Base Counter
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter <= 16'd0;
        end else if (enable) begin
            if (counter >= period) begin
                counter <= 16'd0;
            end else begin
                counter <= counter + 16'd1;
            end
        end
    end

    // Dead-Time Generator & Fault Trip-Zone
    always @(posedge clk or negedge rst_n or negedge fault_n) begin
        if (!rst_n) begin
            raw_pwm      <= 1'b0;
            dt_counter   <= 8'd0;
            pwm_h_reg    <= 1'b0;
            pwm_l_reg    <= 1'b0;
            
        end else if (!fault_n) begin
            // Asynchronous Trip-Zone
            pwm_h_reg <= 1'b0;
            pwm_l_reg <= 1'b0;
	    dt_counter <= 8'd0;
	    raw_pwm <= 1'b0;
            
        end else if (!enable) begin
            // Paused State
            pwm_h_reg <= 1'b0;
            pwm_l_reg <= 1'b0;
            
        end else begin
            // Standard Operation
            raw_pwm      <= raw_pwm_next;

            //Edge Detection
            if (raw_pwm_next != raw_pwm) begin
                dt_counter <= 8'd0; 
                pwm_h_reg  <= 1'b0;
                pwm_l_reg  <= 1'b0;
                
          
            end else if (dt_counter < dead_time) begin
                dt_counter <= dt_counter + 8'd1;
                pwm_h_reg  <= 1'b0;
                pwm_l_reg  <= 1'b0;
                
            end else begin
                // Output signals
                pwm_h_reg <= raw_pwm_next;
                pwm_l_reg <= ~raw_pwm_next;
            end
        end
    end

endmodule