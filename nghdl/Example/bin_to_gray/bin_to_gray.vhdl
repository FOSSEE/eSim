LIBRARY ieee;
USE ieee.std_logic_1164.ALL;

entity bin_to_gray is
port(   
		bin : in std_logic_vector(3 downto 0);  -- binary input
        G   : out std_logic_vector(3 downto 0)  -- gray code output
    );
end bin_to_gray;


architecture gate_level of bin_to_gray is 

begin

G(3) <= bin(3);
G(2) <= bin(3) xor bin(2);
G(1) <= bin(2) xor bin(1);
G(0) <= bin(1) xor bin(0);

end gate_level;