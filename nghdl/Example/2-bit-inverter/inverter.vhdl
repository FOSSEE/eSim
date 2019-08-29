library ieee;
use ieee.std_logic_1164.all;

entity inverter is
    port ( i: in std_logic_vector(0 downto 0);
           o: out std_logic_vector(0 downto 0));
end inverter;

architecture inverter_beh of inverter is
begin
    o <= not i;
end inverter_beh;


