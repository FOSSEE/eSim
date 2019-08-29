/*************************************************************************
 * <ghdlserver.c>  FOSSEE, IIT-Mumbai
 * 24.Mar.2017 - Raj Mohan - Added signal handler for SIGUSR1, to handle an 
 *                           orphan test bench process.
 *                           The test bench will now create a PID file in
 *                           /tmp directory with the name 
 *                           NGHDL_<ngspice pid>_<test bench>_<instance_id>
 *                           This file contains the PID of the test bench .
 *                           On exit, the test bench removes this file.
 *                           The SIGUSR1 signal serves the same purpose as the 
 *                           "End" signal.
 *                         - Added syslog interface for logging.
 *                         - Enabled SO_REUSEADDR socket option.
 *                         - Added the following functions:
 *                             o create_pid_file()
 *                             o get_ngspice_pid()
 * 22.Feb.2017 - Raj Mohan - Implemented a kludge to fix a problem in the
 *                           test bench VHDL code.
 *                         - Changed sleep() to nanosleep().
 * 10.Feb.2017 - Raj Mohan - Log messages with timestamp/code clean up.
 *                           Added the following functions:
 *                             o curtim()
 *                             o print_hash_table()
 *************************************************************************
 */
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
#include <sys/socket.h> 
#include <sys/time.h>                                                        
#include <netinet/in.h>                                                         
#include <netdb.h>
#include <limits.h>
#include <time.h>
#include <errno.h>
#include <dirent.h>
#include <syslog.h>

#define _XOPEN_SOURCE 500
#define MAX_NUMBER_PORT 100

#define NGSPICE "ngspice"     // 17.Mar.2017 - RM

extern char* __progname;  // 26.Feb.2017 May not be portable to non-GNU systems.

void Vhpi_Exit(int sig);

static FILE* pid_file;
static char pid_filename[80];

static char* Out_Port_Array[MAX_NUMBER_PORT];           
static int out_port_num = 0; 
static int server_socket_id = -1;
static int sendto_sock;      // 22.Feb.2017 - RM - Kludge
static int prev_sendto_sock; // 22.Feb.2017 - RM - Kludge
static int pid_file_created; // 10.Mar.2017 - RM 

struct my_struct {
    char val[1024];                  
    char key[1024];       
    UT_hash_handle hh;    //Makes this structure hashable.
};

static struct my_struct *s, *users, *tmp = NULL;

/* 17.Mar.2017 - RM - Get the process id of ngspice program.*/
static int get_ngspice_pid(void)
{
    DIR* dirp;
    FILE* fp = NULL;
    struct dirent* dir_entry;
    char path[1024], rd_buff[1024];
    pid_t pid = -1;

    if ((dirp = opendir("/proc/")) == NULL)
    {
	perror("opendir /proc failed");
	exit(-1);
    }

    while ((dir_entry = readdir(dirp)) != NULL)
    {
		char* nptr;
	    int valid_num = 0;

		int tmp = strtol(dir_entry->d_name, &nptr, 10);
		if ((errno == ERANGE) && (tmp == LONG_MAX || tmp == LONG_MIN))
		{
		    perror("strtol"); // Number out of range.
		    return(-1);
		}
		if (dir_entry->d_name == nptr)
		{
		    continue; // No digits found.
		}
		if (tmp)
		{
		    sprintf(path, "/proc/%s/comm", dir_entry->d_name);
		    if ((fp = fopen(path, "r")) != NULL)
		    {
				fscanf(fp, "%s", rd_buff);
				if (strcmp(rd_buff, NGSPICE) == 0)
				{
				    pid = (pid_t)tmp;
				}
		    }
		}
    }

   if (fp) fclose(fp);

   return(pid);
}

/* 23.Mar.2017 - RM - Pass the sock_port argument. We need this if a netlist
 * uses more than one instance of the same test bench, so that we can uniquely
 * identify the PID files.
 */
/* 10.Mar.2017 - RM - Create PID file for the test bench in /tmp. */
static void create_pid_file(int sock_port)
{
    pid_t my_pid = getpid();
    pid_t ngspice_pid = get_ngspice_pid(); 
    if (ngspice_pid == -1)
    {
	fprintf(stderr, "create_pid_file() Failed to get ngspice PID");
	syslog(LOG_ERR,  "create_pid_file() Failed to get ngspice PID");
	exit(1);
    }
    sprintf(pid_filename, "/tmp/NGHDL_%d_%s_%d", ngspice_pid, __progname, 
            sock_port);
    pid_file = fopen(pid_filename, "w");
    if (pid_file)
    {
	pid_file_created = 1;
	fprintf(pid_file,"%d\n", my_pid);
	fclose(pid_file);
    } else {
        perror("fopen() - PID file");
	syslog(LOG_ERR, "create_pid_file(): Unable to open PID file in /tmp");
        exit(1);
    }

    return;
}

#ifdef DEBUG
static char* curtim(void)
{
    static char ct[50];
    struct timeval tv;
    struct tm* ptm;
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

    for(sptr=users; sptr != NULL; sptr=sptr->hh.next)
    {
	syslog(LOG_INFO, "Hash table:val:%s: key: %s", sptr->val, sptr->key);
    }
}
#endif

static void parse_buffer(int sock_id, char* receive_buffer)
{
    static int rcvnum;

    syslog(LOG_INFO,"RCVD RCVN:%d from CLT:%d buffer : %s",
	   rcvnum++, sock_id,receive_buffer);

    /*Parsing buffer to store in hash table */ 
    char *rest;
    char *token;
    char *ptr1=receive_buffer;
    char *var;
    char *value;

    // Processing tokens.
    while(token = strtok_r(ptr1, ",", &rest)) 
    {
        ptr1 = rest;
        while(var=strtok_r(token, ":", &value))
        {
          s = (struct my_struct*)malloc(sizeof(struct my_struct));
	  strncpy(s->key, var, 64);
	  strncpy(s->val, value, 64);
	  HASH_ADD_STR(users, key, s );
	  break;    
        }
    }
        
    s = (struct my_struct*)malloc(sizeof(struct my_struct));
    strncpy(s->key, "sock_id", 64);
    snprintf(s->val,64, "%d", sock_id);
    HASH_ADD_STR(users, key, s);
}

//
//Create Server and listen for client connections.
//
static int create_server(int port_number,int max_connections)
{
 int sockfd, reuse = 1;
 struct sockaddr_in serv_addr;

 sockfd = socket(AF_INET, SOCK_STREAM, 0);

 if (sockfd < 0)
 {
    fprintf(stderr, "%s- Error: in opening socket on port %d\n", 
            __progname, port_number);
    exit(1);
 }

/* 20.Mar.2017 - RM - SO_REUSEADDR option. To take care of TIME_WAIT state.*/
 int ret = setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(int));
 if (ret < 0) 
 {
     syslog(LOG_ERR, "create_server:setsockopt() failed....");
 }

 bzero((char *) &serv_addr, sizeof(serv_addr));
 serv_addr.sin_family = AF_INET;
 serv_addr.sin_addr.s_addr = INADDR_ANY;
 serv_addr.sin_port = htons(port_number);
     
 if (bind(sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr)) < 0)
 {
     fprintf(stderr,"%s- Error: could not bind socket to port %d\n",
             __progname, port_number);
     syslog(LOG_ERR, "Error: could not bind socket to port %d", port_number);

     close(sockfd);

     exit(1);
 }

 // Start listening on the server.
 listen(sockfd, max_connections);

 return sockfd;
}

// The server to wait (non-blocking) for a client connection.
static int connect_to_client(int server_fd)                                            
{                                                                               
    int ret_val = 1;
    int newsockfd = -1;
    socklen_t clilen;
    struct sockaddr_in  cli_addr;
    fd_set c_set;
    struct timeval time_limit;                                                
  
    time_limit.tv_sec = 0;
    time_limit.tv_usec = 1000;
    
    clilen = sizeof(cli_addr); 

    FD_ZERO(&c_set);
    FD_SET(server_fd, &c_set);

    select(server_fd + 1, &c_set, NULL, NULL, &time_limit);

    ret_val = FD_ISSET(server_fd, &c_set);

    if(ret_val)
    {
        newsockfd = accept(server_fd, (struct sockaddr *) &cli_addr, &clilen);
        if (newsockfd >= 0)
        { 
	    	syslog(LOG_INFO, "SRV:%d New Client Connection CLT:%d", server_fd, newsockfd);
        }        
        else
        {
            syslog(LOG_ERR,"Error: failed in accept(), socket=%d", server_fd);
		    exit(1);
        }                   
    } 

    return(newsockfd);
}   

//                                                                              
// Check if we can read from the socket..
//    
static int can_read_from_socket(int socket_id)                                         
{                                                                               
    struct timeval time_limit;  
    time_limit.tv_sec = 0;  
    time_limit.tv_usec = 1000;
    
    fd_set c_set; 
    FD_ZERO(&c_set); 
    FD_SET(socket_id, &c_set);
    
    int npending = select(socket_id + 1, &c_set, NULL, NULL, &time_limit);
    if (npending == -1)
    { 
        npending = errno;
	syslog(LOG_ERR, "can_read_from_socket:select() ERRNO=%d",npending);
        return(-100);
    }
    return(FD_ISSET(socket_id, &c_set));
}   

//                                                                              
// Check if we can write to the socket..
//    
static int can_write_to_socket(int socket_id)                                          
{                                                                               
    struct timeval time_limit;  
    time_limit.tv_sec = 0;
    time_limit.tv_usec = 1000;
    
    fd_set c_set;
    FD_ZERO(&c_set);
    FD_SET(socket_id, &c_set);                                                  

    int npending = select(socket_id + 1, NULL, &c_set, NULL, &time_limit);
    if (npending == -1)
    {
	npending = errno;

	syslog(LOG_ERR, "can_write_to_socket() select() ERRNO=%d",npending);

	return (-100);
    } else if (npending == 0) {  // select() timed out...
	return(0);
    }
    return(FD_ISSET(socket_id,&c_set));
}   

//Receive string from socket and put it inside buffer.
static int receive_string(int sock_id, char* buffer)                                   
{                                                                               
  int nbytes = 0;
  int ret;  
    
    while(1)
    {
        ret = can_read_from_socket(sock_id); 
	if (ret == 0) 
	{ // select() had timed out. Retry...
	    usleep(1000);
	    continue;
	} else 
        if (ret == -100)
	{
	    return(-1);
	}
	break;
    }                                                                           
    
    nbytes = recv(sock_id, buffer, MAX_BUF_SIZE, 0);
    if (nbytes < 0)
    {
	perror("READ FAILURE");
        exit(1);
    }
    return(nbytes); 
}   

static void set_non_blocking(int sock_id)                                              
{                                                                               
    int x;                                                                    
    x = fcntl(sock_id, F_GETFL, 0); 
    fcntl(sock_id, F_SETFL, x | O_NONBLOCK); 
    syslog(LOG_INFO, "Setting server to non blocking state."); 
} 

static void Data_Send(int sockid)                                       
{                                                                               
  static int trnum;
  char* out;

  int i;
  char colon = ':';
  char semicolon = ';'; 
  int wrt_retries = 0;
  int ret;

  s = NULL;
  int found = 0;

  out = calloc(1, 2048);

  for (i=0; i<out_port_num; i++)
  {  
     
     found = 0;
     
     HASH_FIND_STR(users,Out_Port_Array[i],s);
     if (strcmp(Out_Port_Array[i], s->key) == 0) 
     {
      found=1;
     }

      if(found) 
      { 
          strncat(out, s->key, strlen(s->key));
          strncat(out, &colon, 1);
          strncat(out, s->val, strlen(s->val));
          strncat(out, &semicolon, 1);
      }         
      else                                                                        
      {        

          syslog(LOG_ERR,"The %s's value not found in the table.",
                 Out_Port_Array[i]);
          free(out);
          return;
      }

    }

      while(1)
      {
            if (wrt_retries > 2)  // 22.Feb.2017 - Kludge
            {
                free(out);
                return;
            }
            ret = can_write_to_socket(sockid); 
            if (ret > 0) break;
          
            if( ret == -100)
            {
                syslog(LOG_ERR,"Send aborted to CLT:%d buffer:%s ret=%d",
                 sockid, out,ret);
                      free(out);
                return;
            } 
            else // select() timed out. Retry....
            {
              printf("\n Sleep \n");
              usleep(1000);
              wrt_retries++;
            }
          }

      if ((send(sockid, out, strlen(out), 0)) == -1)
        {
          syslog(LOG_ERR,"Failure sending to CLT:%d buffer:%s", sockid, out);
          exit(1);
        }

      syslog(LOG_INFO,"SNT:TRNUM:%d to CLT:%d buffer: %s", trnum++, sockid, out);  
      free(out);
    
} 

void Vhpi_Initialize(int sock_port)
{
    DEFAULT_SERVER_PORT = sock_port;

    signal(SIGINT,Vhpi_Exit);
    signal(SIGTERM,Vhpi_Exit);

    signal(SIGUSR1, Vhpi_Exit); //10.Mar.2017 - RM

    int try_limit = 100;

    while(try_limit > 0)
    {
      server_socket_id = create_server(DEFAULT_SERVER_PORT,DEFAULT_MAX_CONNECTIONS);
      if(server_socket_id > 0)
        {
           syslog(LOG_INFO,"Started the server on port %d  SRV:%d",
		  DEFAULT_SERVER_PORT, server_socket_id);
            set_non_blocking(server_socket_id);
            break;
        }
        else
	{
            syslog(LOG_ERR,"Could not start server on port %d,will try again",
                   DEFAULT_SERVER_PORT);
	    usleep(1000);
	    try_limit--;
        
	    if(try_limit==0)
	    {
	       syslog(LOG_ERR,
                 "Error:Tried to start server on port %d, failed..giving up.",
                      DEFAULT_SERVER_PORT);
	       exit(1);
            }
	    
	}
    }
  //                                                                            
  //Reading Output Port name and storing in Out_Port_Array;                     
  //                                                                            
    char* line = NULL;
    size_t len = 0; 
    ssize_t read;
    char *token;
    FILE *fp;
    struct timespec ts;

    fp=fopen("connection_info.txt","r");
    if (! fp)
    {
	syslog(LOG_ERR,"Vhpi_Initialize: Failed to open connection_info.txt. Exiting...");
	exit(1);
    }

    line = (char*) malloc(80);
    while ((read = getline(&line, &len, fp)) != -1)
    {
	if (strstr(line,"OUT") != NULL || strstr(line,"out") != NULL )
	{ 
	    strtok_r(line, " ",&token);
	    Out_Port_Array[out_port_num] = line;
	    out_port_num++;
	}
	line = (char*) malloc(80);
    }                     	
    fclose(fp);
    
    free(line);

    ts.tv_sec = 2;
    ts.tv_nsec = 0;
    nanosleep(&ts, NULL);

// 10.Mar.2017 - RM - Create PID file for the test bench.
    create_pid_file(sock_port);
}
void Vhpi_Set_Port_Value(char *port_name,char *port_value,int port_width)
{
    
  s = (struct my_struct*)malloc(sizeof(struct my_struct));
  strncpy(s->key, port_name,64);
  strncpy(s->val,port_value,64);
  HASH_ADD_STR( users, key, s );

}

void Vhpi_Get_Port_Value(char* port_name,char* port_value,int port_width)
{

  HASH_FIND_STR(users,port_name,s);
  if(s)
  {  
    snprintf(port_value,sizeof(port_value),"%s",s->val);

    HASH_DEL(users, s);
    free(s);
    s=NULL;
  }
}

void Vhpi_Listen()
{
    int new_sock;

    while(1)
    {
		new_sock = connect_to_client(server_socket_id);
        if(new_sock  > 0) 
        {
            char receive_buffer[MAX_BUF_SIZE];
	    	int n = receive_string(new_sock, receive_buffer);
	    	if(n > 0)
            {
				sendto_sock = new_sock; // 22.Feb.2017 - RM - Kludge
				syslog(LOG_INFO, "Vhpi_Listen:New socket connection CLT:%d",new_sock);

				printf("\n\n%s\n\n", receive_buffer);

				if(strcmp(receive_buffer, "END")==0) 
                {
                  syslog(LOG_INFO, "RCVD:CLOSE REQUEST from CLT:%d", new_sock);  
                  Vhpi_Exit(0);
                }  
	      		else 
                {
                  parse_buffer(new_sock,receive_buffer);
                }
                break;
            }
        } 
    	else
      	{
        	break;
      	}
    }
}


void  Vhpi_Send() 
{
    int sockid;
    char* out;

// Traverse the list of finished jobs and send out the resulting port values.. 
// 22.Feb.2017 - RM - Kludge
//    log_server=fopen("server.log","a");
//    fprintf(log_server, "%s Vhpi_Send() called\n", curtim());

//    fprintf(log_server,"Vhpi_Send()-------------------\n");
//    print_hash_table();
//    fprintf(log_server,"----------------------------------------\n");
//    HASH_FIND_STR(users,"sock_id",s);
//    if(s)
//    {  
//      sockid=atoi(s->val);
//    }
//    else
//    {
//      fprintf(log_server,"%s Socket id not in table - key=%s val=%s\n",
//              curtim(),
//	      users->key, users->val);  
//    }
//    Data_Send(sockid);

    if (prev_sendto_sock != sendto_sock)
    { 
	Data_Send(sendto_sock);                                      
	prev_sendto_sock = sendto_sock;
    }
// 22.Feb.2017 End kludge
 
}

void  Vhpi_Close()                                                         
{  
    close(server_socket_id);
    syslog(LOG_INFO, "*** Closed VHPI link. ***");
}

void Vhpi_Exit(int sig) 
{                                                                               
    Vhpi_Close(); 

    // printf("\nVHPI EXIT\n");

// 10.Mar.2017 - RM
    if (pid_file_created) {
    	// printf("%s\n", pid_filename);
       	remove(pid_filename);
    }

    syslog(LOG_INFO, "*** Exiting ***");

    exit(0);
}    
