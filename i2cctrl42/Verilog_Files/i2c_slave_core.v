// =============================================================================
// i2c_slave_core.v - I2C Slave
// =============================================================================
module i2c_slave_core (
    clk, rst_n, my_addr, tx_data, scl_in, sda_in,
    sda_gate_out, rx_data, rx_valid
);

    // 1. Inputs
    input clk;
    input rst_n;
    input [6:0] my_addr;
    input [7:0] tx_data;
    input scl_in;
    input sda_in;

    // 2. Outputs
    output sda_gate_out;
    output [7:0] rx_data;
    output rx_valid;

    // 3. Registers
    reg sda_gate_out;
    reg [7:0] rx_data;
    reg rx_valid;

    // State Machine States
    localparam IDLE         = 4'd0;
    localparam RX_ADDR      = 4'd1;
    localparam ACK_ADDR     = 4'd2;
    localparam RX_DATA      = 4'd3;
    localparam ACK_RX       = 4'd4;
    localparam ACK_RX_HOLD  = 4'd5;  // F-04: hold ACK for full SCL period
    localparam TX_DATA      = 4'd6;
    localparam ACK_TX       = 4'd7;

    reg [3:0] state;
    reg [7:0] shift_reg;
    reg [3:0] bit_count;
    reg is_read;
    reg ack_fall; // F-05: ACK_TX transition guard ONLY (not dual-use)
    reg bit_hold; // F-05: extra edge hold after bit0 in TX_DATA ONLY

    // Registers to store the previous pin state for edge detection
    reg scl_prev, sda_prev;

    // =====================================================================
    // OVERSAMPLING & STATE MACHINE
    // Uses the fast system clock to safely detect SCL/SDA edges without
    // relying on the noisy physical bus to clock the flip-flops directly.
    // =====================================================================
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= IDLE;
            sda_gate_out <= 1'b0;
            rx_data <= 8'd0;
            rx_valid <= 1'b0;
            scl_prev <= 1'b1;
            sda_prev <= 1'b1;
            ack_fall <= 1'b0;
            bit_hold <= 1'b0;
        end else begin
            // Shift historical values to detect rising/falling edges
            scl_prev <= scl_in;
            sda_prev <= sda_in;
            rx_valid <= 1'b0; 

            // 1. Detect START Condition: SDA falls while SCL is HIGH
            if (scl_in == 1'b1 && sda_prev == 1'b1 && sda_in == 1'b0) begin
                state <= RX_ADDR;
                bit_count <= 4'd7;
                sda_gate_out <= 1'b0;
            end
            
            // 2. Detect STOP Condition: SDA rises while SCL is HIGH
            else if (scl_in == 1'b1 && sda_prev == 1'b0 && sda_in == 1'b1) begin
                state <= IDLE;
                sda_gate_out <= 1'b0;
            end
            
            // 3. Detect SCL RISING EDGE (Time to sample data from the bus)
            else if (scl_prev == 1'b0 && scl_in == 1'b1) begin
                case (state)
                    RX_ADDR: begin
                        shift_reg[bit_count] <= sda_in;
                        if (bit_count == 0) state <= ACK_ADDR;
                        else bit_count <= bit_count - 1;
                    end
                    
                    RX_DATA: begin
                        shift_reg[bit_count] <= sda_in;
                        if (bit_count == 0) state <= ACK_RX;
                        else bit_count <= bit_count - 1;
                    end
                endcase
            end
            
            // 4. Detect SCL FALLING EDGE (Time to change our output data)
            else if (scl_prev == 1'b1 && scl_in == 1'b0) begin
                case (state)
                    ACK_ADDR: begin
                        if (!ack_fall) begin
                            // F0: Assert ACK, stay in ACK_ADDR
                            // Master is releasing SDA on this same edge
                            if (shift_reg[7:1] == my_addr) begin
                                sda_gate_out <= 1'b1; // Pull bus LOW to ACK!
                                is_read <= shift_reg[0];
                                ack_fall <= 1'b1;
                            end else begin
                                sda_gate_out <= 1'b0;
                                state <= IDLE;
                            end
                        end else begin
                            // F1: Release ACK and enter data phase
                            ack_fall <= 1'b0;
                            if (is_read) begin
                                // Drive bit7 immediately on F1 so master can
                                // sample it at the very next SCL rising edge.
                                // TX_DATA will continue from bit6 downward.
                                shift_reg    <= tx_data;
                                sda_gate_out <= ~tx_data[7];
                                bit_count    <= 4'd6;
                                state        <= TX_DATA;
                            end else begin
                                sda_gate_out <= 1'b0;
                                bit_count    <= 4'd7;
                                state        <= RX_DATA;
                            end
                        end
                    end
                    
                    TX_DATA: begin
                        if (!bit_hold) begin
                            // Drive current bit
                            sda_gate_out <= ~shift_reg[bit_count];
                            if (bit_count == 0)
                                bit_hold <= 1'b1; // F-05: hold bit0 one extra edge
                            else
                                bit_count <= bit_count - 1;
                        end else begin
                            // Extra edge after bit0: release SDA, go to ACK_TX
                            sda_gate_out <= 1'b0;
                            bit_hold <= 1'b0;
                            state <= ACK_TX;
                        end
                    end

                    ACK_TX: begin
                        sda_gate_out <= 1'b0; // Listen for Master's ACK
                        state <= IDLE; // Transaction complete
                    end

                    ACK_RX: begin
                        sda_gate_out <= 1'b1; // Slave ACKs the received data
                        rx_data <= shift_reg; // Latch received byte
                        rx_valid <= 1'b1;     // Pulse valid flag
                        state <= ACK_RX_HOLD; // F-04: hold ACK for full SCL period
                    end

                    // F-04: sda_gate_out stays 1 through entire SCL HIGH window.
                    // Master samples SDA LOW (ACK) on SCL rising edge between
                    // ACK_RX and ACK_RX_HOLD. Release on next SCL falling edge.
                    ACK_RX_HOLD: begin
                        sda_gate_out <= 1'b0;
                        state <= IDLE;
                    end
                    
                    default: sda_gate_out <= 1'b0; 
                endcase
            end
        end
    end
endmodule