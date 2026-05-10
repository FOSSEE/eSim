module divider (
    input  wire        clk,
    input  wire        rst,
    input  wire        in_valid,
    input  wire [7:0]  dividend,
    input  wire [7:0]  divisor,
    output wire        out_valid,
    output wire [7:0]  quotient,
    output wire [7:0]  remainder
);

    // Pipeline registers
    reg        valid_pipe [0:8];
    reg [7:0]  divisor_pipe [0:8];
    reg [7:0]  quotient_pipe [0:8];
    reg [8:0]  remainder_pipe [0:8];
    reg        div0_pipe [0:8];     // NEW: divide-by-zero pipeline

    // Stage 0 (Input stage)
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            valid_pipe[0]     <= 0;
            quotient_pipe[0]  <= 0;
            remainder_pipe[0] <= 0;
            divisor_pipe[0]   <= 0;
            div0_pipe[0]      <= 0;
        end
        else begin
            valid_pipe[0]     <= in_valid;
            quotient_pipe[0]  <= dividend;
            remainder_pipe[0] <= 0;
            divisor_pipe[0]   <= divisor;
            div0_pipe[0]      <= (divisor == 0);   // detect divide-by-zero
        end
    end

    // Pipeline stages
    genvar s;
    generate
        for (s = 1; s <= 8; s = s + 1) begin : PIPE

            reg [8:0]  rem_shift;
            reg [7:0]  quot_shift;

            always @(posedge clk or posedge rst) begin
                if (rst) begin
                    valid_pipe[s]     <= 0;
                    quotient_pipe[s]  <= 0;
                    remainder_pipe[s] <= 0;
                    divisor_pipe[s]   <= 0;
                    div0_pipe[s]      <= 0;
                end
                else begin
                    valid_pipe[s]   <= valid_pipe[s-1];
                    divisor_pipe[s] <= divisor_pipe[s-1];
                    div0_pipe[s]    <= div0_pipe[s-1];

                    // If divide-by-zero, just propagate
                    if (div0_pipe[s-1]) begin
                        quotient_pipe[s]  <= 0;
                        remainder_pipe[s] <= quotient_pipe[s-1];
                    end
                    else begin
                        // Normal division
                        rem_shift  = {remainder_pipe[s-1][7:0], quotient_pipe[s-1][7]};
                        quot_shift = {quotient_pipe[s-1][6:0], 1'b0};

                        if (rem_shift >= divisor_pipe[s-1]) begin
                            remainder_pipe[s] <= rem_shift - divisor_pipe[s-1];
                            quotient_pipe[s]  <= {quot_shift[7:1], 1'b1};
                        end
                        else begin
                            remainder_pipe[s] <= rem_shift;
                            quotient_pipe[s]  <= {quot_shift[7:1], 1'b0};
                        end
                    end
                end
            end

        end
    endgenerate

    assign out_valid = valid_pipe[8];
    assign quotient  = quotient_pipe[8];
    assign remainder = remainder_pipe[8][7:0];

endmodule