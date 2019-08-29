library ieee;
use ieee.std_logic_1164.all;

entity esim_trial_xor is
       port (a : in  std_logic_vector(0 downto 0); 
             b : in  std_logic_vector(0 downto 0);
             c : out std_logic_vector(0 downto 0)); 
     end esim_trial_xor;
     
     architecture rtl of esim_trial_xor is
     begin
        
        c <= a xor b;
        
     end rtl;
