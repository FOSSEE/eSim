library ieee;
use ieee.std_logic_1164.all;

entity inverter is
    port ( i: in std_logic;
           o: out std_logic);
end inverter;

architecture beh of inverter is
begin
    o <= not i;
end beh;


