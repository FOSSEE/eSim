// =============================================================================
// bldc_commutator.v
// =============================================================================

module bldc_commutator (
    input wire enable,
    input wire fault_n,
    input wire [2:0] hall_state,
    
    // Inputs coming directly from your existing PWM block in KiCad
    input wire master_pwm_h,
    input wire master_pwm_l,
    
    // 6-Channel Inverter Output
    output wire ah,
    output wire al,
    output wire bh,
    output wire bl,
    output wire ch,
    output wire cl,
    
    output wire hall_error
);

    // Master Safety Gate
    wire safe = enable & fault_n;

    // -------------------------------------------------------------------------
    // Sector Decoding 
    // -------------------------------------------------------------------------
    // Active Sectors (Where high/low PWM is injected)
    wire act_a = safe & ((hall_state == 3'b101) | (hall_state == 3'b100));
    wire act_b = safe & ((hall_state == 3'b110) | (hall_state == 3'b010));
    wire act_c = safe & ((hall_state == 3'b011) | (hall_state == 3'b001));

    // Return Sectors (Where low-side MOSFET is clamped completely ON)
    wire ret_a = safe & ((hall_state == 3'b010) | (hall_state == 3'b011));
    wire ret_b = safe & ((hall_state == 3'b001) | (hall_state == 3'b101));
    wire ret_c = safe & ((hall_state == 3'b100) | (hall_state == 3'b110));

    // -------------------------------------------------------------------------
    // Output Multiplexers
    // -------------------------------------------------------------------------
    // Phase A
    assign ah = act_a ? master_pwm_h : 1'b0;
    assign al = act_a ? master_pwm_l : (ret_a ? 1'b1 : 1'b0);

    // Phase B
    assign bh = act_b ? master_pwm_h : 1'b0;
    assign bl = act_b ? master_pwm_l : (ret_b ? 1'b1 : 1'b0);

    // Phase C
    assign ch = act_c ? master_pwm_h : 1'b0;
    assign cl = act_c ? master_pwm_l : (ret_c ? 1'b1 : 1'b0);

    // Hardware Sensor Fault Detection (000 or 111)
    assign hall_error = (hall_state == 3'b000) | (hall_state == 3'b111);

endmodule