module tb_divider_8bit_pipeline;

    reg  clk, rst;
    reg  in_valid;
    reg  [7:0] dividend, divisor;
    wire out_valid;
    wire [7:0] quotient, remainder;

    divider_8bit_pipeline DUT (
        .clk(clk),
        .rst(rst),
        .in_valid(in_valid),
        .dividend(dividend),
        .divisor(divisor),
        .out_valid(out_valid),
        .quotient(quotient),
        .remainder(remainder)
    );

    // 100 MHz clock
    always #5 clk = ~clk;

    task send_div;
        input [7:0] a;
        input [7:0] b;
        begin
            @(posedge clk);
            dividend  <= a;
            divisor   <= b;
            in_valid  <= 1'b1;

            @(posedge clk);
            in_valid  <= 1'b0;
        end
    endtask

    initial begin
        clk = 0;
        rst = 1;
        in_valid = 0;
        dividend = 0;
        divisor  = 0;

        // reset
        repeat (5) @(posedge clk);
        rst = 0;

        // Apply inputs
        send_div(8'd10,  8'd10);
        send_div(8'd25,  8'd5);
        send_div(8'd15,  8'd4);
        send_div(8'd9,   8'd2);
        send_div(8'd100, 8'd7);

        // Wait enough clocks for pipeline to flush
        repeat (20) @(posedge clk);

        $finish;
    end

    // Monitor outputs
    always @(posedge clk) begin
        if (out_valid) begin
            $display("Time=%0t  Q=%0d  R=%0d", $time, quotient, remainder);
        end
    end

endmodule