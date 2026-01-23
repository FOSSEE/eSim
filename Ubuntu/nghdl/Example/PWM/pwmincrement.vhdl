library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pwmincrement is
port(C : in std_logic;
     D : in std_logic;
     Q : out std_logic);
end pwmincrement;
--working code for incrementing duty cycle \ Output of oscillator is fed back using a LPF and Comparator in F/B loop
architecture bhv of pwmincrement is
        signal count: integer:=0;       
        signal alpha: integer:=0;  --counts number of clocks
        signal beta : integer:=0;  --counts number of times 'D' is low w.r.t Clock signal(C) 
        signal tmp  : integer:=0;  --stores the value of beta for which Q will be set HIGH
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
                if(alpha=8) then --when aplha is 8, incremement beta by 1 and store in tmp //--set to 8 on purpose(so that first pwm signal has 10% duty cycle)
                tmp<=beta+1; --increase beta and store in tmp, so that we get 10% more duty cycle than previous
                alpha<=0; --reset alpha
                beta<=0; --reset beta  
                count<=0; --reset count
                end if;
                if(tmp=alpha) then --the moment when number of clocks(alpha) equals previous number of times Q was high(tmp), we turn Q off. Effectively incrementing duty cycle by 10%
                Q<='0';
                tmp<=0;
                end if;
        end if;
        end process;
end bhv;
