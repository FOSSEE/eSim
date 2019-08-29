library ieee;
use ieee.std_logic_1164.all;

entity myxor is
       port (a : in  std_logic_vector(0 downto 0); 
             b : in  std_logic_vector(0 downto 0);
             c : out std_logic_vector(0 downto 0)); 
     end myxor;
     
     architecture rtl of myxor is
     begin
        
        c <= a xor b;
        
     end rtl;
