#!/bin/bash

# Update apt repo metadata
sudo apt update

# Install Java (version up to you, but must be >= 8)
sudo apt-get install -y openjdk-17-jdk

# Manually define a hostname for all the hosts on the de1 project. 
# This will ensure connections of Spark between different instances:
for i in {1..255}; do echo "192.168.1.$i host-192-168-1-$i-de1"| sudo tee -a /etc/hosts; done
for i in {1..255}; do echo "192.168.2.$i host-192-168-2-$i-de1"| sudo tee -a /etc/hosts; done

# Set the hostname according to the scheme above and retrieve it
new_hostname=$(sudo hostname host-$(hostname -I | awk '{$1=$1};1' | sed 's/\./-/'g)-de1 ; hostname)

# Set the hostname to /etc/hostname file
echo "$new_hostname" | sudo tee /etc/hostname

# Inform user to edit the hostname if needed
echo "Hostname has been set to $new_hostname. If needed, you can edit it manually using 'sudo nano /etc/hostname'."

