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