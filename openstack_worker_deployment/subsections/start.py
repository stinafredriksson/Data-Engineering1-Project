#!/usr/bin/python3
# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys,  random
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.v2_0 import client as neutron_client
import random
import re

flavor = "ssc.tiny" 
private_net = "UPPMAX 2024/1-1 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "da0d8cf7-a0eb-41ce-8db0-dd0d056b821d"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
neutron = neutron_client.Client(session=sess)
print ("user authorization completed.")

def is_ip_available(ip_address, network_id):
    """Check if the given IP address is available in the specified network."""
    # List all ports in the network
    ports = neutron.list_ports(network_id=network_id)['ports']
    # Check each port to see if the IP address is already in use
    for port in ports:
        for fixed_ip in port['fixed_ips']:
            if fixed_ip['ip_address'] == ip_address:
                return False
    return True

def generate_local_ip(network_id):
    """Generate an available local IP address within the specified network."""
    while True:
        #third_octet = random.randint(0, 255)
        fourth_octet = random.randint(1, 254)  # Avoiding 0 and 255
        ip_address = f"192.168.2.{fourth_octet}"
        if is_ip_available(ip_address, network_id):
            return ip_address
        else:
            print(f"IP {ip_address} is in use, generating a new one...")

def extractLastNumber(s):
    # Regular expression pattern to match the last number in the string
    pattern = r'\d+$'
    match = re.search(pattern, s)
    if match:
        return int(match.group())
    else:
        return None
    

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

instances = nova.servers.list()

# Fetch all instances
numbersInUse = []
# Print the names of all instances
# print("List of available instances:")
for instance in instances:
    name = instance.name
    if "DE_12_worker" in name:
        # print(name)
        number = extractLastNumber(name)
        # print("Number is: " + str(number))
        numbersInUse.append(int(number))

for i in range(max(numbersInUse)+1):
    if i+1 not in numbersInUse:
        workerName = "DE_12_worker" + str(i+1)
        break

if private_net != None:
    net = nova.neutron.find_network(private_net)
    random_local_ip = generate_local_ip(net.id)
    nics = [{'net-id': net.id, 'v4-fixed-ip': random_local_ip}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['default','Spark', 'Erik_Dahlin']

instance = nova.servers.create(name=workerName, image=image, flavor=flavor, key_name='DE_12', userdata=userdata, nics=nics, security_groups=secgroups)

# incase you want to login to the production server 
#instance = nova.servers.create(name="prod_server_without_docker", image=image, flavor=flavor, key_name='access-key-name',userdata=userdata, nics=nics,security_groups=secgroups)
inst_status = instance.status
print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status == 'BUILD':
    print ("Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print ("Instance: "+ instance.name +" is in " + inst_status + "state")
