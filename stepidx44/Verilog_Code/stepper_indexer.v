// ==============================================================================
// stepper_indexer.v
// ==============================================================================

module stepper_indexer (
    input wire clk,
    input wire rst_n,
    input wire enable,
    
    // Standard Stepper Control Interface
    input wire step,       
    input wire dir,        

    // Outputs to Coil A PWM and H-Bridge
    output wire [15:0] coil_a_duty, 
    output wire coil_a_dir,         

    // Outputs to Coil B PWM and H-Bridge
    output wire [15:0] coil_b_duty,
    output wire coil_b_dir          
);

    // --------------------------------------------------------
    // Internal Registers
    // --------------------------------------------------------
    reg [7:0] phase_addr;   // 8-bit Phase Accumulator (0 to 255)
    reg step_prev;          // Memory for edge detection

    // Pipeline registers for synchronous LUT outputs
    reg signed [15:0] lut_sin;
    reg signed [15:0] lut_cos;

    // Combinational wires for LUT lookup
    reg signed [15:0] next_sin;
    reg signed [15:0] next_cos;

    wire [7:0] phase_b = phase_addr + 8'd64;

    // --------------------------------------------------------
    // 1. Coil A (Sine) ROM Lookup
    // --------------------------------------------------------
    always @(*) begin
        case(phase_addr)
            8'd0: next_sin = 16'h0000;
            8'd1: next_sin = 16'h0324;
            8'd2: next_sin = 16'h0648;
            8'd3: next_sin = 16'h096A;
            8'd4: next_sin = 16'h0C8C;
            8'd5: next_sin = 16'h0FAB;
            8'd6: next_sin = 16'h12C8;
            8'd7: next_sin = 16'h15E2;
            8'd8: next_sin = 16'h18F9;
            8'd9: next_sin = 16'h1C0B;
            8'd10: next_sin = 16'h1F1A;
            8'd11: next_sin = 16'h2223;
            8'd12: next_sin = 16'h2528;
            8'd13: next_sin = 16'h2826;
            8'd14: next_sin = 16'h2B1F;
            8'd15: next_sin = 16'h2E11;
            8'd16: next_sin = 16'h30FB;
            8'd17: next_sin = 16'h33DF;
            8'd18: next_sin = 16'h36BA;
            8'd19: next_sin = 16'h398C;
            8'd20: next_sin = 16'h3C56;
            8'd21: next_sin = 16'h3F17;
            8'd22: next_sin = 16'h41CE;
            8'd23: next_sin = 16'h447A;
            8'd24: next_sin = 16'h471C;
            8'd25: next_sin = 16'h49B4;
            8'd26: next_sin = 16'h4C3F;
            8'd27: next_sin = 16'h4EBF;
            8'd28: next_sin = 16'h5133;
            8'd29: next_sin = 16'h539B;
            8'd30: next_sin = 16'h55F5;
            8'd31: next_sin = 16'h5842;
            8'd32: next_sin = 16'h5A82;
            8'd33: next_sin = 16'h5CB3;
            8'd34: next_sin = 16'h5ED7;
            8'd35: next_sin = 16'h60EB;
            8'd36: next_sin = 16'h62F1;
            8'd37: next_sin = 16'h64E8;
            8'd38: next_sin = 16'h66CF;
            8'd39: next_sin = 16'h68A6;
            8'd40: next_sin = 16'h6A6D;
            8'd41: next_sin = 16'h6C23;
            8'd42: next_sin = 16'h6DC9;
            8'd43: next_sin = 16'h6F5E;
            8'd44: next_sin = 16'h70E2;
            8'd45: next_sin = 16'h7254;
            8'd46: next_sin = 16'h73B5;
            8'd47: next_sin = 16'h7504;
            8'd48: next_sin = 16'h7641;
            8'd49: next_sin = 16'h776B;
            8'd50: next_sin = 16'h7884;
            8'd51: next_sin = 16'h7989;
            8'd52: next_sin = 16'h7A7C;
            8'd53: next_sin = 16'h7B5C;
            8'd54: next_sin = 16'h7C29;
            8'd55: next_sin = 16'h7CE3;
            8'd56: next_sin = 16'h7D89;
            8'd57: next_sin = 16'h7E1D;
            8'd58: next_sin = 16'h7E9C;
            8'd59: next_sin = 16'h7F09;
            8'd60: next_sin = 16'h7F61;
            8'd61: next_sin = 16'h7FA6;
            8'd62: next_sin = 16'h7FD8;
            8'd63: next_sin = 16'h7FF5;
            8'd64: next_sin = 16'h7FFF;
            8'd65: next_sin = 16'h7FF5;
            8'd66: next_sin = 16'h7FD8;
            8'd67: next_sin = 16'h7FA6;
            8'd68: next_sin = 16'h7F61;
            8'd69: next_sin = 16'h7F09;
            8'd70: next_sin = 16'h7E9C;
            8'd71: next_sin = 16'h7E1D;
            8'd72: next_sin = 16'h7D89;
            8'd73: next_sin = 16'h7CE3;
            8'd74: next_sin = 16'h7C29;
            8'd75: next_sin = 16'h7B5C;
            8'd76: next_sin = 16'h7A7C;
            8'd77: next_sin = 16'h7989;
            8'd78: next_sin = 16'h7884;
            8'd79: next_sin = 16'h776B;
            8'd80: next_sin = 16'h7641;
            8'd81: next_sin = 16'h7504;
            8'd82: next_sin = 16'h73B5;
            8'd83: next_sin = 16'h7254;
            8'd84: next_sin = 16'h70E2;
            8'd85: next_sin = 16'h6F5E;
            8'd86: next_sin = 16'h6DC9;
            8'd87: next_sin = 16'h6C23;
            8'd88: next_sin = 16'h6A6D;
            8'd89: next_sin = 16'h68A6;
            8'd90: next_sin = 16'h66CF;
            8'd91: next_sin = 16'h64E8;
            8'd92: next_sin = 16'h62F1;
            8'd93: next_sin = 16'h60EB;
            8'd94: next_sin = 16'h5ED7;
            8'd95: next_sin = 16'h5CB3;
            8'd96: next_sin = 16'h5A82;
            8'd97: next_sin = 16'h5842;
            8'd98: next_sin = 16'h55F5;
            8'd99: next_sin = 16'h539B;
            8'd100: next_sin = 16'h5133;
            8'd101: next_sin = 16'h4EBF;
            8'd102: next_sin = 16'h4C3F;
            8'd103: next_sin = 16'h49B4;
            8'd104: next_sin = 16'h471C;
            8'd105: next_sin = 16'h447A;
            8'd106: next_sin = 16'h41CE;
            8'd107: next_sin = 16'h3F17;
            8'd108: next_sin = 16'h3C56;
            8'd109: next_sin = 16'h398C;
            8'd110: next_sin = 16'h36BA;
            8'd111: next_sin = 16'h33DF;
            8'd112: next_sin = 16'h30FB;
            8'd113: next_sin = 16'h2E11;
            8'd114: next_sin = 16'h2B1F;
            8'd115: next_sin = 16'h2826;
            8'd116: next_sin = 16'h2528;
            8'd117: next_sin = 16'h2223;
            8'd118: next_sin = 16'h1F1A;
            8'd119: next_sin = 16'h1C0B;
            8'd120: next_sin = 16'h18F9;
            8'd121: next_sin = 16'h15E2;
            8'd122: next_sin = 16'h12C8;
            8'd123: next_sin = 16'h0FAB;
            8'd124: next_sin = 16'h0C8C;
            8'd125: next_sin = 16'h096A;
            8'd126: next_sin = 16'h0648;
            8'd127: next_sin = 16'h0324;
            8'd128: next_sin = 16'h0000;
            8'd129: next_sin = 16'hFCDC;
            8'd130: next_sin = 16'hF9B8;
            8'd131: next_sin = 16'hF696;
            8'd132: next_sin = 16'hF374;
            8'd133: next_sin = 16'hF055;
            8'd134: next_sin = 16'hED38;
            8'd135: next_sin = 16'hEA1E;
            8'd136: next_sin = 16'hE707;
            8'd137: next_sin = 16'hE3F5;
            8'd138: next_sin = 16'hE0E6;
            8'd139: next_sin = 16'hDDDD;
            8'd140: next_sin = 16'hDAD8;
            8'd141: next_sin = 16'hD7DA;
            8'd142: next_sin = 16'hD4E1;
            8'd143: next_sin = 16'hD1EF;
            8'd144: next_sin = 16'hCF05;
            8'd145: next_sin = 16'hCC21;
            8'd146: next_sin = 16'hC946;
            8'd147: next_sin = 16'hC674;
            8'd148: next_sin = 16'hC3AA;
            8'd149: next_sin = 16'hC0E9;
            8'd150: next_sin = 16'hBE32;
            8'd151: next_sin = 16'hBB86;
            8'd152: next_sin = 16'hB8E4;
            8'd153: next_sin = 16'hB64C;
            8'd154: next_sin = 16'hB3C1;
            8'd155: next_sin = 16'hB141;
            8'd156: next_sin = 16'hAECD;
            8'd157: next_sin = 16'hAC65;
            8'd158: next_sin = 16'hAA0B;
            8'd159: next_sin = 16'hA7BE;
            8'd160: next_sin = 16'hA57E;
            8'd161: next_sin = 16'hA34D;
            8'd162: next_sin = 16'hA129;
            8'd163: next_sin = 16'h9F15;
            8'd164: next_sin = 16'h9D0F;
            8'd165: next_sin = 16'h9B18;
            8'd166: next_sin = 16'h9931;
            8'd167: next_sin = 16'h975A;
            8'd168: next_sin = 16'h9593;
            8'd169: next_sin = 16'h93DD;
            8'd170: next_sin = 16'h9237;
            8'd171: next_sin = 16'h90A2;
            8'd172: next_sin = 16'h8F1E;
            8'd173: next_sin = 16'h8DAC;
            8'd174: next_sin = 16'h8C4B;
            8'd175: next_sin = 16'h8AFC;
            8'd176: next_sin = 16'h89BF;
            8'd177: next_sin = 16'h8895;
            8'd178: next_sin = 16'h877C;
            8'd179: next_sin = 16'h8677;
            8'd180: next_sin = 16'h8584;
            8'd181: next_sin = 16'h84A4;
            8'd182: next_sin = 16'h83D7;
            8'd183: next_sin = 16'h831D;
            8'd184: next_sin = 16'h8277;
            8'd185: next_sin = 16'h81E3;
            8'd186: next_sin = 16'h8164;
            8'd187: next_sin = 16'h80F7;
            8'd188: next_sin = 16'h809F;
            8'd189: next_sin = 16'h805A;
            8'd190: next_sin = 16'h8028;
            8'd191: next_sin = 16'h800B;
            8'd192: next_sin = 16'h8001;
            8'd193: next_sin = 16'h800B;
            8'd194: next_sin = 16'h8028;
            8'd195: next_sin = 16'h805A;
            8'd196: next_sin = 16'h809F;
            8'd197: next_sin = 16'h80F7;
            8'd198: next_sin = 16'h8164;
            8'd199: next_sin = 16'h81E3;
            8'd200: next_sin = 16'h8277;
            8'd201: next_sin = 16'h831D;
            8'd202: next_sin = 16'h83D7;
            8'd203: next_sin = 16'h84A4;
            8'd204: next_sin = 16'h8584;
            8'd205: next_sin = 16'h8677;
            8'd206: next_sin = 16'h877C;
            8'd207: next_sin = 16'h8895;
            8'd208: next_sin = 16'h89BF;
            8'd209: next_sin = 16'h8AFC;
            8'd210: next_sin = 16'h8C4B;
            8'd211: next_sin = 16'h8DAC;
            8'd212: next_sin = 16'h8F1E;
            8'd213: next_sin = 16'h90A2;
            8'd214: next_sin = 16'h9237;
            8'd215: next_sin = 16'h93DD;
            8'd216: next_sin = 16'h9593;
            8'd217: next_sin = 16'h975A;
            8'd218: next_sin = 16'h9931;
            8'd219: next_sin = 16'h9B18;
            8'd220: next_sin = 16'h9D0F;
            8'd221: next_sin = 16'h9F15;
            8'd222: next_sin = 16'hA129;
            8'd223: next_sin = 16'hA34D;
            8'd224: next_sin = 16'hA57E;
            8'd225: next_sin = 16'hA7BE;
            8'd226: next_sin = 16'hAA0B;
            8'd227: next_sin = 16'hAC65;
            8'd228: next_sin = 16'hAECD;
            8'd229: next_sin = 16'hB141;
            8'd230: next_sin = 16'hB3C1;
            8'd231: next_sin = 16'hB64C;
            8'd232: next_sin = 16'hB8E4;
            8'd233: next_sin = 16'hBB86;
            8'd234: next_sin = 16'hBE32;
            8'd235: next_sin = 16'hC0E9;
            8'd236: next_sin = 16'hC3AA;
            8'd237: next_sin = 16'hC674;
            8'd238: next_sin = 16'hC946;
            8'd239: next_sin = 16'hCC21;
            8'd240: next_sin = 16'hCF05;
            8'd241: next_sin = 16'hD1EF;
            8'd242: next_sin = 16'hD4E1;
            8'd243: next_sin = 16'hD7DA;
            8'd244: next_sin = 16'hDAD8;
            8'd245: next_sin = 16'hDDDD;
            8'd246: next_sin = 16'hE0E6;
            8'd247: next_sin = 16'hE3F5;
            8'd248: next_sin = 16'hE707;
            8'd249: next_sin = 16'hEA1E;
            8'd250: next_sin = 16'hED38;
            8'd251: next_sin = 16'hF055;
            8'd252: next_sin = 16'hF374;
            8'd253: next_sin = 16'hF696;
            8'd254: next_sin = 16'hF9B8;
            8'd255: next_sin = 16'hFCDC;
            default: next_sin = 16'h0000;
        endcase
    end

    // --------------------------------------------------------
    // 2. Coil B (Cosine) ROM Lookup
    // --------------------------------------------------------
    always @(*) begin
        case(phase_b)
            8'd0: next_cos = 16'h0000;
            8'd1: next_cos = 16'h0324;
            8'd2: next_cos = 16'h0648;
            8'd3: next_cos = 16'h096A;
            8'd4: next_cos = 16'h0C8C;
            8'd5: next_cos = 16'h0FAB;
            8'd6: next_cos = 16'h12C8;
            8'd7: next_cos = 16'h15E2;
            8'd8: next_cos = 16'h18F9;
            8'd9: next_cos = 16'h1C0B;
            8'd10: next_cos = 16'h1F1A;
            8'd11: next_cos = 16'h2223;
            8'd12: next_cos = 16'h2528;
            8'd13: next_cos = 16'h2826;
            8'd14: next_cos = 16'h2B1F;
            8'd15: next_cos = 16'h2E11;
            8'd16: next_cos = 16'h30FB;
            8'd17: next_cos = 16'h33DF;
            8'd18: next_cos = 16'h36BA;
            8'd19: next_cos = 16'h398C;
            8'd20: next_cos = 16'h3C56;
            8'd21: next_cos = 16'h3F17;
            8'd22: next_cos = 16'h41CE;
            8'd23: next_cos = 16'h447A;
            8'd24: next_cos = 16'h471C;
            8'd25: next_cos = 16'h49B4;
            8'd26: next_cos = 16'h4C3F;
            8'd27: next_cos = 16'h4EBF;
            8'd28: next_cos = 16'h5133;
            8'd29: next_cos = 16'h539B;
            8'd30: next_cos = 16'h55F5;
            8'd31: next_cos = 16'h5842;
            8'd32: next_cos = 16'h5A82;
            8'd33: next_cos = 16'h5CB3;
            8'd34: next_cos = 16'h5ED7;
            8'd35: next_cos = 16'h60EB;
            8'd36: next_cos = 16'h62F1;
            8'd37: next_cos = 16'h64E8;
            8'd38: next_cos = 16'h66CF;
            8'd39: next_cos = 16'h68A6;
            8'd40: next_cos = 16'h6A6D;
            8'd41: next_cos = 16'h6C23;
            8'd42: next_cos = 16'h6DC9;
            8'd43: next_cos = 16'h6F5E;
            8'd44: next_cos = 16'h70E2;
            8'd45: next_cos = 16'h7254;
            8'd46: next_cos = 16'h73B5;
            8'd47: next_cos = 16'h7504;
            8'd48: next_cos = 16'h7641;
            8'd49: next_cos = 16'h776B;
            8'd50: next_cos = 16'h7884;
            8'd51: next_cos = 16'h7989;
            8'd52: next_cos = 16'h7A7C;
            8'd53: next_cos = 16'h7B5C;
            8'd54: next_cos = 16'h7C29;
            8'd55: next_cos = 16'h7CE3;
            8'd56: next_cos = 16'h7D89;
            8'd57: next_cos = 16'h7E1D;
            8'd58: next_cos = 16'h7E9C;
            8'd59: next_cos = 16'h7F09;
            8'd60: next_cos = 16'h7F61;
            8'd61: next_cos = 16'h7FA6;
            8'd62: next_cos = 16'h7FD8;
            8'd63: next_cos = 16'h7FF5;
            8'd64: next_cos = 16'h7FFF;
            8'd65: next_cos = 16'h7FF5;
            8'd66: next_cos = 16'h7FD8;
            8'd67: next_cos = 16'h7FA6;
            8'd68: next_cos = 16'h7F61;
            8'd69: next_cos = 16'h7F09;
            8'd70: next_cos = 16'h7E9C;
            8'd71: next_cos = 16'h7E1D;
            8'd72: next_cos = 16'h7D89;
            8'd73: next_cos = 16'h7CE3;
            8'd74: next_cos = 16'h7C29;
            8'd75: next_cos = 16'h7B5C;
            8'd76: next_cos = 16'h7A7C;
            8'd77: next_cos = 16'h7989;
            8'd78: next_cos = 16'h7884;
            8'd79: next_cos = 16'h776B;
            8'd80: next_cos = 16'h7641;
            8'd81: next_cos = 16'h7504;
            8'd82: next_cos = 16'h73B5;
            8'd83: next_cos = 16'h7254;
            8'd84: next_cos = 16'h70E2;
            8'd85: next_cos = 16'h6F5E;
            8'd86: next_cos = 16'h6DC9;
            8'd87: next_cos = 16'h6C23;
            8'd88: next_cos = 16'h6A6D;
            8'd89: next_cos = 16'h68A6;
            8'd90: next_cos = 16'h66CF;
            8'd91: next_cos = 16'h64E8;
            8'd92: next_cos = 16'h62F1;
            8'd93: next_cos = 16'h60EB;
            8'd94: next_cos = 16'h5ED7;
            8'd95: next_cos = 16'h5CB3;
            8'd96: next_cos = 16'h5A82;
            8'd97: next_cos = 16'h5842;
            8'd98: next_cos = 16'h55F5;
            8'd99: next_cos = 16'h539B;
            8'd100: next_cos = 16'h5133;
            8'd101: next_cos = 16'h4EBF;
            8'd102: next_cos = 16'h4C3F;
            8'd103: next_cos = 16'h49B4;
            8'd104: next_cos = 16'h471C;
            8'd105: next_cos = 16'h447A;
            8'd106: next_cos = 16'h41CE;
            8'd107: next_cos = 16'h3F17;
            8'd108: next_cos = 16'h3C56;
            8'd109: next_cos = 16'h398C;
            8'd110: next_cos = 16'h36BA;
            8'd111: next_cos = 16'h33DF;
            8'd112: next_cos = 16'h30FB;
            8'd113: next_cos = 16'h2E11;
            8'd114: next_cos = 16'h2B1F;
            8'd115: next_cos = 16'h2826;
            8'd116: next_cos = 16'h2528;
            8'd117: next_cos = 16'h2223;
            8'd118: next_cos = 16'h1F1A;
            8'd119: next_cos = 16'h1C0B;
            8'd120: next_cos = 16'h18F9;
            8'd121: next_cos = 16'h15E2;
            8'd122: next_cos = 16'h12C8;
            8'd123: next_cos = 16'h0FAB;
            8'd124: next_cos = 16'h0C8C;
            8'd125: next_cos = 16'h096A;
            8'd126: next_cos = 16'h0648;
            8'd127: next_cos = 16'h0324;
            8'd128: next_cos = 16'h0000;
            8'd129: next_cos = 16'hFCDC;
            8'd130: next_cos = 16'hF9B8;
            8'd131: next_cos = 16'hF696;
            8'd132: next_cos = 16'hF374;
            8'd133: next_cos = 16'hF055;
            8'd134: next_cos = 16'hED38;
            8'd135: next_cos = 16'hEA1E;
            8'd136: next_cos = 16'hE707;
            8'd137: next_cos = 16'hE3F5;
            8'd138: next_cos = 16'hE0E6;
            8'd139: next_cos = 16'hDDDD;
            8'd140: next_cos = 16'hDAD8;
            8'd141: next_cos = 16'hD7DA;
            8'd142: next_cos = 16'hD4E1;
            8'd143: next_cos = 16'hD1EF;
            8'd144: next_cos = 16'hCF05;
            8'd145: next_cos = 16'hCC21;
            8'd146: next_cos = 16'hC946;
            8'd147: next_cos = 16'hC674;
            8'd148: next_cos = 16'hC3AA;
            8'd149: next_cos = 16'hC0E9;
            8'd150: next_cos = 16'hBE32;
            8'd151: next_cos = 16'hBB86;
            8'd152: next_cos = 16'hB8E4;
            8'd153: next_cos = 16'hB64C;
            8'd154: next_cos = 16'hB3C1;
            8'd155: next_cos = 16'hB141;
            8'd156: next_cos = 16'hAECD;
            8'd157: next_cos = 16'hAC65;
            8'd158: next_cos = 16'hAA0B;
            8'd159: next_cos = 16'hA7BE;
            8'd160: next_cos = 16'hA57E;
            8'd161: next_cos = 16'hA34D;
            8'd162: next_cos = 16'hA129;
            8'd163: next_cos = 16'h9F15;
            8'd164: next_cos = 16'h9D0F;
            8'd165: next_cos = 16'h9B18;
            8'd166: next_cos = 16'h9931;
            8'd167: next_cos = 16'h975A;
            8'd168: next_cos = 16'h9593;
            8'd169: next_cos = 16'h93DD;
            8'd170: next_cos = 16'h9237;
            8'd171: next_cos = 16'h90A2;
            8'd172: next_cos = 16'h8F1E;
            8'd173: next_cos = 16'h8DAC;
            8'd174: next_cos = 16'h8C4B;
            8'd175: next_cos = 16'h8AFC;
            8'd176: next_cos = 16'h89BF;
            8'd177: next_cos = 16'h8895;
            8'd178: next_cos = 16'h877C;
            8'd179: next_cos = 16'h8677;
            8'd180: next_cos = 16'h8584;
            8'd181: next_cos = 16'h84A4;
            8'd182: next_cos = 16'h83D7;
            8'd183: next_cos = 16'h831D;
            8'd184: next_cos = 16'h8277;
            8'd185: next_cos = 16'h81E3;
            8'd186: next_cos = 16'h8164;
            8'd187: next_cos = 16'h80F7;
            8'd188: next_cos = 16'h809F;
            8'd189: next_cos = 16'h805A;
            8'd190: next_cos = 16'h8028;
            8'd191: next_cos = 16'h800B;
            8'd192: next_cos = 16'h8001;
            8'd193: next_cos = 16'h800B;
            8'd194: next_cos = 16'h8028;
            8'd195: next_cos = 16'h805A;
            8'd196: next_cos = 16'h809F;
            8'd197: next_cos = 16'h80F7;
            8'd198: next_cos = 16'h8164;
            8'd199: next_cos = 16'h81E3;
            8'd200: next_cos = 16'h8277;
            8'd201: next_cos = 16'h831D;
            8'd202: next_cos = 16'h83D7;
            8'd203: next_cos = 16'h84A4;
            8'd204: next_cos = 16'h8584;
            8'd205: next_cos = 16'h8677;
            8'd206: next_cos = 16'h877C;
            8'd207: next_cos = 16'h8895;
            8'd208: next_cos = 16'h89BF;
            8'd209: next_cos = 16'h8AFC;
            8'd210: next_cos = 16'h8C4B;
            8'd211: next_cos = 16'h8DAC;
            8'd212: next_cos = 16'h8F1E;
            8'd213: next_cos = 16'h90A2;
            8'd214: next_cos = 16'h9237;
            8'd215: next_cos = 16'h93DD;
            8'd216: next_cos = 16'h9593;
            8'd217: next_cos = 16'h975A;
            8'd218: next_cos = 16'h9931;
            8'd219: next_cos = 16'h9B18;
            8'd220: next_cos = 16'h9D0F;
            8'd221: next_cos = 16'h9F15;
            8'd222: next_cos = 16'hA129;
            8'd223: next_cos = 16'hA34D;
            8'd224: next_cos = 16'hA57E;
            8'd225: next_cos = 16'hA7BE;
            8'd226: next_cos = 16'hAA0B;
            8'd227: next_cos = 16'hAC65;
            8'd228: next_cos = 16'hAECD;
            8'd229: next_cos = 16'hB141;
            8'd230: next_cos = 16'hB3C1;
            8'd231: next_cos = 16'hB64C;
            8'd232: next_cos = 16'hB8E4;
            8'd233: next_cos = 16'hBB86;
            8'd234: next_cos = 16'hBE32;
            8'd235: next_cos = 16'hC0E9;
            8'd236: next_cos = 16'hC3AA;
            8'd237: next_cos = 16'hC674;
            8'd238: next_cos = 16'hC946;
            8'd239: next_cos = 16'hCC21;
            8'd240: next_cos = 16'hCF05;
            8'd241: next_cos = 16'hD1EF;
            8'd242: next_cos = 16'hD4E1;
            8'd243: next_cos = 16'hD7DA;
            8'd244: next_cos = 16'hDAD8;
            8'd245: next_cos = 16'hDDDD;
            8'd246: next_cos = 16'hE0E6;
            8'd247: next_cos = 16'hE3F5;
            8'd248: next_cos = 16'hE707;
            8'd249: next_cos = 16'hEA1E;
            8'd250: next_cos = 16'hED38;
            8'd251: next_cos = 16'hF055;
            8'd252: next_cos = 16'hF374;
            8'd253: next_cos = 16'hF696;
            8'd254: next_cos = 16'hF9B8;
            8'd255: next_cos = 16'hFCDC;
            default: next_cos = 16'h0000;
        endcase
    end

    // --------------------------------------------------------
    // 3. Step Edge Detection & Phase Accumulator
    // --------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            phase_addr <= 8'd0;
            step_prev  <= 1'b0;
        end else if (enable) begin
            step_prev <= step; // Track previous state to find the edge

            // Detect Rising Edge of the 'step' pin
            if (step == 1'b1 && step_prev == 1'b0) begin
                if (dir)
                    phase_addr <= phase_addr + 8'd1; // Step Forward
                else
                    phase_addr <= phase_addr - 8'd1; // Step Reverse
            end
        end
    end

    // --------------------------------------------------------
    // 4. Synchronous ROM Output
    // --------------------------------------------------------
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lut_sin <= 16'sd0;
            lut_cos <= 16'sd0;
        end else if (enable) begin
            lut_sin <= next_sin;
            lut_cos <= next_cos;
        end
    end

    // --------------------------------------------------------
    // 5. Math & Steering Logic
    // --------------------------------------------------------
    assign coil_a_dir = lut_sin[15];
    assign coil_b_dir = lut_cos[15];

    // Properly handle 16-bit signed to unsigned absolute conversion
    wire [15:0] abs_sin = lut_sin[15] ? (~lut_sin[14:0] + 15'd1) : lut_sin[14:0];
    wire [15:0] abs_cos = lut_cos[15] ? (~lut_cos[14:0] + 15'd1) : lut_cos[14:0];

    // Force 32-bit width for the multiplication to hold values up to 3,276,700
    wire [31:0] intermediate_a = ({16'b0, abs_sin} * 32'd100);
    wire [31:0] intermediate_b = ({16'b0, abs_cos} * 32'd100);

    // Final scaling: (Value * 100) / 32768
    assign coil_a_duty = intermediate_a[30:15];
    assign coil_b_duty = intermediate_b[30:15];

endmodule