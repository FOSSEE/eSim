--This file uses only std_logic_vector(slv) variable type
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
 
entity full_adder_slv is
  port (
    i_bit1  : in std_logic_vector(0 downto 0);
    i_bit2  : in std_logic_vector(0 downto 0);
    i_bit3  : in std_logic_vector(0 downto 0);
    o_sum   : out std_logic_vector(0 downto 0);
    o_carry : out std_logic_vector(0 downto 0)
    );
end full_adder_slv;
 
architecture rtl of full_adder_slv is
begin
  o_sum   <= i_bit1 xor i_bit2 xor i_bit3;
  o_carry <= (i_bit1 and i_bit2) or (i_bit2 and i_bit3) or (i_bit3 and i_bit1);
end rtl;
