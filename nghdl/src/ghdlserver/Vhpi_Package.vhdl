-- author: Madhav P. Desai
library ieee;
use ieee.std_logic_1164.all;
library work;
use work.Utility_Package.all;
package Vhpi_Foreign is

  -----------------------------------------------------------------------------
  -- foreign Vhpi function
  -----------------------------------------------------------------------------
  procedure  Vhpi_Initialize(sock_port : in integer);
  attribute foreign of Vhpi_Initialize : procedure is "VHPIDIRECT Vhpi_Initialize";
  
  procedure Vhpi_Close; -- close .
  attribute foreign of Vhpi_Close : procedure is "VHPIDIRECT Vhpi_Close";

  procedure Vhpi_Listen;
  attribute foreign of Vhpi_Listen : procedure is "VHPIDIRECT Vhpi_Listen";

  procedure Vhpi_Send; 
  attribute foreign of Vhpi_Send : procedure is "VHPIDIRECT Vhpi_Send";

  procedure Vhpi_Set_Port_Value(port_name: in VhpiString; port_value: in VhpiString; port_width: in integer);
  attribute foreign of Vhpi_Set_Port_Value: procedure is "VHPIDIRECT Vhpi_Set_Port_Value";
  
  procedure Vhpi_Get_Port_Value(port_name: in VhpiString; port_value : out VhpiString; port_width: in integer);
  attribute foreign of Vhpi_Get_Port_Value : procedure is "VHPIDIRECT Vhpi_Get_Port_Value";
  
  procedure Vhpi_Log(message_string: in VhpiString);
  attribute foreign of Vhpi_Log : procedure is "VHPIDIRECT Vhpi_Log";

end Vhpi_Foreign;
  
package body Vhpi_Foreign is

  -----------------------------------------------------------------------------
  -- subprogram bodies for foreign vhpi routines.  will never be called
  -----------------------------------------------------------------------------
  procedure  Vhpi_Initialize(sock_port: in integer) is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Initialize;
  
  procedure Vhpi_Close is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Close;

  procedure Vhpi_Listen is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Listen;

  procedure Vhpi_Send is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Send;
  
  procedure Vhpi_Set_Port_Value(port_name: in VhpiString; port_value: in VhpiString; port_width: in integer) is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Set_Port_Value;    
  
  procedure  Vhpi_Get_Port_Value(port_name : in  VhpiString;  port_value: out VhpiString; port_width: in integer)is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Get_Port_Value;        

  procedure Vhpi_Log(message_string: in VhpiString) is
  begin
    assert false  report "fatal: this should never be called" severity failure;
  end Vhpi_Log;

end Vhpi_Foreign;



