import re
import os
from configparser import ConfigParser


class ModelGeneration:

    def __init__(self, file):

        # Script starts from here
        print("Arguement is : ", file)
        self.fname = os.path.basename(file)
        print("VHDL filename is : ", self.fname)

        if os.name == 'nt':
            self.home = os.path.join('library', 'config')
        else:
            # self.home = os.expanduser('~')
            self.home = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")) # direcotory: Resources/

        self.parser = ConfigParser()
        self.parser.read(os.path.join(
            self.home, os.path.join('.nghdl', 'config.ini')))
        self.nghdl_home = self.parser.get('NGHDL', 'NGHDL_HOME')
        self.release_dir = self.parser.get('NGHDL', 'RELEASE')
        self.src_home = self.parser.get('SRC', 'SRC_HOME')
        self.licensefile = self.parser.get('SRC', 'LICENSE')

        # #### Creating connection_info.txt file from vhdl file #### #
        read_vhdl = open(file, 'r')
        vhdl_data = read_vhdl.readlines()
        read_vhdl.close()

        start_flag = -1  # Used for scaning part of data
        scan_data = []
        # p=re.search('port(.*?)end',read_vhdl,re.M|re.I|re.DOTALL).group()

        for item in vhdl_data:
            if re.search('port', item, re.I):
                start_flag = 1

            elif re.search("end", item, re.I):
                start_flag = 0

            if start_flag == 1:
                item = re.sub("port", " ", item, flags=re.I)
                item = re.sub("\(", " ", item, flags=re.I)      # noqa
                item = re.sub("\)", " ", item, flags=re.I)      # noqa
                item = re.sub(";", " ", item, flags=re.I)
                if item.find(','):
                    temp1 = item.split(",")
                    item = "" + temp1[-1]
                    temp2 = temp1[-1].split(":")
                    for i in range(len(temp1) - 1):
                        temp3 = temp1[i] + ":" + temp2[-1]
                        scan_data.append(temp3.rstrip())
                scan_data.append(item.rstrip())
                scan_data = [_f for _f in scan_data if _f]
            elif start_flag == 0:
                break

        port_info = []
        self.port_vector_info = []

        for item in scan_data:
            print("Scan Data :", item)
            if re.search("in", item, flags=re.I):
                if re.search("std_logic_vector", item, flags=re.I):
                    temp = re.compile(r"\s*std_logic_vector\s*", flags=re.I)
                elif re.search("std_logic", item, flags=re.I):
                    temp = re.compile(r"\s*std_logic\s*", flags=re.I)
                else:
                    raise ValueError("Please check your vhdl " +
                                     "code for datatype of input port")
            elif re.search("out", item, flags=re.I):
                if re.search("std_logic_vector", item, flags=re.I):
                    temp = re.compile(r"\s*std_logic_vector\s*", flags=re.I)
                elif re.search("std_logic", item, flags=re.I):
                    temp = re.compile(r"\s*std_logic\s*", flags=re.I)
                else:
                    raise ValueError("Please check your vhdl " +
                                     "code for datatype of output port")
            else:
                raise ValueError(
                    "Please check the in/out direction of your port"
                )

            lhs = temp.split(item)[0]
            rhs = temp.split(item)[1]
            bit_info = re.compile(r"\s*downto\s*", flags=re.I).split(rhs)[0]
            if bit_info:
                port_info.append(lhs + ":" + str(int(bit_info) + int(1)))
                self.port_vector_info.append(1)
            else:
                port_info.append(lhs + ":" + str(int(1)))
                self.port_vector_info.append(0)

        print("Port Info :", port_info)

        # Open connection_info.txt file
        con_ifo = open('connection_info.txt', 'w')

        for item in port_info:
            word = item.split(':')
            con_ifo.write(
                word[0].strip() + ' ' + word[1].strip() + ' ' + word[2].strip()
            )
            con_ifo.write("\n")
        con_ifo.close()

    def readPortInfo(self):

        # ############## Reading connection/port information ############## #

        # Declaring input and output list
        input_list = []
        output_list = []

        # Reading connection_info.txt file for port infomation
        read_file = open('connection_info.txt', 'r')
        data = read_file.readlines()
        read_file.close()

        # Extracting input and output port list from data
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        for line in data:
            print(line)
            if re.match(r'^\s*$', line):
                pass
            else:
                in_items = re.findall(
                    "IN", line, re.MULTILINE | re.IGNORECASE
                )
                out_items = re.findall(
                    "OUT", line, re.MULTILINE | re.IGNORECASE
                )

                if in_items:
                    input_list.append(line.split())
                if out_items:
                    output_list.append(line.split())

        print("Input List :", input_list)
        print("Output list :", output_list)

        self.input_port = []
        self.output_port = []

        # creating list of input and output port with its weight
        for input in input_list:
            self.input_port.append(input[0] + ":" + input[2])
        for output in output_list:
            self.output_port.append(output[0] + ":" + output[2])

        print("Output Port List : ", self.output_port)
        print("Input Port List : ", self.input_port)

    def createCfuncModFile(self):

        # ############## Creating content for cfunc.mod file ############## #

        print("Starting With cfunc.mod file")
        cfunc = open('cfunc.mod', 'w')
        print("Building content for cfunc.mod file")

        comment = '''/* This is cfunc.mod file auto generated by \
        model_generation.py \nDeveloped by Fahim, Rahul at IIT Bombay */\n
                '''

        header = '''
        #include <stdio.h>
        #include <math.h>
        #include <string.h>
        #include <time.h>
        #include <sys/types.h>
        #include <stdlib.h>
        #include <unistd.h>
        #include <errno.h>

        '''

        if os.name == 'nt':
            header += '''
            #undef BOOLEAN
            #include<winsock2.h>
            '''
        else:
            header += '''
            #include <sys/socket.h>
            #include <netinet/in.h>
            #include <netdb.h>
            '''

        function_open = (
            '''void cm_''' + self.fname.split('.')[0] + '''(ARGS) \n{''')

        digital_state_output = []
        for item in self.output_port:
            digital_state_output.append(
                "Digital_State_t *_op_" + item.split(':')[0] +
                ", *_op_" + item.split(':')[0] + "_old;"
            )

        var_section = '''
            // Declaring components of Client
            FILE *log_client = NULL;
            log_client=fopen("client.log","a");
            int bytes_recieved;
            char send_data[1024];
            char recv_data[1024];
            char *key_iter;
            struct hostent *host;
            struct sockaddr_in server_addr;
            int sock_port = 5000+PARAM(instance_id);
        '''

        if os.name != 'nt':
            var_section += '''
                int socket_fd;
            '''

        temp_input_var = []
        for item in self.input_port:
            temp_input_var.append(
                "char temp_" + item.split(':')[0] + "[1024];"
            )

        # Start of INIT function
        init_start_function = '''
            if(INIT)
            {
                /* Allocate storage for output ports ''' \
                '''and set the load for input ports */
        '''

        cm_event_alloc = []
        cm_count_output = 0
        for item in self.output_port:
            cm_event_alloc.append(
                "cm_event_alloc(" +
                str(cm_count_output) + "," + item.split(':')[1] +
                "*sizeof(Digital_State_t));"
            )
            cm_count_output = cm_count_output + 1

        load_in_port = []
        for item in self.input_port:
            load_in_port.append(
                "for(Ii=0;Ii<PORT_SIZE(" + item.split(':')[0] +
                ");Ii++)\n\t\t{\n\t\t\tLOAD(" + item.split(':')[0] +
                "[Ii])=PARAM(input_load); \n\t\t}"
            )

        cm_count_ptr = 0
        cm_event_get_ptr = []
        for item in self.output_port:
            cm_event_get_ptr.append(
                "_op_" + item.split(':')[0] + " = _op_" +
                item.split(':')[0] +
                "_old = (Digital_State_t *) cm_event_get_ptr(" +
                str(cm_count_ptr) + ",0);"
            )

            cm_count_ptr = cm_count_ptr + 1

        systime_info = '''
                /*Taking system time info for log */
                time_t systime;
                systime = time(NULL);
                printf(ctime(&systime));
                printf("Client-Initialising GHDL...\\n\\n");
                fprintf(log_client,"Setup Client Server Connection at %s \\n"''' \
                ''',ctime(&systime));
        '''

        els_evt_ptr = []
        els_evt_count1 = 0
        els_evt_count2 = 0
        for item in self.output_port:
            els_evt_ptr.append("_op_" + item.split(":")[0] +
                               " = (Digital_State_t *) cm_event_get_ptr(" +
                               str(els_evt_count1) + "," +
                               str(els_evt_count2) + ");")
            els_evt_count2 = els_evt_count2 + 1
            els_evt_ptr.append("_op_" + item.split(":")[0] + "_old" +
                               " = (Digital_State_t *) cm_event_get_ptr(" +
                               str(els_evt_count1) + "," +
                               str(els_evt_count2) + ");")
            els_evt_count1 = els_evt_count1 + 1

        client_setup_ip = '''
                /* Client Setup IP Addr */
                FILE *fptr;
                int ip_count = 0;
                char* my_ip = malloc(16);

                char ip_filename[100];
        '''

        if os.name == 'nt':
            client_setup_ip += '''
                    sprintf(ip_filename, "''' + \
                os.getenv('LOCALAPPDATA').replace('\\', '/') + \
                '''/Temp/NGHDL_COMMON_IP_%d.txt", getpid());
            '''
        else:
            client_setup_ip += '''
                    sprintf(ip_filename, "/tmp/NGHDL_COMMON_IP_%d.txt",''' \
                    ''' getpid());
            '''

        client_setup_ip += '''
                fptr = fopen(ip_filename, "r");
                if (fptr)
                {
                    char line_ip[20];
                    int line_port;
                    while(fscanf(fptr, "%s %d", line_ip, &line_port) == 2) {
                        ip_count++;
                    }

                    fclose(fptr);
                }

                if (ip_count < 254) {
                    sprintf(my_ip, "127.0.0.%d", ip_count+1);
                } else {
                    sprintf(my_ip, "127.0.%d.1", (ip_count+3)%256);
                }

                fptr = fopen(ip_filename, "a");
                if (fptr)
                {
                    fprintf(fptr, "%s %d\\n", my_ip, sock_port);
                    fclose(fptr);
                } else {
                    perror("Client - cannot open Common_IP file ");
                    exit(1);
                }

                STATIC_VAR(my_ip) = my_ip;
        '''

        client_fetch_ip = '''
            /* Client Fetch IP Addr */
        '''

        if os.name == 'nt':
            client_fetch_ip += '''
                WSADATA WSAData;
                SOCKET socket_fd;
                WSAStartup(MAKEWORD(2, 2), &WSAData);
            '''

        client_fetch_ip += '''
            char* my_ip = STATIC_VAR(my_ip);

            host = gethostbyname(my_ip);
            fprintf(log_client,"Creating client socket \\n");
        '''

        create_socket = '''
            //Creating socket for client
            if ((socket_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
            {
                perror("Client - Error while creating client Socket ");
                fprintf(log_client,"Error while creating client socket \\n");
                exit(1);
            }

            printf("Client-Socket (Id : %d) created\\n", socket_fd);
            fprintf(log_client,"Client-Client Socket created ''' \
            '''successfully \\n");
            fprintf(log_client,"Client- Socket Id : %d \\n",socket_fd);

            // memset(&server_addr, 0, sizeof(server_addr));
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(sock_port);
            server_addr.sin_addr = *((struct in_addr *)host->h_addr);
            bzero(&(server_addr.sin_zero),8);

        '''

        connect_server = '''
            fprintf(log_client,"Client-Connecting to server \\n");

            //Connecting to server
            int try_limit=10;
            while(try_limit>0)
            {
                if (connect(socket_fd, (struct sockaddr*)&server_addr,''' \
                '''sizeof(struct sockaddr)) == -1)
                {
                    sleep(1);
                    try_limit--;
                    if(try_limit==0)
                    {
                        fprintf(stderr,"Connect- Error:Tried to connect server on port,''' \
                        '''failed...giving up \\n");
                        fprintf(log_client,"Connect- Error:Tried to connect server on ''' \
                        '''port, failed...giving up \\n");
                        exit(1);
                    }
                }
                else
                {
                    printf("Client-Connected to server \\n");
                    fprintf(log_client,"Client-Connected to server \\n");
                    break;
                }
            }
        '''

        # Assign bit value to every input
        assign_data_to_input = []
        for item in self.input_port:
            assign_data_to_input.append("\tfor(Ii=0;Ii<PORT_SIZE(" +
                                        item.split(':')[0] + ");Ii++)\n\
        \t{\n\t\tif( INPUT_STATE(" + item.split(':')[0] + "[Ii])==ZERO )\n\
        \t\t{\n\t\t\ttemp_" + item.split(':')[0] + "[Ii]='0';\n\t\t}\n\
        \t\telse\n\t\t{\n\t\t\ttemp_" + item.split(':')[0] + "[Ii]='1';\n\
        \t\t}\n\t}\n\ttemp_" + item.split(':')[0] + "[Ii]='\\0';\n\n")

        snprintf_stmt = []
        snprintf_count = 0
        snprintf_stmt.append(
            "\t//Sending and receiving data to-from server \n"
        )
        snprintf_stmt.append('\tsnprintf(send_data,sizeof(send_data),"')
        for item in self.input_port:
            snprintf_count = snprintf_count + 1
            snprintf_stmt.append(item.split(':')[0] + ":%s")
            if snprintf_count == len(self.input_port):
                snprintf_stmt.append('", ')
                internal_count = 0
                for item1 in self.input_port:
                    if internal_count == len(self.input_port):
                        pass
                    else:
                        snprintf_stmt.append("temp_" + item1.split(':')[0])
                        internal_count = internal_count + 1
                        if internal_count == len(self.input_port):
                            pass
                        else:
                            snprintf_stmt.append(",")
                snprintf_stmt.append(");")
            else:
                snprintf_stmt.append(",")

        send_data = '''

            if ( send(socket_fd,send_data,sizeof(send_data),0)==-1)
            {
                fprintf(stderr, "Client-Failure Sending Message \\n");
        '''

        if os.name == 'nt':
            send_data += '''
                    closesocket(socket_fd);
            '''
        else:
            send_data += '''
                    close(socket_fd);
            '''

        send_data += '''
                exit(1);
            }
            else
            {
                printf("Client-Message sent: %s \\n",send_data);
                fprintf(log_client,"Socket Id : %d & Message sent : %s \\n"''' \
                ''',socket_fd,send_data);
            }

        '''

        recv_data = '''

            bytes_recieved=recv(socket_fd,recv_data,sizeof(recv_data),0);
            if ( bytes_recieved <= 0 )
            {
                perror("Client-Either Connection Closed or Error ");
                exit(1);
            }
            recv_data[bytes_recieved] = '\\0';

            printf("Client-Message Received -  %s\\n\\n",recv_data);
            fprintf(log_client,"Message Received From Server-''' \
            '''%s\\n",recv_data);

        '''

        # Scheduling output event
        sch_output_event = []

        for item in self.output_port:
            sch_output_event.append(
                "\t/* Scheduling event and processing them */\n\
        \tif((key_iter=strstr(recv_data, " + '"' + item.split(':')[0] + ':"'")) != NULL)\n\
        \t{\n\
        \t\twhile(*key_iter++ != ':');\n\
        \t\tfor(Ii=0;*key_iter != ';';Ii++,key_iter++)\n\
        \t\t{\n\
        \t\t\tfprintf(log_client,\"Client-Bit val is %c \\n\",*key_iter);\n\
        \t\t\tif(*key_iter=='0')\n\t\t\t{\n\
        \t\t\t\t_op_" + item.split(':')[0] + "[Ii]=ZERO;\n\t\t\t}\n\
        \t\t\telse if(*key_iter=='1')\n\t\t\t{\n\
        \t\t\t\t_op_" + item.split(':')[0] + "[Ii]=ONE;\n\
        \t\t\t}\n\t\t\telse\n\t\t\t{\n\
        \t\t\t\tfprintf(log_client,\"Unknown value return from server \\n\");\
        \n\t\t\t\tprintf(\"Client-Unknown value return \\n\");\n\t\t\t}\n\n\
        \t\t\tif(ANALYSIS == DC)\n\t\t\t{\n\
        \t\t\t\tOUTPUT_STATE(" + item.split(':')[0] + "[Ii]) = _op_" + item.split(':')[0] + "[Ii];\n\
        \t\t\t}\n\t\t\telse if(_op_" + item.split(':')[0] + "[Ii] != _op_" + item.split(':')[0] + "_old[Ii])\n\
        \t\t\t{\n\t\t\t\tOUTPUT_STATE(" + item.split(':')[0] + "[Ii]) = _op_" + item.split(':')[0] + "[Ii];\n\
        \t\t\t\tOUTPUT_DELAY(" + item.split(':')[0] + "[Ii]) = ((_op_" + item.split(':')[0] + "[Ii] == ZERO) ? PARAM(fall_delay) : PARAM(rise_delay));\n\
        \t\t\t}\n\t\t\telse\n\t\t\t{\n\
        \t\t\t\tOUTPUT_CHANGED(" + item.split(':')[0] + "[Ii]) = FALSE;\n\t\t\t}\n\
        \t\t\tOUTPUT_STRENGTH(" + item.split(':')[0] + "[Ii]) = STRONG;\n\
        \t\t}\n\
        \t}\n")

        # Writing content in cfunc.mod file
        cfunc.write(comment)
        cfunc.write(header)
        cfunc.write("\n")
        cfunc.write(function_open)
        cfunc.write("\n")

        # Adding digital state Variable
        for item in digital_state_output:
            cfunc.write("\t" + item + "\n")

        # Adding variable declaration section
        cfunc.write(var_section)
        for item in temp_input_var:
            cfunc.write("\t" + item + "\n")
        cfunc.write("\n")

        # Adding INIT portion
        cfunc.write(init_start_function)
        for item in cm_event_alloc:
            cfunc.write(2 * "\t" + item)
            cfunc.write("\n")

        cfunc.write(2 * "\t" + "/* set the load for input ports. */")
        cfunc.write("\n")
        cfunc.write(2 * "\t" + "int Ii;")
        cfunc.write("\n")

        for item in load_in_port:
            cfunc.write(2 * "\t" + item)
            cfunc.write("\n")
        cfunc.write("\n")
        cfunc.write(2 * "\t" + "/*Retrieve Storage for output*/")
        cfunc.write("\n")
        for item in cm_event_get_ptr:
            cfunc.write(2 * "\t" + item)
            cfunc.write("\n")
        cfunc.write(systime_info)
        cfunc.write("\n")
        cfunc.write(client_setup_ip)
        cfunc.write("\n")
        cfunc.write("\t\tchar command[1024];\n")

        if os.name == 'nt':
            self.digital_home = self.parser.get('NGHDL', 'DIGITAL_MODEL')
            self.digital_home = os.path.join(self.digital_home, "ghdl")

            cmd_str2 = "/start_server.sh %d %s & read" + "\\" + "\"" + "\""
            cmd_str1 = os.path.normpath(
                "\"" + self.digital_home + "/" +
                self.fname.split('.')[0] + "/DUTghdl/"
            )
            cmd_str1 = cmd_str1.replace("\\", "/")

            cfunc.write(
                '\t\tsnprintf(command,1024, "start mintty.exe -t ' +
                '\\"VHDL-Testbench Logs\\" -h always bash.exe -c ' +
                '\\' + cmd_str1 + cmd_str2 + ', sock_port, my_ip);'
            )
        else:
            cfunc.write(
                '\t\tsnprintf(command,1024,"' + self.home +
                '/nghdl-simulator/src/xspice/icm/ghdl/' +
                self.fname.split('.')[0] +
                '/DUTghdl/start_server.sh %d %s &", sock_port, my_ip);'
            )

        cfunc.write('\n\t\tsystem(command);')
        cfunc.write("\n\t}")
        cfunc.write("\n")
        cfunc.write("\telse\n\t{\n")

        for item in els_evt_ptr:
            cfunc.write(2 * "\t" + item)
            cfunc.write("\n")
        cfunc.write("\t}")
        cfunc.write("\n\n")

        cfunc.write(client_fetch_ip)
        cfunc.write(create_socket)
        cfunc.write(connect_server)

        cfunc.write("\t//Formating data for sending it to client\n")
        cfunc.write("\tint Ii;\n\n")

        for item in assign_data_to_input:
            cfunc.write(item)

        for item in snprintf_stmt:
            cfunc.write(item)

        cfunc.write(send_data)
        cfunc.write(recv_data)

        for item in sch_output_event:
            cfunc.write(item)

        # Close socket fd
        if os.name == 'nt':
            cfunc.write("\tclosesocket(socket_fd);\n\n")
        else:
            cfunc.write("\tclose(socket_fd);\n\n")

        # close log_client file
        cfunc.write("\tfclose(log_client);")

        # Close cm_ function
        cfunc.write("\n}")
        cfunc.close()

    def createIfSpecFile(self):

        # ################### Creating ifspec.ifs file #################### #

        print("Starting with ifspec.ifs file")
        ifspec = open('ifspec.ifs', 'w')

        print("Gathering Al the content for ifspec file")

        ifspec_comment = '''
        /*
        SUMMARY: This file is auto generated and it contains the interface
         specification for the code model. */\n
        '''

        name_table = 'NAME_TABLE:\n\
        C_Function_Name: cm_' + self.fname.split('.')[0] + '\n\
        Spice_Model_Name: ' + self.fname.split('.')[0] + '\n\
        Description: "Model generated from ghdl code ' + self.fname + '" \n'

        # Input and Output Port Table
        in_port_table = []
        out_port_table = []

        for item in self.input_port:
            port_table = 'PORT_TABLE:\n'
            port_name = 'Port_Name:\t' + item.split(':')[0] + '\n'
            description = (
                'Description:\t"input port ' + item.split(':')[0] + '"\n'
            )
            direction = 'Direction:\tin\n'
            default_type = 'Default_Type:\td\n'
            allowed_type = 'Allowed_Types:\t[d]\n'
            vector = 'Vector:\tyes\n'
            vector_bounds = (
                'Vector_Bounds:\t[' + item.split(':')[1] +
                ' ' + item.split(":")[1] + ']\n'
            )
            null_allowed = 'Null_Allowed:\tno\n'

            # Insert detail in the list
            in_port_table.append(
                port_table + port_name + description +
                direction + default_type + allowed_type +
                vector + vector_bounds + null_allowed
            )

        for item in self.output_port:
            port_table = 'PORT_TABLE:\n'
            port_name = 'Port_Name:\t' + item.split(':')[0] + '\n'
            description = (
                'Description:\t"output port ' + item.split(':')[0] + '"\n'
            )
            direction = 'Direction:\tout\n'
            default_type = 'Default_Type:\td\n'
            allowed_type = 'Allowed_Types:\t[d]\n'
            vector = 'Vector:\tyes\n'
            vector_bounds = (
                'Vector_Bounds:\t[' + item.split(':')[1] +
                ' ' + item.split(":")[1] + ']\n'
            )
            null_allowed = 'Null_Allowed:\tno\n'

            # Insert detail in the list
            in_port_table.append(
                port_table + port_name + description +
                direction + default_type + allowed_type +
                vector + vector_bounds + null_allowed
            )

        parameter_table = '''

        PARAMETER_TABLE:
        Parameter_Name:     instance_id                  input_load
        Description:        "instance_id"                "input load value (F)"
        Data_Type:          real                         real
        Default_Value:      0                            1.0e-12
        Limits:             -                            -
        Vector:              no                          no
        Vector_Bounds:       -                           -
        Null_Allowed:       yes                          yes

        PARAMETER_TABLE:
        Parameter_Name:     rise_delay                  fall_delay
        Description:        "rise delay"                "fall delay"
        Data_Type:          real                        real
        Default_Value:      1.0e-9                      1.0e-9
        Limits:             [1e-12 -]                   [1e-12 -]
        Vector:              no                          no
        Vector_Bounds:       -                           -
        Null_Allowed:       yes                         yes
        '''

        static_table = '''

        STATIC_VAR_TABLE:

        Static_Var_Name:    my_ip
        Data_Type:          pointer
        Description:        "connect to ghdlserver through this ip"

        '''

        # Writing all the content in ifspec file
        ifspec.write(ifspec_comment)
        ifspec.write(name_table + "\n\n")

        for item in in_port_table:
            ifspec.write(item + "\n")

        ifspec.write("\n")

        for item in out_port_table:
            ifspec.write(item + "\n")

        ifspec.write("\n")
        ifspec.write(parameter_table)
        ifspec.write("\n")
        ifspec.write(static_table)
        ifspec.close()

    def createTestbench(self):

        # #################### Creating testbench file ##################### #

        print("Starting with testbench file")

        testbench = open(self.fname.split('.')[0] + '_tb.vhdl', 'w')
        print(self.fname.split('.')[0] + '_tb.vhdl')

        # comment
        comment_vhdl = "------------------------------------------------------"
        comment_vhdl += "--------------------------\n"
        comment_vhdl += "--This testbench has been created by "
        comment_vhdl += "Ambikeshwar Srivastava, Rahul Paknikar \n"
        comment_vhdl += "--------------------------- FOSSEE, IIT Bombay ------"
        comment_vhdl += "---------------------------\n"
        comment_vhdl += "-----------------------------------------------------"
        comment_vhdl += "---------------------------\n"

        # Adding header, entity and architecture statement
        tb_header = '''
        library ieee;
        use ieee.std_logic_1164.all;
        use ieee.numeric_std.all;
        library work;
        use work.Vhpi_Foreign.all;
        use work.Utility_Package.all;
        use work.sock_pkg.all;

        '''

        tb_entity = ("entity " + self.fname.split('.')[0] +
                     "_tb is\nend entity;\n\n")

        arch = ("architecture " + self.fname.split('.')[0] + "_tb_beh of " +
                self.fname.split('.')[0] + "_tb is\n")

        # Adding components
        components = []
        components.append("\tcomponent " + self.fname.split('.')[0] +
                          " is\n\t\tport(\n\t\t\t\t")

        port_vector_count = 0

        for item in self.input_port:
            if self.port_vector_info[port_vector_count]:
                components.append(
                    item.split(':')[0] + ": in std_logic_vector(" +
                    str(int(item.split(':')[1]) - int(1)) +
                    " downto 0);\n\t\t\t\t"
                )
            else:
                components.append(
                    item.split(':')[0] + ": in std_logic;\n\t\t\t\t"
                )

            port_vector_count += 1
            # if item.split(":")[1] != '1':
            #     components.append(
            #         item.split(':')[0] + ": in std_logic_vector(" +
            #         str(int(item.split(':')[1])-int(1)) + " downto 0);" +
            #         "\n\t\t\t\t"
            #     )
            # else:
            #     components.append(
            #         item.split(':')[0] + ": in std_logic_vector(" +
            #         str(int(item.split(':')[1])-int(1)) + " downto 0);" +
            #         "\n\t\t\t\t"
            #     )
        for item in self.output_port[:-1]:
            if self.port_vector_info[port_vector_count]:
                components.append(
                    item.split(':')[0] + ": out std_logic_vector(" +
                    str(int(item.split(':')[1]) - int(1)) +
                    " downto 0);\n\t\t\t\t"
                )
            else:
                components.append(
                    item.split(':')[0] + ": out std_logic;\n\t\t\t\t"
                )

            port_vector_count += 1

        if self.port_vector_info[port_vector_count]:
            components.append(
                self.output_port[-1].split(':')[0] +
                ": out std_logic_vector(" +
                str(int(self.output_port[-1].split(':')[1]) - int(1)) +
                " downto 0)\n\t\t\t\t"
            )
        else:
            components.append(self.output_port[-1].split(':')[0] +
                              ": out std_logic\n\t\t\t\t")
            # if item.split(":")[1] != '1':
            #    components.append(item.split(':')[0]+":
            # out std_logic_vector("
            #   +str(int(item.split(':')[1])-int(1))+" downto 0)\n\t\t\t\t")
            # else:
            #    components.append(item.split(':')[0]+":
            # out std_logic_vector("
            #   +str(int(item.split(':')[1])-int(1))+" downto 0)\n\t\t\t\t")

        components.append(");\n")
        components.append("\tend component;\n\n")

        # Adding signals
        signals = []
        signals.append("\tsignal clk_s : std_logic := '0';\n")

        port_vector_count = 0

        for item in self.input_port:
            if self.port_vector_info[port_vector_count]:
                signals.append(
                    "\tsignal " + item.split(':')[0] + ": std_logic_vector(" +
                    str(int(item.split(':')[1]) - int(1)) + " downto 0);\n"
                )
            else:
                signals.append(
                    "\tsignal " + item.split(':')[0] + ": std_logic;\n"
                )
            port_vector_count += 1

            # if item.split(":")[1] != '1':
            #    signals.append("\tsignal "+item.split(':')[0]+":
            #                   std_logic_vector("+str(int(item.split(':')[1])-
            #                   int(1))+" downto 0);\n")
            # else:
            #    signals.append("\tsignal "+item.split(':')[0]+":
            #                   std_logic_vector("+str(int(item.split(':')[1])-
            #                   int(1))+" downto 0);\n")

        for item in self.output_port:
            if self.port_vector_info[port_vector_count]:
                signals.append(
                    "\tsignal " + item.split(':')[0] + ": std_logic_vector(" +
                    str(int(item.split(':')[1]) - int(1)) + " downto 0);\n"
                )
            else:
                signals.append(
                    "\tsignal " + item.split(':')[0] + ": std_logic;\n"
                )

            port_vector_count += 1
            # if item.split(":")[1] != '1':
            #     signals.append(
            #         "\tsignal " + item.split(':')[0] + ":std_logic_vector(" +
            #         str(int(item.split(':')[1]) - int(1)) + " downto 0);\n"
            #     )
            # else:
            #     signals.append(
            #         "\tsignal " + item.split(':')[0] + ":std_logic_vector(" +
            #         str(int(item.split(':')[1]) - int(1)) + " downto 0);\n"
            #     )

        # Adding mapping part
        map = []
        map.append("\tu1 : " + self.fname.split('.')[0] + " port map(\n")

        for item in self.input_port:
            map.append("\t\t\t\t" + item.split(':')[0] +
                       " => " + item.split(':')[0] + ",\n")

        for item in self.output_port:
            if self.output_port.index(item) == len(self.output_port) - 1:
                map.append("\t\t\t\t" + item.split(':')[0] +
                           " => " + item.split(':')[0] + "\n")
            else:
                map.append("\t\t\t\t" + item.split(':')[0] +
                           " => " + item.split(':')[0] + ",\n")
        map.append("\t\t\t);")

        # Testbench Clock
        tb_clk = "clk_s <= not clk_s after 5 us;\n\n"

        # Adding Process block for Vhpi
        process_Vhpi = []
        process_Vhpi.append(
            "process\n\t\tvariable sock_port : integer;" +
            "\n\t\ttype string_ptr is access string;" +
            "\n\t\tvariable sock_ip : string_ptr;" +
            "\n\t\tbegin\n\t\tsock_port := sock_port_fun;" +
            "\n\t\tsock_ip := new string'(sock_ip_fun);" +
            "\n\t\tVhpi_Initialize(sock_port," +
            "Pack_String_To_Vhpi_String(sock_ip.all));" +
            "\n\t\twait until clk_s = '1';" +
            "\n\t\twhile true loop\n\t\t\twait until clk_s = '0';" +
            "\n\t\t\tVhpi_Listen;\n\t\t\twait for 1 us;\n\t\t\t" +
            "Vhpi_Send;" +
            "\n\t\tend loop;\n\t\twait;\n\tend process;\n\n"
        )

        # Adding process block
        process = []
        process.append("\tprocess\n")
        process.append("\t\tvariable count : integer:=0;\n")

        for item in self.input_port:
            process.append(
                "\t\tvariable " + item.split(':')[0] + "_v : VhpiString;\n"
            )

        for item in self.output_port:
            process.append(
                "\t\tvariable " + item.split(':')[0] + "_v : VhpiString;\n"
            )

        process.append("\t\tvariable obj_ref : VhpiString;\n")
        process.append("\tbegin\n")
        process.append("\t\twhile true loop\n")
        process.append("\t\t\twait until clk_s = '0';\n\n")

        port_vector_count = 0

        for item in self.input_port:
            process.append(
                '\t\t\tobj_ref := Pack_String_To_Vhpi_String("' +
                item.split(':')[0] + '");\n'
            )
            process.append(
                '\t\t\tVhpi_Get_Port_Value(obj_ref,' +
                item.split(':')[0] + '_v,' + item.split(':')[1] + ');\n'
            )

            if self.port_vector_info[port_vector_count]:
                process.append(
                    '\t\t\t' + item.split(':')[0] +
                    ' <= Unpack_String(' + item.split(':')[0] + '_v,' +
                    item.split(':')[1] + ');\n'
                )
            else:
                process.append(
                    '\t\t\t' + item.split(':')[0] +
                    ' <= To_Std_Logic(' + item.split(':')[0] + '_v' + ');\n'
                )

            port_vector_count += 1
            process.append("\n")

        process.append('\t\t\twait for 1 us;\n')

        for item in self.output_port:
            if self.port_vector_info[port_vector_count]:
                process.append(
                    '\t\t\t' + item.split(':')[0] +
                    '_v := Pack_String_To_Vhpi_String' +
                    '(Convert_SLV_To_String(' +
                    item.split(':')[0] + '));\n'
                )
            else:
                process.append(
                    '\t\t\t' + item.split(':')[0] +
                    '_v := Pack_String_To_Vhpi_String(To_String(' +
                    item.split(':')[0] + '));\n'
                )

            port_vector_count += 1

            process.append(
                '\t\t\tobj_ref := Pack_String_To_Vhpi_String("' +
                item.split(':')[0] + '");\n'
            )
            process.append(
                '\t\t\tVhpi_Set_Port_Value(obj_ref,' +
                item.split(':')[0] + '_v,' + item.split(':')[1] + ');\n'
            )
            process.append("\n")

        process.append(
            '\t\t\treport "Iteration - "' +
            "& integer'image(count) severity note;\n"
        )
        process.append('\t\t\tcount := count + 1;\n')
        process.append("\t\tend loop;\n")
        process.append("\tend process;\n\n")
        process.append("end architecture;")

        # Writing all the components to testbench file
        testbench.write(comment_vhdl)
        testbench.write(tb_header)
        testbench.write(tb_entity)
        testbench.write(arch)

        for item in components:
            testbench.write(item)

        for item in signals:
            testbench.write(item)

        testbench.write("\n\n")

        testbench.write("begin\n\n")

        for item in map:
            testbench.write(item)

        testbench.write("\n\t" + tb_clk)

        for item in process_Vhpi:
            testbench.write(item)

        for item in process:
            testbench.write(item)

        testbench.close()

    def createServerScript(self):

        # ####### Creating and writing components in start_server.sh ####### #
        self.digital_home = self.parser.get('NGHDL', 'DIGITAL_MODEL')
        self.digital_home = os.path.join(self.digital_home, "ghdl")

        start_server = open('start_server.sh', 'w')

        start_server.write("#!/bin/bash\n\n")
        start_server.write(
            "###This server run ghdl testbench for infinite time till " +
            "Ngspice sends kill signal to stop it\n\n"
        )

        if os.name == 'nt':
            pathstr = self.digital_home + "/" + \
                self.fname.split('.')[0] + "/DUTghdl/"
            pathstr = pathstr.replace("\\", "/")
            start_server.write("cd " + pathstr + "\n")
        else:
            start_server.write("cd " + self.digital_home +
                               "/" + self.fname.split('.')[0] + "/DUTghdl/\n")

        start_server.write("chmod 775 sock_pkg_create.sh &&\n")
        start_server.write("./sock_pkg_create.sh $1 $2 &&\n")
        start_server.write("ghdl -i *.vhdl &&\n")
        #start_server.write("ghdl -a *.vhdl &&\n")
        #=============================================
        # Modified to compile in the required order
        #=============================================

        start_server.write("ghdl -a Utility_Package.vhdl &&\n")
        start_server.write("ghdl -a Vhpi_Package.vhdl &&\n")
        start_server.write("ghdl -a sock_pkg.vhdl &&\n")

        #=============================================
        start_server.write("ghdl -a " + self.fname + " &&\n")
        start_server.write(
            "ghdl -a " + self.fname.split('.')[0] + "_tb.vhdl  &&\n"
        )

        if os.name == 'nt':
            start_server.write("ghdl -e -Wl,ghdlserver.o " +
                               "-Wl,libws2_32.a " +
                               self.fname.split('.')[0] + "_tb &&\n")
            start_server.write("./" + self.fname.split('.')[0] + "_tb.exe")
        else:
            start_server.write("ghdl -e -Wl,ghdlserver.o " + self.fname.split('.')[0] + "_tb &&\n")
            start_server.write("./" + self.fname.split('.')[0] + "_tb --vcd=" + self.fname.split('.')[0] + "_tb.vcd\n")
            start_server.write( "gtkwave " + self.fname.split('.')[0] + "_tb.vcd 2>/dev/null")

        start_server.close()

    def createSockScript(self):

        # ########### Creating and writing in sock_pkg_create.sh ########### #

        sock_pkg_create = open('sock_pkg_create.sh', 'w')

        sock_pkg_create.write("#!/bin/bash\n\n")
        sock_pkg_create.write(
            "##This file creates sock_pkg.vhdl file and sets the port " +
            "and ip from parameters passed to it\n\n"
        )
        sock_pkg_create.write("echo \"library ieee;\n")
        sock_pkg_create.write("package sock_pkg is\n")
        sock_pkg_create.write("\tfunction sock_port_fun return integer;\n")
        sock_pkg_create.write("\tfunction sock_ip_fun return string;\n")
        sock_pkg_create.write("end;\n\n")
        sock_pkg_create.write("package body sock_pkg is\n")
        sock_pkg_create.write("\tfunction sock_port_fun return integer is\n")
        sock_pkg_create.write("\t\tvariable sock_port : integer;\n")
        sock_pkg_create.write("\t\t\tbegin\n")
        sock_pkg_create.write("\t\t\t\tsock_port := $1;\n")
        sock_pkg_create.write("\t\t\t\treturn sock_port;\n")
        sock_pkg_create.write("\t\t\tend function;\n\n")
        sock_pkg_create.write("\tfunction sock_ip_fun return string is\n")
        sock_pkg_create.write("\t\ttype string_ptr is access string;\n")
        sock_pkg_create.write("\t\tvariable sock_ip : string_ptr;\n")
        sock_pkg_create.write("\t\t\tbegin\n")
        sock_pkg_create.write('\t\t\t\tsock_ip := new string\'(\\"$2\\");\n')
        sock_pkg_create.write("\t\t\t\treturn sock_ip.all;\n")
        sock_pkg_create.write("\t\t\tend function;\n\n")
        sock_pkg_create.write("\t\tend package body;\" > sock_pkg.vhdl")
