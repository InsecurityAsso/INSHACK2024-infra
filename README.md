# Infrastructure Ins'Hack 2024

## Deploying development server
1. Create a virtual environement and source it (optional) 
```bash
python3 -m venv venv

# source venv on linux/OSX
source venv/bin/activate

# source venv on windows
venv\Scripts\activate.bat
```
2. Run the server
```bash
python3 test_server.py
```

## Project Roadmap
### 1. Web interface
#### 1.1. Frontend
- [not started] Home page
- [not started] Login page
- [not started] Register page
- [not started] Profile page
- [not started] Challenges page
- [not started] Scoreboard page
- [not started] users verification
- [not started] users authentication
- [not started] users password reset
- [not started] teams management
#### 1.2. Backend
- [done] users mail check
- [done] users password check
- [done] email user after verification
- [done] user personnal space
- [implemented] account deletion - requires further testing
- [in progress] password reset - logic is done, implementation is been worked on
- [not started] teams management
- [not started] API to interact with other components (VPN, Nginx, docker, ...)
- [not started] Implement defense against bruteforce attacks (with django-ratelimit most likely)
### 2. Network  infrastructure
#### 2.1. Docker
- [not started] Dockerfile for web interface
- [not started] Dockerfile for VPN
- [not started] docker-compose.yml file for whole infrastructure
#### 2.2. VPN
- [not started] VPN server conf
- [not started] VPN client conf
#### 2.3. Nginx
- [not started] Nginx conf
### 3. Challenges
#### 3.1. Challenges creation
- [not started] Create challenges
- [not started] Create challenges categories
- [not started] Create challenges levels
- [not started] Create challenges hints
- [not started] Create challenges flags
- [not started] Create challenges dockerfiles

#### 3.2. Challenges deployment
- [not started] Create docker subnet for each team


## Networking CheatSheet
#### Create a bridge interface on host
```bash
# create a bridge on host
sudo brctl addbr br0

# add host interface to bridge
sudo brctl addif br0 eth0
```
#### Expose a container or a VM on subdomain using nginx
1. Add an host record
```bash
echo "target_ip sub.domain.com" >> /etc/hosts
```
2. Create sub.domain.com.conf
```bash
touch /etc/nginx/sites-enabled/sub.domain.com.conf
```
3. Content of subdomain.conf
```bash
# stream all traffic to VM or container
stream {
    upstream VM {
        server 192.168.1.10:1-65535;
    }

    server {
        listen sub.domain.com:1-65535; 
        proxy_pass VM;
    }
}
```
4. Apply changes
```bash
sudo service nginx reload
```
#### Remove a VM or a container
1. Stop the VM or container
```bash
docker stop container_name
# or 
vmrun stop /path/to/vm.vmx nogui
```
2. Remove the VM file if needed
```bash
rm /path/to/vm.vmx
```
3. Delete host record
```bash
sed -i '/target_ip sub.domain.com/d' /etc/hosts
```
4. Delete nginx config file
```bash
rm /etc/nginx/sites-enabled/sub.domain.com.conf
```
5. Apply changes
```bash
sudo service nginx reload
```
## VM Ware (cli) CheatSheet
#### VMs Management
```bash
# Start VM
vmrun start /path/to/vm.vmx nogui

# Stop VM
vmrun stop /path/to/vm.vmx nogui

# get vm ip
vmrun getGuestIPAddress /path/to/vm.vmx

# get vm state
vmrun list | grep /path/to/vm.vmx
```
#### Configure VMWare to use the bridge interface:
1. Stop VMWare Network Service: 
```bash	
sudo service vmware-networks stop
```
2. Edit `/etc/vmware/networking` and add the following lines:
```bash
add bridge0
bridge0.name = "vmnet0"
bridge0.standalone = "yes"
bridge0.guestNetmask = "255.255.255.0"
bridge0.hostIP = "host_local_ip"
bridge0.virtualDev = "vmxnet3"
```
3. configure the VM to use the bridge interface:
3.1 Open the VMX file of the VM
```bash
sudo nano /path/to/vm.vmx
```
3.2 Add the following lines:
```bash
ethernet0.connectionType = "bridged"
ethernet0.vnet = "vmnet0"
# set ip address
ethernet0.addressType = "static"
ethernet0.address = "vm_ip"
```
4. Start VMWare Network Service:
```bash
sudo service vmware-networks start
```
### Docker CheatSheet
#### Dockerfile
```dockerfile
FROM base-image:latest #ex: ubuntu:latest

# install dependencies
RUN apt-get update && apt-get install -y \
    dep1 \
    dep2 \
    dep3

# copy files
COPY . /path/to/destination

# set working directory
WORKDIR /path/to/working/directory

# run commands
RUN command1
RUN command2

# expose ports
EXPOSE 80
EXPOSE 443

# set entrypoint
ENTRYPOINT ["command1", "command2"]
```
#### Build image from dockerfile and docker-compose.yml
```bash
docker-compose build
```
#### Run container from image
```bash
docker run -d \
--name container_name image_name \
 -p host_port:container_port # can be used multiple times
```

# credits (to add to a footer or something) 
- [flaticon](https://www.flaticon.com/)
- [pixabay](https://pixabay.com/)
