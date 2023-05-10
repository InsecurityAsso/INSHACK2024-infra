# Infrastructure Ins'Hack 2024
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