library IEEE;
use IEEE.STD_LOGIC_1164.all;
 
entity mux is
 port(A : in std_logic;
      B : in std_logic;
      C : in std_logic;
      D : in std_logic;
      S0 : in std_logic;
      S1 : in std_logic;
      Z: out std_logic);
end mux;
 
architecture bhv of mux is
begin
process (A,B,C,D,S0,S1) is
begin
  if (S0 ='0' and S1 = '0') then
      Z <= A;
  elsif (S0 ='0' and S1 = '1') then
      Z <= B;
  elsif (S0 ='1' and S1 = '0') then
      Z <= C;
  else
      Z <= D;
  end if;
 
end process;
end bhv;

