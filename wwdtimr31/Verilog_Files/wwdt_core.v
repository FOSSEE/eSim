// =============================================================================
// wwdt_core.v Automotive-Grade Windowed Watchdog Timer (WWDT)
// =============================================================================

module wwdt_core (
    input  wire clk,
    input  wire rst_n,
    input  wire enable,
    input  wire [7:0] timeout_val,
    input  wire [7:0] window_val,
    input  wire [7:0] feed_data,
    input  wire feed_en,
    output reg  wdg_reset,
    output reg  early_warning,
    output reg  window_open
);

    // -------------------------------------------------------------------------
    // Industry-standard magic key for watchdog feed validation
    // -------------------------------------------------------------------------
    localparam VALID_FEED_KEY = 8'hA5;
    localparam EWI_MARGIN = 8'd5;

    reg [7:0] counter;
    reg       active;
    reg       feed_en_prev;

    // -------------------------------------------------------------------------
    // Edge detection for the feed strobe (purely combinational, used inside
    // the clocked block so it samples registered feed_en_prev — no glitch risk)
    // -------------------------------------------------------------------------
    wire feed_pulse = (feed_en && !feed_en_prev);

    // -------------------------------------------------------------------------
    // Main clocked state machine
    // -------------------------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            counter       <= 8'd255;  // Benign default; overwritten on enable↑
            active        <= 1'b0;
            wdg_reset     <= 1'b0;
            early_warning <= 1'b0;
            feed_en_prev  <= 1'b0;
            window_open   <= 1'b0;
        end else begin
            feed_en_prev <= feed_en;

            // -----------------------------------------------------------------
            // 1. Permanent Enable Latch
            //    Once armed, active can never be cleared by software.
            //    counter is loaded from the hardware-strapped timeout_val pin.
            // -----------------------------------------------------------------
            if (enable && !active) begin
                active      <= 1'b1;
                counter     <= timeout_val;
                window_open <= 1'b0;  
            end

            // -----------------------------------------------------------------
            // 2. Main Watchdog Execution (only when armed)
            // -----------------------------------------------------------------
            if (active) begin

                window_open <= (counter <= window_val) ? 1'b1 : 1'b0;

                if (counter == EWI_MARGIN && !wdg_reset) begin
                    early_warning <= 1'b1;
                end

                // -------------------------------------------------------------
                // Feed Logic (highest priority inside the active block)
                // -------------------------------------------------------------
                if (feed_pulse) begin

                    if (feed_data != VALID_FEED_KEY) begin
                        // FAULT 1: Wrong magic key — runaway / corrupted code
                        wdg_reset <= 1'b1;

                    end else if (counter > window_val || counter == 8'd0) begin
                        wdg_reset <= 1'b1;

                    end else begin
                        // SUCCESS: Correct key, inside the open window.
                        // Reload the countdown for the next service interval.
                        counter       <= timeout_val;
                        early_warning <= 1'b0;

                    end

                // -------------------------------------------------------------
                // Timeout Logic (fires when no feed_pulse and count hits zero)
                // -------------------------------------------------------------
                end else if (counter == 8'd0) begin
                    // FAULT 3: Starvation — watchdog was not fed in time
                    wdg_reset <= 1'b1;

                // -------------------------------------------------------------
                // Normal Countdown
                // Guard: freeze the counter once a fatal fault is latched so
                // the system holds its reset state until hardware rst_n.
                // -------------------------------------------------------------
                end else if (!wdg_reset) begin
                    counter <= counter - 8'd1;
                end

            end // if (active)
        end
    end

endmodule