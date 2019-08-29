/* 18.Mar.2017 - RM - Cleaned up.*/

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

// Should be enough..
#define MAX_BUF_SIZE 4096

//Defualt port number

//unlikely to have more than 16 active
//threads talking to the TB?
#define DEFAULT_MAX_CONNECTIONS 65535

int DEFAULT_SERVER_PORT;

//Vhpi Functions.
void   Vhpi_Initialize(int sock_port);
void   Vhpi_Close(); 
void   Vhpi_Exit();
void   Vhpi_Listen();
void   Vhpi_Send();
void   Vhpi_Set_Port_Value(char* reg_name, char* reg_value, int port_width);
void   Vhpi_Get_Port_Value(char* reg_name, char* reg_value, int port_width);


 
