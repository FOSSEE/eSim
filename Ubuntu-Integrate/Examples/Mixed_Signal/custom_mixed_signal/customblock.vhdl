library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity customblock is
port(C : in std_logic;
     D : in std_logic;
     Q : out std_logic);
end customblock;


architecture bhv of customblock is
       signal count:  integer:=1;       --counts number of CLOCK cycles
       signal period: integer:=10;      --PWM signal period is 10 times of clock period
       signal boost  : integer:=9;      --number of clock pulses during T_ON
       signal buck : integer:=1;        --number of clock pulses during T_OFF
begin
	process (C,D)

       begin

          if(C='1' and C'event) then 
            count<=count+1;      
            if(count=period)then -- resets count for period
              count<=1;
            end if;
            if(D='1') then --boost duty cycle when compartor output is high--
              if(count<=boost)then 
                Q<='1';
              elsif(count>boost) then
                Q<='0';     
              end if; 
            end if;
            if(D='0')then --buck duty cycle when compartor output is low--
              if(count<=buck)then --
                Q<='1';
              elsif(count>buck)then
                Q<='0';  
              end if;
            end if;    
        end if;
  end process;
end bhv;
