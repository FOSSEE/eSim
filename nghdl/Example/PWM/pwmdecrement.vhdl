library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pwmdecrement is
port(C : in std_logic;
     D : in std_logic;
     Q : out std_logic);
end pwmdecrement;

architecture bhv of pwmdecrement is
        signal count: integer:=0;       
        signal alpha: integer:=0;  --counts number of clocks
        signal beta : integer:=1;  --counts number of times 'D' is low w.r.t Clock signal(C)  
        signal tmp  : integer:=9; --stores the value of beta for which Q will be set HIGH
        begin
	process (C,D)

        begin
        if(C='1' and C'event) then
        alpha<=alpha+1;  --counts number of rising edges
                if(count=0) then --initial pulse 
                Q <= '1';
                count<=1;
                end if;
               if(D='0') then --if D is low, increase beta by 1
                beta<=beta+1;
                end if;
                if(alpha=9) then --when aplha is 9, decrease beta by 1 and store in tmp //--set to 9 on purpose(so that first pwm signal has 90% duty cycle)
                tmp<=beta-1; --decrease beta and store in tmp, so that we get 10% less duty cycle than previous
                alpha<=0;
                beta<=0;
                count<=0;
                end if;
                if(tmp=alpha) then --the moment when number of clocks(alpha) equals previous number of times Q was high(tmp), we turn Q off. 
                Q<='0';
                end if;
        end if;
        end process;
end bhv;
