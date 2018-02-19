# Automated Network Documentation Project

You are new in the company. Previous network engineer left the company and no documentation about network is available. Your manager gave you couple of weeks to familiarize yourself with the network and **build an automated solution to document the environment**.  You have full freedom to decide how to collect the information and how to document the environment.

## What you know

- Ip range of your network - the range is stored in the range.txt file.
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

### Prerequisites

What things you need to install before running our project:

- GNS3 network simulation program
- python 2.7 or higher
- Virtualbox

### Setting up the project environment
- Download and install all of the prerequisites.
- Download and open "**Python Project.gns3**" file, located in *Topology/Python Project*.
- Press the "**Start button**", to start the gns3 simulation. After the debian7 virtual machine dialog opens, enter the password: **admin**, when prompted.
- Create a folder and include the files: **main.py**, **password.txt** and **range.txt**.
- Open terminal, cd to your folder and run the main.py file.

## Running the tests



### Break down into end to end tests


### And coding style tests


## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
