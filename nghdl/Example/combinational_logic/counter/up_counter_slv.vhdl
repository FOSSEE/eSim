-- This logic is implemented in up_counter.vhdl example as well, but there tmp variable is declared as unsigned
--whereas here it is declared as std_logic_vector; which requires type conversion. 
--slv stands for std_logic_vector
library ieee;

use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity up_counter_slv is
port(C : in std_logic;
     CLR : in std_logic;
     Q : out std_logic_vector(3 downto 0));
end up_counter_slv;

architecture bhv of up_counter_slv is

	signal tmp: std_logic_vector(3 downto 0);
	begin
	process (C, CLR)
		begin
			if (CLR='1') then
			tmp <= "0000";

			elsif (C'event and C='1') then
			tmp <= std_logic_vector(to_unsigned(1+to_integer(unsigned(tmp)), tmp'length));

			end if;

	end process;
	Q <= tmp;

end bhv;
