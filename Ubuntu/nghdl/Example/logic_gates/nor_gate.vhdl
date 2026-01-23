library ieee;
use ieee.std_logic_1164.all;

entity nor_gate is
    port (a : in  std_logic;
          b : in  std_logic;
          c : out std_logic);
end nor_gate;
     
architecture rtl of nor_gate is
    begin
		c <= a nor b;
end rtl;
