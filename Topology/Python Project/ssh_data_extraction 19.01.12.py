# This code is part of the ssh connection code

import re
import time

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

# modules installed and status of modules -> show diag (do we need a regex?)
# show interfaces, show ip int br -> interface description and status (do we need regex?)
# show cdp neighbors detail | include Device ID -> can be useful in neighbor discovery?

''' I can't test this code on my machine, due to my issue with ssh.
Please test and if there is a problem or we need more regexes, tell me'''
        
