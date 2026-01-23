/************************************************************************************
 * <ghdlserver.c>  eSim Team, FOSSEE, IIT-Bombay
 ************************************************************************************
 * 8.June.2020 - Bladen Martin   - Added OS (Windows and Linux) dependent              
 *             - Rahul Paknikar    preprocessors for ease of maintenance
 *
 * 28.May.2020 - Bladen Martin   - Termination of testbench: Replaced Process ID
 *             - Rahul Paknikar    mechanism with socket connection from client
 *                                 receiving the special close message
 ************************************************************************************
 ************************************************************************************
 * 08.Nov.2019 - Rahul Paknikar  - Switched to blocking sockets from non-blocking
 *								 - Close previous used socket to prevent from   
 *								   generating too many socket descriptors
 *								 - Enabled SO_REUSEPORT, SO_DONTROUTE socket options
 * 5.July.2019 - Rahul Paknikar  - Added loop to send all port values for 
 *                                 a given event.
 ************************************************************************************
 ************************************************************************************
 * 24.Mar.2017 - Raj Mohan - Added syslog interface for logging.
 *                         - Enabled SO_REUSEADDR socket option.
 * 22.Feb.2017 - Raj Mohan - Implemented a kludge to fix a problem in the
 *                           test bench VHDL code.
 *                         - Changed sleep() to nanosleep().
 * 10.Feb.2017 - Raj Mohan - Log messages with timestamp/code clean up.
 *                           Added the following functions:
 *                             o curtim()
 *                             o print_hash_table()
 ***********************************************************************************/

#include <string.h>
#include "ghdlserver.h"
#include "uthash.h"
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/time.h>
#include <limits.h>
#include <time.h>
#include <errno.h>

#ifdef __linux__
    #include <sys/socket.h>
    #include <arpa/inet.h>
    #include <netinet/in.h>
    #include <netdb.h>
    #include <syslog.h>
#elif _WIN32
    #include <ws2tcpip.h>
    #include <winsock2.h>
    #include <eventsys.h>
    #include <windows.h>
#endif

#define _XOPEN_SOURCE 500
#define MAX_NUMBER_PORT 100
#define NGSPICE "ngspice"     // 17.Mar.2017 - RM

static FILE *pid_file;
static char pid_filename[80];
static char *Out_Port_Array[MAX_NUMBER_PORT];
static int out_port_num = 0;
static int server_socket_id = -1;
static int sendto_sock;      // 22.Feb.2017 - RM - Kludge
static int prev_sendto_sock; // 22.Feb.2017 - RM - Kludge
static int pid_file_created; // 10.Mar.2017 - RM

#ifdef __linux__
    extern char* __progname; // 26.Feb.2017 May not be portable to non-GNU systems.
#endif

void Vhpi_Exit(int sig);

struct my_struct {
    char val[1024];                  
    char key[1024];       
    UT_hash_handle hh;    //Makes this structure hashable.
};

static struct my_struct *s, *users, *tmp = NULL;


#ifdef DEBUG
static char* curtim(void)
{
    static char ct[50];
    struct timeval tv;
    struct tm *ptm;
    long milliseconds;
    char time_string[40];

    gettimeofday (&tv, NULL);
    ptm = localtime (&tv.tv_sec);
    strftime (time_string, sizeof (time_string), "%Y-%m-%d %H:%M:%S", ptm);
    milliseconds = tv.tv_usec / 1000;
    sprintf (ct, "%s.%03ld", time_string, milliseconds);
    return(ct);
}
#endif


#ifdef DEBUG
static void print_hash_table(void)
{
    struct my_struct *sptr;
    
    #ifdef __linux__
        for(sptr = users; sptr != NULL; sptr = sptr->hh.next)
		    syslog(LOG_INFO, "Hash table:val:%s: key: %s", sptr->val, sptr->key);
    #endif
}
#endif


static void parse_buffer(int sock_id, char *receive_buffer)
{
    static int rcvnum;
    
    #ifdef __linux__
        syslog(LOG_INFO, "RCVD RCVN:%d from CLT:%d buffer : %s",
	       rcvnum++, sock_id, receive_buffer);
    #endif

    /*Parsing buffer to store in hash table */
    char *rest;
    char *token;
    char *ptr1 = receive_buffer;
    char *var;
    char *value;

	// Processing tokens.
	while (token = strtok_r(ptr1, ",", &rest))
	{
		ptr1 = rest;
		while (var = strtok_r(token, ":", &value))
		{
			s = (struct my_struct *) malloc(sizeof(struct my_struct));
			strncpy(s->key, var, 64);
			strncpy(s->val, value, 64);
			HASH_ADD_STR(users, key, s);
			break;
		}
	}

	s = (struct my_struct *) malloc(sizeof(struct my_struct));
	strncpy(s->key, "sock_id", 64);
	snprintf(s->val, 64, "%d", sock_id);
	HASH_ADD_STR(users, key, s);
}


//Create Server and listen for client connections.
// 26.Sept.2019 - RP - added parameter of socket ip
static int create_server(int port_number, char my_ip[], int max_connections)
{
	int sockfd, reuse = 1;
	struct sockaddr_in serv_addr;

	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	if (sockfd < 0)
	{
        #ifdef __linux__
		    fprintf(stderr, "%s- Error: in opening socket at server \n", __progname);

        #elif _WIN32
		    fprintf(stderr, "Error: in opening socket at server \n");

        #endif

		//exit(1);
		return -1;
	}

	/* 18.May.2020 - BM - typecast optval field to char*  */
	/* 20.Mar.2017 - RM - SO_REUSEADDR option. To take care of TIME_WAIT state.*/
	int ret = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (char *) &reuse, sizeof(int));

    /* 08.Nov.2019 - RP - SO_REUSEPORT and SO_DONTROUTE option.*/
    /* 08.June.2020 - BM - SO_REUSEPORT only available in Linux */
    #ifdef __linux__
	    ret += setsockopt(sockfd, SOL_SOCKET, SO_REUSEPORT, &reuse, sizeof(int));
    #endif

	ret += setsockopt(sockfd, SOL_SOCKET, SO_DONTROUTE, (char *) &reuse, sizeof(int));
	if (ret < 0)
	{
        #ifdef __linux__
		    syslog(LOG_ERR, "create_server:setsockopt() failed....");
        #endif
		// close(sockfd);
		// return -1;
	}

	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr(my_ip); // 26.Sept.2019 - RP - Bind to specific IP only
	serv_addr.sin_port = htons(port_number);

	if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
	{
        #ifdef __linux__
		    fprintf(stderr, "%s- Error: could not bind socket to port %d\n", __progname, port_number);
		    syslog(LOG_ERR, "Error: could not bind socket to port %d", port_number);
		    close(sockfd);

        #elif _WIN32
		    fprintf(stderr, "Error: could not bind socket to port %d\n", port_number);
		    closesocket(sockfd);

        #endif
		
        exit(1);
	}

	// Start listening on the server.
	listen(sockfd, max_connections);

	return sockfd;
}


// The server to wait (blocking) for a client connection.
static int connect_to_client(int server_fd)
{
	int ret_val = 0;
	int newsockfd = -1;
	socklen_t clilen;
	struct sockaddr_in cli_addr;

	clilen = sizeof(cli_addr);

	/* 08.Nov.2019 - RP - Blocking Socket (Accept) */
	newsockfd = accept(server_fd, (struct sockaddr *) &cli_addr, &clilen);
	if (newsockfd >= 0)
	{
        #ifdef _linux_
            syslog(LOG_INFO, "SRV:%d New Client Connection CLT:%d", server_fd, newsockfd);
        #endif
	}
	else
	{
        #ifdef __linux__
            syslog(LOG_ERR, "Error: failed in accept(), socket=%d", server_fd);
        #endif

		exit(1);
	}

	return newsockfd;
}


//Receive string from socket and put it inside buffer.
static void receive_string(int sock_id, char *buffer)
{
	int nbytes = 0;

	/* 08.Nov.2019 - RP - Blocking Socket - Receive */
    nbytes = recv(sock_id, buffer, MAX_BUF_SIZE, 0);
    if (nbytes <= 0)
    {
		perror("receive_string() - READ FAILURE ");
        exit(1);
    }

    // 28.May.2020 - BM - Added method to close server by Ngspice after simulation
    char *exitstr = "CLOSE_FROM_NGSPICE";  
    if (strcmp(buffer, exitstr) == 0)
	{
	    Vhpi_Exit(0);
	}
}


static void Data_Send(int sockid)
{
	static int trnum;
	char *out;

	int i;
	char colon = ':';
	char semicolon = ';';
	int wrt_retries = 0;
	int ret;

	s = NULL;

	out = calloc(1, 2048);

	// 5.July.2019 - RP - loop to send all ports at once for an event
	for (i = 0; i < out_port_num; i++)
	{
        HASH_FIND_STR(users, Out_Port_Array[i], s);
    	if (strcmp(Out_Port_Array[i], s->key) == 0)
    	{
    		strncat(out, s->key, strlen(s->key));
          	strncat(out, &colon, 1);
          	strncat(out, s->val, strlen(s->val));
          	strncat(out, &semicolon, 1);
      	}      
      	else                                                                        
      	{        
            #ifdef __linux__
              	syslog(LOG_ERR,"The %s's value not found in the table.",
                     Out_Port_Array[i]);
            #endif

          	free(out);
            printf("Error! The %s's value not found in the table. Exiting simulation...",
                 Out_Port_Array[i]);
          	return;
     	}
    }

	/* 08.Nov.2019 - RP - Blocking Socket (Send) */
	if ((send(sockid, out, strlen(out), 0)) == -1)
	{
        #ifdef __linux__
		    syslog(LOG_ERR, "Failure sending to CLT:%d buffer:%s", sockid, out);
        #endif

		exit(1);
	}

    #ifdef __linux__
    	syslog(LOG_INFO, "SNT:TRNUM:%d to CLT:%d buffer: %s", trnum++, sockid, out);
    #endif

	free(out);
}


// 26.Sept.2019 - RP - added parameter of socket ip
void Vhpi_Initialize(int sock_port, char sock_ip[])
{
    DEFAULT_SERVER_PORT = sock_port;

	signal(SIGINT, Vhpi_Exit);
	signal(SIGTERM, Vhpi_Exit);

    #ifdef _WIN32
	    WSADATA WSAData;
	    WSAStartup(MAKEWORD(2, 2), &WSAData);
    #endif

    int try_limit = 100;

	while (try_limit > 0)
	{
		// 26.Sept.2019 - RP
		server_socket_id = create_server(DEFAULT_SERVER_PORT, sock_ip, DEFAULT_MAX_CONNECTIONS);

      	if (server_socket_id >= 0)
      	{
            #ifdef __linux__
                syslog(LOG_INFO, "Started the server on port %d  SRV:%d",
                    DEFAULT_SERVER_PORT, server_socket_id);
            #endif

            break;
        }

        #ifdef __linux__
            syslog(LOG_ERR, "Could not start server on port %d,will try again",
                    DEFAULT_SERVER_PORT);
        #endif

	    usleep(1000);
	    try_limit--;

	    if (try_limit == 0)
	    {
            #ifdef __linux__
    	      	syslog(LOG_ERR,
	           "Error:Tried to start server on port %d, failed..giving up.",
	                DEFAULT_SERVER_PORT);
            #endif

		    exit(1);
        }
    }

	//Reading Output Port name and storing in Out_Port_Array;
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    char *token;
    FILE *fp;
    struct timespec ts;

    fp = fopen("connection_info.txt", "r");
    if (!fp)
    {
        #ifdef __linux__
    		syslog(LOG_ERR,"Vhpi_Initialize: Failed to open connection_info.txt. Exiting...");
        #endif

		exit(1);
    }

    line = (char *) malloc(80);

    #ifdef __linux__
	    while ((read = getline(&line, &len, fp)) != -1)
	    {
		    if (strstr(line, "OUT") != NULL || strstr(line, "out") != NULL)
		    {
		        strtok_r(line, " ", &token);
		        Out_Port_Array[out_port_num] = line;
		        out_port_num++;
		    }
		    line = (char *) malloc(80);
        }

    #elif _WIN32
	    while (fgets(line, sizeof(line), fp) != NULL)
	    {
		    if (strstr(line, "OUT") != NULL || strstr(line, "out") != NULL)
		    {
			    strtok_r(line, " ", &token);
			    Out_Port_Array[out_port_num] = line;
			    out_port_num++;
		    }
		    line = (char *) malloc(80);
	    }

    #endif

    fclose(fp);
    free(line);

    ts.tv_sec = 2;
    ts.tv_nsec = 0;
    nanosleep(&ts, NULL);
}


void Vhpi_Set_Port_Value(char *port_name, char *port_value, int port_width)
{
	s = (struct my_struct *) malloc(sizeof(struct my_struct));
	strncpy(s->key, port_name, 64);
	strncpy(s->val, port_value, 64);
	HASH_ADD_STR(users, key, s);
}


void Vhpi_Get_Port_Value(char *port_name, char *port_value, int port_width)
{
	HASH_FIND_STR(users, port_name, s);
	if (s)
	{
		snprintf(port_value, sizeof(port_value), "%s", s->val);
		HASH_DEL(users, s);
		free(s);
		s = NULL;
	}
}


void Vhpi_Listen()
{
    sendto_sock = connect_to_client(server_socket_id);	// 22.Feb.2017 - RM - Kludge
	char receive_buffer[MAX_BUF_SIZE];
	receive_string(sendto_sock, receive_buffer);

    #ifdef __linux__
       	syslog(LOG_INFO, "Vhpi_Listen:New socket connection CLT:%d", sendto_sock);
    #endif

   	if (strcmp(receive_buffer, "END") == 0)
    {
        #ifdef __linux__
            syslog(LOG_INFO, "RCVD:CLOSE REQUEST from CLT:%d", sendto_sock);
        #endif

    	Vhpi_Exit(0);
    }

	parse_buffer(sendto_sock, receive_buffer);
}


void Vhpi_Send()
{
	// 22.Feb.2017 - RM - Kludge
	if (prev_sendto_sock != sendto_sock)
	{
		Data_Send(sendto_sock);

        #ifdef __linux__
		    close(prev_sendto_sock); // 08.Nov.2019 - RP - Close previous socket

        #elif _WIN32
    		closesocket(prev_sendto_sock);

        #endif

		prev_sendto_sock = sendto_sock;
	}
	// 22.Feb.2017 End kludge
}


void Vhpi_Exit(int sig)
{
    #ifdef __linux__
	    close(server_socket_id);
	    syslog(LOG_INFO, "*** Closed VHPI link. Exiting... ***");

    #elif _WIN32
	    closesocket(server_socket_id);

    #endif

	exit(0);
}