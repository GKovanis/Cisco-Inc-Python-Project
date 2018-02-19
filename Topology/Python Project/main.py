import re
import time
import paramiko #needs to be imported

#a function to get the network information in ip/cidr_net_mask format and return
#a list with all the ips in the network
def generate_ip_list(ip_mask):

    #split the network and the ip mask
    ip_mask = ip_mask.split("/")
    net = ip_mask[0]
    cidr = int(ip_mask[1])
    net = net.split(".")
    #find the ip range
    net_range = 32 - cidr
    #generate the ips in the network
    ip_list = []
    for i in range(1,net_range+1):
        ip_list.append(net[0]+"."+net[1]+"."+net[2]+"."+str(i))
    return ip_list

#a function that brute forces every machine to find its password and returns a
# [ip,password] list
def cracker(ip_list):

    pass_file = open("password.txt", 'r')
    pass_list = map(str.rstrip, pass_file.readlines())
    for ip in ip_list:
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
                #Closing the connection
                session.close()
                credentials.append([ip,password])
                break
            except paramiko.AuthenticationException:

    return credentials

def extract_data(): #alex
    # Commands for ssh data extraction

    selected_cisco_commands = '''show version&\  # hardware version, OS version
                              show interfaces&\  # interface description, need all(?)
                              show ip int brief | include (Ethernet|Serial)&\  # interfaces status, need all
                              show diag&\  # modules installed and status (?)
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

    dev_os = re.search(r"Version \d.\.\d\(\w+\)", output)

    dev_cdp_neighbors = re.findall(r"Device ID: (.+)\r\n", output)
    all_cdp_neighbors = ','.join(dev_cdp_neighbors)
    return all_cdp_neighbors
    # modules installed and status of modules -> show diag (do we need a regex?)
    # show interfaces, show ip int br -> interface description and status (do we need regex?)
    # show cdp neighbors detail | include Device ID -> can be useful in neighbor discovery?

    ''' I can't test this code on my machine, due to my issue with ssh.
    Please test and if there is a problem or we need more regexes, tell me'''

#main
range_file = open("range.txt", 'r')
net = range_file.readlines()[0].rstrip("/n")
ip_list = generate_ip_list(net)
credentials = cracker(ip_list)
neighbouring_list = []
for [ip,password] in credentials:
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
        neighbours = extract_data()
        #Closing the connection
        session.close()
        #forming a [ip, neighbours] list
        neighbouring_list.append([ip,neighbors])#Abe i imagine that something like this will suit you
    except paramiko.SSHException:
        print"Error connecting or host timed out\n"
