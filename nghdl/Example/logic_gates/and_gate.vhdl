library ieee;

use ieee.std_logic_1164.all;

entity and_gate is

port(    a: in std_logic;
         b: in std_logic;
         c: out std_logic
);

end and_gate;

architecture beh of and_gate is

    begin

    process(a, b)

    begin

    if (a='1' and b='1') then
        c <= '1';

    else 

	c <= '0';

    end if;

    end process;

end beh;
