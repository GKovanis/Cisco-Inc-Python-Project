# Automated Network Documentation Project

You are new in the company. Previous network engineer left the company and no documentation about network is available. Your manager gave you couple of weeks to familiarize yourself with the network and **build an automated solution to document the environment**.  You have full freedom to decide how to collect the information and how to document the environment.

## What you know

- IP range of your network - the range is stored in the range.txt file.
- Devices are either Cisco IOS devices or NX-OS devices (Nexus and MDS)
- All passwords of devices are stored in the file password.txt. At least one password from the file will work for a device.

## Minimal requirements that your manager expects

He wants to know all available devices in the network. For each device, he wants to know:
- Hardware version
- OS version running on the device
- Management IP address
- Password
- Modules which are installed on the device - and status of each module
- He wants to know the topology
- He wants to see the interface description and interface status for each interface on each device.


## End Of Life/End of Support
Your manager is dreaming to have a tool which will be able to report end of life/end of support for the available hardware/OS in the network.

## Prerequisites

What things you need to install before running our project:

- GNS3 network simulation program
- python 2.7 or higher
- Cisco IOS router image file 

Router image used in our topology:
- **c3725**

Libraries used in our script:

- **re** : regexes
- **time**: introducing delay
- **paramiko**: ssh connection
- **threading**: apply multi-threading
- **os.path**: functions on pathnames
- **subprocess**: used for ping our routers
- **sys**: access to parameters used by python interpreter
- **networkx**: used to create the topology graph
- **mathplotlib.pyplot**: used to plot the topology
- **ast.literal_eval**:  raises an exception if the input isn't a valid Python datatype
- **requests**: used to create REST requests
## Setting up the project environment
- Download and install all of the prerequisites.
- Download and open "**Python Project.gns3**" file, located in *Topology/Python Project*.
- Create a new IOS router template on gns3, from *gns3>Preferences>Dynamips>IOS routers>New*.
- In the routers, uncheck the option to *Automatically delete NVRAM and disk files*.
- Copy/Paste the router configurations provided in *Topology>Router Configurations* for each Router.
- Generate an idle_pc value, it reduces cpu load. If available, use the idle-pc values that Cisco recommends for the corresponding routers. 
- Press the "**Start**" button, to start the gns3 simulation.
- Create a folder and include the folder **Results** and the files: **main.py**, **password.txt** and **range.txt**.
- Open terminal, change directory to the folder you created and run the **main.py** script.

## Run the project


### Minimal Requirements
Our project is deployed by executing the **main.py** script. To begin, end user has to provide the IP range of the network, inside the range.txt file and the SSH passwords of the routers, inside the password.txt file. Next, we ping each of the ip addresses provided in the range.txt file, to find the assigned ones. Then, **main.py** attempts to start an SSH session with each router, using the passwords provided in password.txt one by one. After the password that matches with the router's SSH configuration is found, connection is established. During connection, the **main.py** script sends certain show commands to the router, to extract the information in the "**Minimal Requirements that your manager expects**" section. We then apply some regexes, in order to extract only the piece of information that we need from the whole output. After we apply them, we write the results in a .txt file. We also create a graph of the routers in our topology, by extracting the neighbours of every router(node) and correlate them using the add_edge function. This graph can be found here: *Topology/Python Project/Results*, its name is topology.png. The last part of our code was to define a function for multi-threading, so that it is possible for our functions to run in parallel for every router in the topology.  
### End Of Life/End Of Support
For this part, in order to get the End of Life and End of Support information of each router, we had to connect to the routers' supplier company website. To get this information, it was necessary to request for an authorization token. We performed this request by sending to the company's server a POST command, with the clients ID and secret password included, which were given to us by the company. After we received the token, we asked for the End of Life and End of Support information, by sending a GET command with the Serial Number of every router of our topology. We used regexes to isolate only the 2 dates we needed from the json output that was send by the server, as a reply to our GET request.     

## Testing
Running the **main.py** script, outputs 8 .txt files, one for each router. These files can be found in *Topology/Python Project/Results* path. The output for router R1, for example, looks like this:

Information for Router : R1.pyproject
Router's Hardware Version is: C3725-ADVENTERPRISEK9-M
The OS running on the router is: Version 12.4(25d)
Management IP address is: 192.168.2.101
Router's password is: python
Router's SN: FTX0945W0MY
Router's installed modules and status is:
NAME: "3725 chassis", DESCR: "3725 chassis"
PID:                   , VID: 0.1, SN: FTX0945W0MY
Router's interface description and status are:
FastEthernet0/0            unassigned      YES NVRAM  administratively down down
FastEthernet0/1            192.168.2.101   YES NVRAM  up                    up  Device Neighbors are: 
R2.pyproject,R3.pyproject,R4.pyproject,R5.pyproject,R6.pyproject,R7.pyproject,R8.pyproject

We also run the command:  **python main.py > log.txt**, to create a log file with the ping statistics of our ping attemps to find the assigned ones. This log file is located in the following path: *Topology/Python Project*.

For the *End Of Life/End Of Support* part, the output should look like this:

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Serial Number : FTX0945W0MY
Last Date of Support : 2016-10-31
Last Date of Life : 2016-01-30

Every group of lines represent the End Of Life/End Of Support of a specific router, identified by the Serial Number value, in the first row. 
This output can be found in the *Topology/Python Project/Results* path.



## Authors
- **George Kovanis**
- **Fivos Andriotis**
- **Abetare Shabani**
- **Alexandros Pagonis**