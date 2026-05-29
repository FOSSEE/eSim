library ieee;
use ieee.std_logic_1164.all;

entity or_gate is
    Port ( a : in  STD_LOGIC;    
           b : in  STD_LOGIC;    
           c : out  STD_LOGIC);    
end or_gate;

architecture behavioral of or_gate is
begin
c <= a or b;    
end behavioral;
