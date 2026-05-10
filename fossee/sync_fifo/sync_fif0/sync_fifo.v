module sync_fifo (
    input  wire        clk,
    input  wire        rst,
    input  wire        wr_en,
    input  wire        rd_en,
    input  wire [7:0]  din,
    output reg  [7:0]  dout,
    output wire        full,
    output wire        empty
);

    parameter DEPTH = 8;
    parameter ADDR  = 3;   // log2(8)

    reg [7:0] mem [0:DEPTH-1];

    reg [ADDR:0] wptr;
    reg [ADDR:0] rptr;

    // WRITE
    always @(posedge clk or posedge rst) begin
        if (rst)
            wptr <= 0;
        else if (wr_en && !full) begin
            mem[wptr[ADDR-1:0]] <= din;
            wptr <= wptr + 1;
        end
    end

    // READ
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            rptr <= 0;
            dout <= 0;
        end
        else if (rd_en && !empty) begin
            dout <= mem[rptr[ADDR-1:0]];
            rptr <= rptr + 1;
        end
    end

    assign empty = (wptr == rptr);

    assign full  = (wptr[ADDR-1:0] == rptr[ADDR-1:0]) &&
                   (wptr[ADDR]     != rptr[ADDR]);

endmodule