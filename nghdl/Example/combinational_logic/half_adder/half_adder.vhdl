library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
 
entity half_adder is
  port (
    i_bit0  : in std_logic_vector(0 downto 0);
    i_bit1  : in std_logic_vector(0 downto 0);
    o_sum   : out std_logic_vector(0 downto 0);
    o_carry : out std_logic_vector(0 downto 0)
    );
end half_adder;
 
architecture rtl of half_adder is
begin
  o_sum   <= i_bit0 xor i_bit1;
  o_carry <= i_bit0 and i_bit1;
end rtl;
