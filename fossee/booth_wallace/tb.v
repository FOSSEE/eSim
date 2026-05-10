`timescale 1ns/1ps

module tb_booth_wallace;

    reg  signed [3:0] A, B;
    wire signed [7:0] P;

    // Instantiate DUT
    booth_wallace_4x4 DUT (
        .A(A),
        .B(B),
        .P(P)
    );

    initial begin

        // Apply inputs
        A = 7;
        B = -5;

        #5;   // wait for combinational logic

        $display("A = %0d", A);
        $display("B = %0d", B);
        $display("Product = %0d", P);

        if (P == -20)
            $display("TEST PASSED ✅");
        else
            $display("TEST FAILED ❌");

        $finish;

    end

endmodule