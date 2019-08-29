-- author: Madhav P. Desai
library ieee;
use ieee.std_logic_1164.all;

package Utility_Package is

  -----------------------------------------------------------------------------
  -- constants
  -----------------------------------------------------------------------------
  constant c_word_length : integer := 32;
  constant c_vhpi_max_string_length : integer := 1024;
  
  -----------------------------------------------------------------------------
  -- types
  -----------------------------------------------------------------------------
  subtype VhpiString is string(1 to c_vhpi_max_string_length);

  -----------------------------------------------------------------------------
  -- utility functions
  -----------------------------------------------------------------------------
  function Minimum(x,y: integer) return integer; -- returns minimum
  function Pack_String_To_Vhpi_String(x: string) return VhpiString; -- converts x to null terminated string
  function Pack_SLV_To_Vhpi_String(x: std_logic_vector) return VhpiString; -- converts slv x to null terminated string
  function Unpack_String(x: VhpiString; lgth: integer) return std_logic_vector; -- convert null term string to slv
  function To_Std_Logic(x: VhpiString) return std_logic; -- string to sl
  function To_String(x: std_logic) return VhpiString; -- string to sl
  function Convert_To_String(val : natural) return STRING; -- convert val to string.
  function Convert_SLV_To_String(val : std_logic_vector) return STRING; -- convert val to string.
  function To_Hex_Char (constant val: std_logic_vector)    return character;
  function Convert_SLV_To_Hex_String(val : std_logic_vector) return STRING; -- convert val to string.  

end package Utility_Package;

package body Utility_Package is

  -----------------------------------------------------------------------------
  -- utility functions
  -----------------------------------------------------------------------------
  function Minimum(x,y: integer) return integer is
  begin
    if( x < y) then return x; else return y; end if;
  end Minimum;

  function Ceiling(x,y: integer) return integer is
    variable ret_var : integer;
  begin
    assert x /= 0 report "divide by zero in ceiling function" severity failure;
    ret_var := x/y;
    if(ret_var*y < x) then ret_var := ret_var + 1; end if;
    return(ret_var);
  end Ceiling;

  function Pack_String_To_Vhpi_String(x:  string) return VhpiString is
     alias lx: string(1 to x'length) is x;
     variable strlen: integer;
     variable ret_var : VhpiString;
  begin
	strlen := Minimum(c_vhpi_max_string_length-1,x'length);
	for I in 1 to strlen loop
		ret_var(I) := lx(I);
	end loop;
	ret_var(strlen+1) := nul;
	return(ret_var); 
  end Pack_String_To_Vhpi_String;
  
  function Pack_SLV_To_Vhpi_String(x: std_logic_vector) return VhpiString is
    alias lx : std_logic_vector(1 to x'length) is x;
    variable strlen: integer;
    variable ret_var : VhpiString;
  begin
    strlen := Minimum(c_vhpi_max_string_length-1,x'length);
    for I in 1 to strlen loop
      if(lx(I) = '1') then 
        ret_var(I) := '1';
      else
        ret_var(I) := '0';
      end if;
    end loop;
    ret_var(strlen+1) := nul;
    return(ret_var); 
  end Pack_SLV_To_Vhpi_String;
  
  function Unpack_String(x: VhpiString; lgth: integer) return std_logic_vector is
    variable ret_var : std_logic_vector(1 to lgth);
    variable strlen: integer;
  begin
    strlen := Minimum(c_vhpi_max_string_length-1,lgth);
    for I in 1 to strlen loop
      if(x(I) = '1') then 
        ret_var(I) := '1';
      else
        ret_var(I) := '0';
      end if;
    end loop;
    return(ret_var);     
  end Unpack_String;

  function To_Std_Logic(x: VhpiString) return std_logic is
    variable s: std_logic_vector(0 downto 0);
  begin
    s := Unpack_String(x,1);
    return(s(0));
  end To_Std_Logic;

  function To_String(x: std_logic) return VhpiString is
    variable s: std_logic_vector(0 downto 0);
  begin
   s(0) := x;
   return(Pack_SLV_To_Vhpi_String(s));
  end To_String;

  -- Thanks to: D. Calvet calvet@hep.saclay.cea.fr
  function Convert_To_String(val : NATURAL) return STRING is
	variable result : STRING(10 downto 1) := (others => '0'); -- smallest natural, longest string
	variable pos    : NATURAL := 1;
	variable tmp, digit  : NATURAL;
  begin
	tmp := val;
	loop
		digit := abs(tmp MOD 10);
	    	tmp := tmp / 10;
	    	result(pos) := character'val(character'pos('0') + digit);
	    	pos := pos + 1;
	    	exit when tmp = 0;
	end loop;
	return result((pos-1) downto 1);
  end Convert_To_String;

  function Convert_SLV_To_String(val : std_logic_vector) return STRING is
	alias lval: std_logic_vector(1 to val'length) is val;
        variable ret_var: string( 1 to lval'length);
   begin
        for I in lval'range loop
                if(lval(I) = '1') then
			ret_var(I) := '1';
		elsif (lval(I) = '0') then
			ret_var(I) := '0';
		else
			ret_var(I) := 'X';
		end if;
        end loop;
        return(ret_var);
   end Convert_SLV_To_String;

  function To_Hex_Char (constant val: std_logic_vector)   return character  is
    alias lval: std_logic_vector(1 to val'length) is val;
    variable tvar : std_logic_vector(1 to 4);
    variable ret_val : character;
  begin
    if(lval'length >= 4) then
      tvar := lval(1 to 4);
    else
      tvar := (others => '0');
      tvar(1 to lval'length) := lval;
    end if;

    case tvar is
      when "0000" => ret_val := '0';
      when "0001" => ret_val := '1';
      when "0010" => ret_val := '2';                     
      when "0011" => ret_val := '3';
      when "0100" => ret_val := '4';
      when "0101" => ret_val := '5';
      when "0110" => ret_val := '6';                     
      when "0111" => ret_val := '7';
      when "1000" => ret_val := '8';
      when "1001" => ret_val := '9';
      when "1010" => ret_val := 'a';                     
      when "1011" => ret_val := 'b';
      when "1100" => ret_val := 'c';
      when "1101" => ret_val := 'd';
      when "1110" => ret_val := 'e';                     
      when "1111" => ret_val := 'f';                                                               
      when others => ret_val := 'f';
    end case;

    return(ret_val);
  end To_Hex_Char;
        
  function Convert_SLV_To_Hex_String(val : std_logic_vector) return STRING is
    alias lval: std_logic_vector(val'length downto 1) is val;
    variable ret_var: string( 1 to Ceiling(lval'length,4));
    variable hstr  : std_logic_vector(4 downto 1);
    variable I : integer;
  begin

    I := 0;

    while I < (lval'length/4) loop
      hstr := lval(4*(I+1) downto (4*I)+1);
      ret_var(ret_var'length - I) := To_Hex_Char(hstr);
      I := (I + 1);
    end loop;  -- I

    hstr := (others => '0');
    if(ret_var'length > (lval'length/4)) then
      hstr((lval'length-((lval'length/4)*4)) downto 1) := lval(lval'length downto (4*(lval'length/4))+1);
      ret_var(1) := To_Hex_Char(hstr);
    end if;

    return(ret_var);
  end Convert_SLV_To_Hex_String;
end Utility_Package;

