library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
       
entity up_counter is
	port(Clock : in  std_logic;
    	CLR : in  std_logic;
        	Q : out std_logic_vector(3 downto 0));        
end up_counter;
       
architecture beh of up_counter is
	signal tmp: unsigned(3 downto 0) := "0000";
                
    --------------- Other ways to initialize --------------
    -- signal tmp: unsigned(3 downto 0) := x"0";
    -- signal tmp: unsigned(3 downto 0) := (others => '0');
    -------------------------------------------------------

    begin
    process (Clock, CLR)        
        begin          
            if (CLR='1') then          
                tmp <= "0000";          
            elsif (Clock'event and Clock='1') then  
                if tmp="1111" then
                	tmp <= x"0";
                else      
                	tmp <= tmp +1;        
                end if;  
            end if;          
    end process;
           
    Q <= std_logic_vector (tmp);   
end beh;
