--This file uses structural style and uses only std_logic variable type
library ieee;
use ieee.std_logic_1164.all;

entity full_adder_structural is
port(a: in std_logic;
	 b: in std_logic;
     cin: in std_logic;
     sum: out std_logic;
     carry: out std_logic);
end full_adder_structural;

library ieee;
use ieee.std_logic_1164.all;

entity andgate is
port(a: in std_logic;
     b: in std_logic;
     z: out std_logic);
end andgate;

architecture e1 of andgate is
begin
z <= a and b;
end e1;

library ieee;
use ieee.std_logic_1164.all;

entity xorgate is
port(a: in std_logic;
     b: in std_logic;
     z: out std_logic);
end xorgate;

architecture e2 of xorgate is
begin
z <= a xor b;
end e2;

library ieee;
use ieee.std_logic_1164.all;

entity orgate is
port(a: in std_logic;
     b: in std_logic;
     z: out std_logic);
end orgate;

architecture e3 of orgate is
begin
z <= a or b;
end e3;



architecture structural of full_adder_structural is

component andgate
port(a: in std_logic;
     b: in std_logic;
     z: out std_logic);
end component;

component xorgate
port(a: in std_logic;
	 b: in std_logic;
     z: out std_logic);
end component;

component orgate
port(a: in std_logic;
	 b: in std_logic;
     z: out std_logic);
end component;

signal c1,c2,c3: std_logic;

begin

u1 : xorgate port map(a,b,c1);
u2 : xorgate port map(c1,cin,sum);
u3 : andgate port map(c1,cin,c2);
u4 : andgate port map(a,b,c3);
u5 : orgate port map(c2,c3,carry);


end structural;
