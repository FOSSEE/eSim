library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
 
entity nghdl_ha is
port (
    	i_bit1  : in std_logic_vector(0 downto 0);
	    i_bit2  : in std_logic_vector(0 downto 0);
    	o_sum   : out std_logic_vector(0 downto 0);
    	o_carry : out std_logic_vector(0 downto 0)
    );
end nghdl_ha;
 

architecture rtl of nghdl_ha is

begin
 
  o_sum   <= i_bit1 xor i_bit2;
  o_carry <= i_bit1 and i_bit2;

end rtl;