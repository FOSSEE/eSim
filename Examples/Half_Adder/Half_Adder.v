module Half_Adder (net__u1_pad3_, net__u1_pad4_, net__u2_pad1_, net__u2_pad2_);
  inout net__u1_pad3_;
  inout net__u1_pad4_;
  inout net__u2_pad1_;
  inout net__u2_pad2_;

  half_adder x1 (net__u1_pad3_, net__u1_pad4_, net__u2_pad1_, net__u2_pad2_);
endmodule
