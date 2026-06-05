// ==============================================================================
// hbridge_router.v 
// ==============================================================================

module hbridge_router (
    input wire pwm_a_h,
    input wire pwm_a_l,
    input wire dir_a,
    input wire pwm_b_h,
    input wire pwm_b_l,
    input wire dir_b,
    
    output wire a_top_left,
    output wire a_bot_right,
    output wire a_top_right,
    output wire a_bot_left,
    
    output wire b_top_left,
    output wire b_bot_right,
    output wire b_top_right,
    output wire b_bot_left
);

    // --------------------------------------------------------
    // Coil A Logic Steering
    // --------------------------------------------------------
    wire dir_a_inv = ~dir_a;

    // Left Leg gets PWM during Forward, held LOW during Reverse
    assign a_top_left  = pwm_a_h & dir_a;
    assign a_bot_left  = (pwm_a_l & dir_a) | dir_a_inv; // Held ON during reverse
    
    // Right Leg gets PWM during Reverse, held LOW during Forward
    assign a_top_right = pwm_a_h & dir_a_inv;
    assign a_bot_right = (pwm_a_l & dir_a_inv) | dir_a; // Held ON during forward

    // --------------------------------------------------------
    // Coil B Logic Steering
    // --------------------------------------------------------
    wire dir_b_inv = ~dir_b;

    // Left Leg gets PWM during Forward, held LOW during Reverse
    assign b_top_left  = pwm_b_h & dir_b;
    assign b_bot_left  = (pwm_b_l & dir_b) | dir_b_inv; // Held ON during reverse
    
    // Right Leg gets PWM during Reverse, held LOW during Forward
    assign b_top_right = pwm_b_h & dir_b_inv;
    assign b_bot_right = (pwm_b_l & dir_b_inv) | dir_b; // Held ON during forward

endmodule