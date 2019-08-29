library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
 
entity full_adder_sl is
  port (
    i_bit1  : in std_logic;
    i_bit2  : in std_logic;
    i_bit3  : in std_logic;
    o_sum   : out std_logic;
    o_carry : out std_logic
    );
end full_adder_sl;
 
architecture rtl of full_adder_sl is
begin
  o_sum   <= i_bit1 xor i_bit2 xor i_bit3;
  o_carry <= (i_bit1 and i_bit2) or (i_bit2 and i_bit3) or (i_bit3 and i_bit1);
end rtl;