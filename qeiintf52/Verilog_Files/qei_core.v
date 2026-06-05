// =============================================================================
// qei_core.v - Quadrature Encoder Interface (4x Evaluation Mode)
// =============================================================================

module qei_core (
    input  wire        clk,
    input  wire        rst_n,
    input  wire        enable,
    input  wire        pha_in,
    input  wire        phb_in,
    input  wire        idx_in,
    input  wire [15:0] max_count,
    
    output reg  [15:0] pos_count,
    output reg         direction,
    output reg         sync_error
);

    // -------------------------------------------------------------------------
    // 1. Double-Flop Synchronizers (Anti-Metastability for Analog Inputs)
    // -------------------------------------------------------------------------
    reg pha_sync1, pha_sync2;
    reg phb_sync1, phb_sync2;
    reg idx_sync1, idx_sync2;

    // Previous state registers for Edge Detection
    reg pha_prev;
    reg phb_prev;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pha_sync1 <= 1'b0; pha_sync2 <= 1'b0;
            phb_sync1 <= 1'b0; phb_sync2 <= 1'b0;
            idx_sync1 <= 1'b0; idx_sync2 <= 1'b0;
            pha_prev  <= 1'b0; phb_prev  <= 1'b0;
        end else begin
            // Shift data through the 2-stage synchronizer
            pha_sync1 <= pha_in; pha_sync2 <= pha_sync1;
            phb_sync1 <= phb_in; phb_sync2 <= phb_sync1;
            idx_sync1 <= idx_in; idx_sync2 <= idx_sync1;
            
            // Store the previous synchronized value for edge detection
            pha_prev <= pha_sync2;
            phb_prev <= phb_sync2;
        end
    end

    // -------------------------------------------------------------------------
    // 2. Main QEI Decoding State Machine
    // -------------------------------------------------------------------------
    wire a_edge = (pha_sync2 ^ pha_prev);
    wire b_edge = (phb_sync2 ^ phb_prev);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pos_count  <= 16'd0;
            direction  <= 1'b0;
            sync_error <= 1'b0;
        end else if (enable) begin
            
            // Reset position on Index Pulse (Zero-marker hit)
            if (idx_sync2) begin
                pos_count <= 16'd0;
                sync_error <= 1'b0; // Clear error on index reset
            end 
            else begin
                // -------------------------------------------------------------
                // 4x Quadrature Decoding Logic
                // -------------------------------------------------------------
                if (a_edge && b_edge) begin
                    // ILLEGAL STATE: Both phases transitioned simultaneously. 
                    // Indicates severe noise, vibration, or sensor failure.
                    sync_error <= 1'b1;
                end 
                else if (a_edge || b_edge) begin
                    // Industry Standard 4x Direction Logic:
                    // Forward if: (A ^ B_prev) is true
                    // This covers all 4 edges correctly.
                    if (pha_sync2 ^ phb_prev) begin
                        direction <= 1'b1; // FORWARD
                        if (pos_count < max_count) 
                            pos_count <= pos_count + 16'd1;
                        else 
                            pos_count <= 16'd0;
                    end 
                    else begin
                        direction <= 1'b0; // REVERSE
                        if (pos_count > 16'd0) 
                            pos_count <= pos_count - 16'd1;
                        else 
                            pos_count <= max_count;
                    end
                end
            end
        end
    end

endmodule