// =============================================================================
// i2c_master_core.v I2C Master
// =============================================================================

module i2c_master_core (
    clk, rst_n, enable, rw_flag, addr, tx_data, sda_in,
    sda_gate, scl_gate, rx_data, rx_valid, busy
);

    input        clk;
    input        rst_n;
    input        enable;
    input        rw_flag;
    input  [6:0] addr;
    input  [7:0] tx_data;
    input        sda_in;

    output       sda_gate;
    output       scl_gate;
    output [7:0] rx_data;
    output       rx_valid;
    output       busy;

    reg        sda_gate;
    reg [7:0]  rx_data;
    reg        rx_valid;
    reg        busy;

    localparam IDLE        = 4'd0;
    localparam DELAY_START = 4'd1;
    localparam START       = 4'd2;
    localparam SEND_ADDR   = 4'd3;
    localparam ACK_ADDR    = 4'd4;
    localparam TX_DATA     = 4'd5;
    localparam ACK_TX      = 4'd6;
    localparam RX_DATA     = 4'd7;
    localparam ACK_RX      = 4'd8;
    localparam PRE_STOP    = 4'd9;
    localparam STOP        = 4'd10;

    // F-09: parameterised divider — no magic numbers
    // Default: 1 MHz sys-clk, CLK_DIV=50 -> 10 kHz SCL
    localparam CLK_DIV   = 50;
    localparam MID_POINT = CLK_DIV/2 - 1;  // = 24 for CLK_DIV=50

    reg [3:0]  state;
    reg [7:0]  shift_reg;
    reg [7:0]  tx_data_latch;
    reg [3:0]  bit_count;
    reg [7:0]  clk_div;
    reg        scl_internal;
    reg        scl_prev;
    reg        is_read;
    reg        done_latch;
    reg        scl_en;
    reg [1:0]  delay_count;
    reg        ack_fall;
    reg [5:0]  mid_count;
    reg        mid_armed;

    // F-01: enable falling-edge detection for done_latch re-arm
    reg        enable_prev;
    wire       enable_fall = enable_prev & ~enable;

    assign scl_gate = scl_en ? ~scl_internal : 1'b0;

    wire scl_rising  = ( scl_internal && !scl_prev);
    wire scl_falling = (!scl_internal &&  scl_prev);
    wire mid_high    = (mid_armed && mid_count == MID_POINT[5:0]);

    // =========================================================================
    // BLOCK 1 - SCL edge history
    // =========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) scl_prev <= 1'b1;
        else        scl_prev <= scl_internal;
    end

    // =========================================================================
    // BLOCK 2a - F-01: enable edge detector
    // Clears done_latch on falling edge of enable so master can retrigger.
    // =========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            enable_prev <= 1'b0;
        end else begin
            enable_prev <= enable;
            if (enable_fall)
                done_latch <= 1'b0;
        end
    end

    // =========================================================================
    // BLOCK 2 - Clock divider (1 MHz sys clk -> 10 kHz SCL)
    // F-03: gated by scl_en so divider freezes when scl_en=0 in PRE_STOP,
    //       preventing a ghost SCL toggle from reaching the NMOS gate.
    // F-09: uses CLK_DIV localparam instead of magic number 8'd49.
    // =========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            clk_div      <= 8'd0;
            scl_internal <= 1'b1;
        end else if (scl_en && ((enable && !done_latch) || state != IDLE)) begin
            if (clk_div >= (CLK_DIV - 1)) begin
                scl_internal <= ~scl_internal;
                clk_div      <= 8'd0;
            end else
                clk_div <= clk_div + 1;
        end else begin
            scl_internal <= 1'b1;
            clk_div      <= 8'd0;
        end
    end

    // =========================================================================
    // BLOCK 3 - Mid-HIGH pulse generator (for START condition only)
    // Fires 25 sys-clks after SCL rising edge = middle of HIGH phase
    // =========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            mid_count <= 6'd0;
            mid_armed <= 1'b0;
        end else begin
            if (scl_rising) begin
                mid_count <= 6'd0;
                mid_armed <= 1'b1;
            end else if (mid_armed) begin
                if (mid_count == MID_POINT[5:0])
                    mid_armed <= 1'b0;
                else
                    mid_count <= mid_count + 1;
            end
        end
    end

    // =========================================================================
    // BLOCK 4 - State machine
    // =========================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state         <= IDLE;
            sda_gate      <= 1'b0;
            busy          <= 1'b0;
            rx_valid      <= 1'b0;
            rx_data       <= 8'd0;
            done_latch    <= 1'b0;
            is_read       <= 1'b0;
            shift_reg     <= 8'd0;
            tx_data_latch <= 8'd0;
            bit_count     <= 4'd0;
            scl_en        <= 1'b0;
            delay_count   <= 2'd0;
            ack_fall      <= 1'b0;
        end else begin
            rx_valid <= 1'b0;

            case (state)

                // -------------------------------------------------------------
                IDLE: begin
                    sda_gate    <= 1'b0;
                    scl_en      <= 1'b0;
                    delay_count <= 2'd0;
                    ack_fall    <= 1'b0;
                    if (enable && !done_latch) begin
                        busy   <= 1'b1;
                        scl_en <= 1'b1;
                        state  <= DELAY_START;
                    end
                end

                // -------------------------------------------------------------
                // Wait 3 SCL rising edges - ADC bridges fully settle
                DELAY_START: begin
                    if (scl_rising) begin
                        delay_count <= delay_count + 1;
                        if (delay_count == 2'd2) begin
                            is_read       <= rw_flag;
                            shift_reg     <= {addr, rw_flag};
                            tx_data_latch <= tx_data;
                            state         <= START;
                        end
                    end
                end

                // -------------------------------------------------------------
                // START: SDA falls at mid-point of SCL HIGH phase
                // SDA falls while SCL HIGH = valid I2C START condition OK
                START: begin
                    if (mid_high) begin
                        sda_gate  <= 1'b1;  // NMOS ON -> SDA LOW while SCL HIGH
                        bit_count <= 4'd7;  // Start from MSB
                        state     <= SEND_ADDR;
                    end
                end

                // -------------------------------------------------------------
                // SEND_ADDR: transmit all 8 bits of {addr,rw} MSB first.
                // Each bit driven on SCL falling edge.
                // bit_count counts 7 down to 0.
                // After bit0 is driven, transition to ACK_ADDR.
                SEND_ADDR: begin
                    if (scl_falling) begin
                        // Drive current bit (NMOS inversion: send bit B -> sda_gate=~B)
                        sda_gate <= ~shift_reg[bit_count];
                        if (bit_count == 0) begin
                            ack_fall <= 1'b0;
                            state    <= ACK_ADDR;
                        end else
                            bit_count <= bit_count - 1;
                    end
                end

                // -------------------------------------------------------------
                // ACK_ADDR - 2 falling edges, locked to slave timing:
                //
                // F0 (ack_fall=0):
                //   Master releases SDA (sda_gate=0, NMOS OFF, bus HIGH)
                //   Slave on same falling edge: ACK_ADDR state detected,
                //   asserts sda_gate_out=1 -> pulls bus LOW = ACK OK
                //   Slave moves to RX_DATA, bit_count=7
                //
                // F1 (ack_fall=1):
                //   Master drives tx_data[7] - same edge slave expects bit7 OK
                //   Transition to TX_DATA, bit_count=6
                ACK_ADDR: begin
                    if (scl_falling) begin
                        if (!ack_fall) begin
                            // F0: Release SDA for slave ACK
                            sda_gate <= 1'b0;
                            ack_fall <= 1'b1;
                        end else begin
                            // F1: Start data transmission
                            ack_fall <= 1'b0;
                            if (!is_read) begin
                                shift_reg <= tx_data_latch;
                                sda_gate  <= ~tx_data_latch[7]; // Drive bit7
                                bit_count <= 4'd6;
                                state     <= TX_DATA;
                            end else begin
                                sda_gate  <= 1'b0;
                                bit_count <= 4'd7;
                                state     <= RX_DATA;
                            end
                        end
                    end
                end

                // -------------------------------------------------------------
                // TX_DATA: drive bits 6 down to 0 on falling edges.
                // (bit7 already driven in ACK_ADDR F1)
                // After bit0 driven, transition to ACK_TX.
                TX_DATA: begin
                    if (scl_falling) begin
                        sda_gate <= ~shift_reg[bit_count];
                        if (bit_count == 0) begin
                            ack_fall <= 1'b0;
                            state    <= ACK_TX;
                        end else
                            bit_count <= bit_count - 1;
                    end
                end

                // -------------------------------------------------------------
                // ACK_TX - 2 falling edges, locked to slave ACK_RX timing:
                //
                // F0 (ack_fall=0):
                //   Master releases SDA (sda_gate=0)
                //   Slave on same falling edge: ACK_RX state detected,
                //   asserts sda_gate_out=1 -> bus LOW = ACK OK
                //   Slave moves to IDLE
                //
                // F1 (ack_fall=1):
                //   ACK window closed.
                //   Hold SDA LOW (sda_gate=1) for STOP setup -> PRE_STOP
                ACK_TX: begin
                    if (scl_falling) begin
                        if (!ack_fall) begin
                            // F0: Release SDA for slave ACK
                            sda_gate <= 1'b0;
                            ack_fall <= 1'b1;
                        end else begin
                            // F1: ACK done, prepare STOP
                            ack_fall <= 1'b0;
                            sda_gate <= 1'b1;  // NMOS ON -> hold SDA LOW
                            state    <= PRE_STOP;
                        end
                    end
                end

                // -------------------------------------------------------------
                // PRE_STOP:
                //   sda_gate=1 -> NMOS ON -> SDA bus LOW (setup)
                //   scl_en=0   -> SCL NMOS OFF -> SCL rises HIGH via pull-up
                //   Once scl_internal=1 (SCL confirmed HIGH) -> STOP
                PRE_STOP: begin
                    sda_gate <= 1'b1;  // Hold SDA LOW
                    scl_en   <= 1'b0;  // Release SCL -> pull-up takes it HIGH
                    if (scl_internal == 1'b1)
                        state <= STOP;
                end

                // -------------------------------------------------------------
                // STOP:
                //   SCL is HIGH (confirmed by PRE_STOP)
                //   SDA was LOW (sda_gate=1)
                //   Release SDA: sda_gate=0 -> NMOS OFF -> pull-up -> SDA HIGH
                //   SDA rises while SCL HIGH = valid I2C STOP condition OK
                STOP: begin
                    sda_gate   <= 1'b0;  // Release SDA HIGH = STOP OK
                    done_latch <= 1'b1;
                    busy       <= 1'b0;
                    state      <= IDLE;
                end

                // -------------------------------------------------------------
                // RX_DATA: sample sda_in on SCL rising edges, MSB first
                RX_DATA: begin
                    sda_gate <= 1'b0;
                    if (scl_rising) begin
                        shift_reg[bit_count] <= sda_in;
                        if (bit_count == 0) begin
                            ack_fall <= 1'b0;
                            state    <= ACK_RX;
                        end else
                            bit_count <= bit_count - 1;
                    end
                end

                // -------------------------------------------------------------
                // ACK_RX: master pulls SDA LOW to ACK received byte.
                // Uses same 2-falling-edge pattern as slave ACK for full
                // SCL period width (matching real-world I2C behaviour).
                //
                // F0 (ack_fall=0):
                //   Assert ACK (sda_gate=1), latch rx_data, pulse rx_valid
                //
                // F1 (ack_fall=1):
                //   Release SDA, hold LOW for STOP setup -> PRE_STOP
                ACK_RX: begin
                    if (scl_falling) begin
                        if (!ack_fall) begin
                            // F0: Assert ACK for full period
                            sda_gate <= 1'b1;  // NMOS ON -> SDA LOW = ACK
                            rx_data  <= shift_reg;
                            rx_valid <= 1'b1;
                            ack_fall <= 1'b1;
                        end else begin
                            // F1: ACK window closed, prepare STOP
                            ack_fall <= 1'b0;
                            sda_gate <= 1'b1;  // Hold SDA LOW for STOP setup
                            state    <= PRE_STOP;
                        end
                    end
                end

                default: state <= IDLE;

            endcase
        end
    end

endmodule