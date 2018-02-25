import re
import time
import paramiko #needs to be imported
import threading
import os.path
import subprocess
import sys
import networkx as nx
import matplotlib.pyplot as plt
from ast import literal_eval
import requests

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
#The IPs that will reply to our pings are the ones that have a router, we only need to keep them
def ip_validate(ip_list):
    clean_list = []
    for ip in ip_list:
        ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])
        if ping_reply == 0:
            clean_list.append(ip)
    return clean_list

#a function that brute forces every machine to find its password and returns an
# [ip,password] list
def cracker(ip):
    #Open and read the file with the passwords
    pass_file = open("password.txt", 'r')
    pass_list = map(str.rstrip, pass_file.readlines())
    #Brute Force every password until we find the correct one
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
	    #Sleep so we make sure we get all the data properly
            time.sleep(1)
            Serial = extract_data(connection,ip,password)
	    #S_nums contains the serial numbers of all routers to used for FindEndOf
	    S_nums.append(Serial)
            #Closing the connection
            session.close()
	    break
        except paramiko.AuthenticationException:
	    continue
    return

def extract_data(connection,ip,password):
    # Necessary Commands for ssh data extraction
    selected_cisco_commands = '''show version&
                              show ip int brief | include (Ethernet|Serial)&
                              show diag&
                              show inventory&
                              show cdp neighbors detail | include Device ID''' 

    #Splitting commands by the "&" character

    command_list = selected_cisco_commands.split("&")

    #Writing each line in the command string to the device

    for each_line in command_list:
        connection.send(each_line + '\n')
        time.sleep(3)

    #Checking command output for IOS syntax errors
    output = connection.recv(65535)

    # Log if all the parameters were extracted successfully or if we had any errors during the process
    if re.search(r"% Invalid input detected at", output):
        print("* There was at least one IOS syntax error on device {}".format(ip))

    else:
        print("* All parameters were extracted from device {}".format(ip))
    
    # Regex for Router Hostname
    hostname = re.search(r"(\w+\d+)#",output)
    hostname = hostname.group(1)+'.pyproject'

    # Regex for Router Hardware Version
    hardware_version = re.search(r"C\d+-\w+-\w",output)

    # Regex for Router's interfaces
    ip_int_brief = re.findall(r"((FastEthernet|Serial)\d\/\d.*\n)", ''.join(output))
    ip_int_br = [''.join(x[0]) for x in ip_int_brief]
    ip_int_br = '\n'.join(ip_int_br) #convert list to string

    # Regex for Router's installed modules
    inventory = re.findall(r"NAME:.*\nPID:.*", ''.join(output))
    inv = '\n'.join(inventory) #convert list to string

    # Regex for Router OS Version
    dev_os = re.search(r"Version \d.\.\d\(\w+\)", output)

    # Regex for Router's CDP Neighbors
    dev_cdp_neighbors = re.findall(r"Device ID: (.+)\r\n", output)
    all_cdp_neighbors = ','.join(dev_cdp_neighbors)

    # Add edges to create topology
    for i in range(len(dev_cdp_neighbors)):
	G.add_edge(hostname,dev_cdp_neighbors[i])

    # Regex for Router Serial Number
    SN = re.search(r"Chassis Serial Number *: (.*)",output) 

    # Write Results in a txt file with Router's IP as name
    filename = 'Results/%s.txt' % ip
    with open(filename,'w') as file1:
	file1.write("Information for Router : " + hostname + '\n\n')
	file1.write("Router's Hardware Version is: "+hardware_version.group(0)+'\n')
	file1.write("\nThe OS running on the router is: "+dev_os.group(0)+'\n')
	file1.write("\nManagement IP address is: "+ip+'\n')
	file1.write("\nRouter's password is: "+password+'\n')
        file1.write("\nRouter's SN: "+SN.group(1)+'\n')
	file1.write("\nRouter's installed modules and status is:\n"+inv+'\n')
	file1.write("\nRouter's interface description and status are:\n"+ip_int_br+'\n')
	file1.write("Device Neighbors are: \n"+all_cdp_neighbors+'\n')

    #We return the Serial Number which is needed to find EOL/EOS of each device
    return SN.group(1)


#Creating threads
def create_threads(ip_list):
    threads = []
    for ip in ip_list:
        th = threading.Thread(target = cracker, args = (ip,))   #args is a tuple with a single element
        th.start()
        threads.append(th)
    for th in threads:
        th.join()

def FindEndOf(S_Nums):
    # generate token
    r = requests.post('https://cloudsso.cisco.com/as/token.oauth2?client_id=k9n8bfgkfxdxv8nuen4ys4pp&grant_type=client_credentials&client_secret=kgSRMEzANeHgHbRyxuGJP65e')

    # convert unicode to dict
    dic = literal_eval(str(r.text))
    token= dic['access_token']

    #Run this process for each Serial Number
    for i in range(len(S_Nums)):
	S_Nums[i] = S_Nums[i].rstrip('\r')
    # response of API
    StringNums = ','.join(S_nums)
	
    response = requests.get('https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1/'+StringNums+'?responseencoding=json', headers={'Authorization': 'Bearer '+ token})
    data = response.text

    #Regexes to find EOS / EOL of Device
    EndofSupport = re.findall(r"LastDateOfSupport\":{\"value\":\"(\d+\-\d+\-\d+)",data)
    EndofLife = re.findall(r"EndOfServiceContractRenewal\":{\"value\":\"(\d+\-\d+\-\d+)",data)
    EOXInputValue = re.findall(r"EOXInputValue\":\"(.*?)\"}",data)

# Write the results in a .txt file
    filename = 'Results/Device EOS-EOL.txt'
    with open(filename,'w') as file1:
        for i in range(0,len(EndofLife)):

            file1.write("Serial Number : " + EOXInputValue[i] + '\n')
            file1.write("Last Date of Support : " + EndofSupport[i] + '\n')
            file1.write("Last Date of Life : " + EndofLife[i] + '\n\n')

#Initializations
S_nums = []
G = nx.Graph()

#Open and Read IP range .txt file
range_file = open("range.txt", 'r')
net = range_file.readlines()[0].rstrip("\n")
net = net.split(',')

# Turn the IP Ranges into distinct IPs
ip_list = generate_ip_list(net)

# Keep only the valid IPs for current topology
clean_list = ip_validate(ip_list)

# Create threads to do entire process in parallel
create_threads(clean_list)

# Find the End-Of-Life and End-Of-Support of each device
FindEndOf(S_nums)

# Draw topology and save it in a .png image
nx.draw(G)
plt.savefig('Results/topology.png')
