library IEEE;
use IEEE.STD_LOGIC_1164.all;

entity t_demux is
 port(

 F : in STD_LOGIC_vector(0 downto 0);
 S0: in STD_LOGIC_vector(0 downto 0);
 S1: in STD_LOGIC_vector(0 downto 0);
 A: out STD_LOGIC_vector(0 downto 0);
 B: out STD_LOGIC_vector(0 downto 0);
 C: out STD_LOGIC_vector(0 downto 0);
 D: out STD_LOGIC_vector(0 downto 0)
 );
end t_demux;

architecture bhv of t_demux is
begin
process (F,S0,S1) is
begin
 if (S0 ="0" and S1 = "0") then
 A <= F;
 elsif (S0 ="1" and S1 = "0") then
 B <= F;
 elsif (S0 ="0" and S1 = "1") then
 C <= F;
 else
 D <= F;
 end if;

end process;
end bhv;