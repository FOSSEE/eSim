library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.numeric_std.ALL;


entity updown_counter is
    Port ( clk: in std_logic;
           reset: in std_logic;
     up_down: in std_logic;
           counter: out std_logic_vector(3 downto 0)
     );
end updown_counter;

architecture Behavioral of updown_counter is
signal tmp: std_logic_vector(3 downto 0);
begin

process(clk,reset)
begin
    if(reset='1') then
         tmp <= "0000";
    elsif(clk'event and clk='1') then
         if(up_down='1') then
           tmp <= std_logic_vector(to_unsigned(to_integer(unsigned(tmp)-1), tmp'length));
         else 
           tmp <= std_logic_vector(to_unsigned(to_integer(unsigned(tmp)+1), tmp'length));
         end if;
    end if;
end process;
 counter <= std_logic_vector(tmp);

end Behavioral;