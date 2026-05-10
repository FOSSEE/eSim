module asynchronous_fifo (
    input  wclk,
    input  rclk,
    input  rst,
    input  wr_en,
    input  rd_en,
    input  [7:0] din,
    output reg [7:0] dout,
    output full,
    output empty
);

localparam ADDR_WIDTH = 3;
localparam DEPTH = 8;

reg [7:0] mem [0:7];

reg [3:0] wptr_bin, rptr_bin;
reg [3:0] wptr_gray, rptr_gray;

reg [3:0] wptr_gray_sync1, wptr_gray_sync2;
reg [3:0] rptr_gray_sync1, rptr_gray_sync2;

wire [3:0] wptr_bin_next;
wire [3:0] wptr_gray_next;
wire [3:0] rptr_bin_next;
wire [3:0] rptr_gray_next;

assign wptr_bin_next  = wptr_bin + (wr_en & ~full);
assign wptr_gray_next = (wptr_bin_next >> 1) ^ wptr_bin_next;

assign rptr_bin_next  = rptr_bin + (rd_en & ~empty);
assign rptr_gray_next = (rptr_bin_next >> 1) ^ rptr_bin_next;

initial begin
    wptr_bin = 0;
    rptr_bin = 0;
    wptr_gray = 0;
    rptr_gray = 0;
    dout = 0;
end

// WRITE DOMAIN
always @(posedge wclk) begin
    if (rst) begin
        wptr_bin  <= 0;
        wptr_gray <= 0;
    end else begin
        wptr_bin  <= wptr_bin_next;
        wptr_gray <= wptr_gray_next;

        if (wr_en && !full)
            mem[wptr_bin[2:0]] <= din;
    end
end

// READ DOMAIN
always @(posedge rclk) begin
    if (rst) begin
        rptr_bin  <= 0;
        rptr_gray <= 0;
        dout      <= 0;
    end else begin
        rptr_bin  <= rptr_bin_next;
        rptr_gray <= rptr_gray_next;

        if (rd_en && !empty)
            dout <= mem[rptr_bin[2:0]];
    end
end

// Synchronizers
always @(posedge wclk) begin
    if (rst) begin
        rptr_gray_sync1 <= 0;
        rptr_gray_sync2 <= 0;
    end else begin
        rptr_gray_sync1 <= rptr_gray;
        rptr_gray_sync2 <= rptr_gray_sync1;
    end
end

always @(posedge rclk) begin
    if (rst) begin
        wptr_gray_sync1 <= 0;
        wptr_gray_sync2 <= 0;
    end else begin
        wptr_gray_sync1 <= wptr_gray;
        wptr_gray_sync2 <= wptr_gray_sync1;
    end
end

assign empty = (rptr_gray == wptr_gray_sync2);

assign full =
    (wptr_gray_next ==
        {~rptr_gray_sync2[3:2],
          rptr_gray_sync2[1:0]});

endmodule