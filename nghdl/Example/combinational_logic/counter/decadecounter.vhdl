library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity decadecounter is
	port(CLK : in std_logic;
	     RST : in std_logic;
	     Count : out std_logic_vector(9 downto 0));
end decadecounter;

architecture beh of decadecounter is
	signal a: std_logic_vector(9 downto 0) := "0000000001";
begin
	process(CLK, RST)
	begin
		if RST = '1' then
			a <= "0000000001";
		elsif rising_edge(CLK) then
			a <= a(0) & a(9 downto 1);  -- rotating left
		end if;
	end process;
	Count <= std_logic_vector (a);
end beh;
