library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity counter is
port(C : in std_logic;
     CLR : in std_logic;
     Q : out std_logic_vector(3 downto 0));
end counter;
architecture bhv of counter is
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