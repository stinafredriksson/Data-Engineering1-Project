#!/bin/bash
# Update system
sudo apt-get update
sudo apt-get -y upgrade

# Set hostname
NEW_HOSTNAME="worker6"
sudo sed -i "1s/.*/$NEW_HOSTNAME/" /etc/hostname
sudo hostnamectl set-hostname --static "$NEW_HOSTNAME"

# Set upp ssh to master
MASTER_HOSTNAME=master
MASTER_IP=192.168.2.224

for i in {1..1}; do echo "$MASTER_IP $MASTER_HOSTNAME"| sudo tee -a /etc/hosts; done

# Adding potential drivers
sudo bash -c 'for i in {1..255}; do echo "192.168.2.$i host-192-168-2-$i-de1" >> /etc/hosts; done'

# Creating config
FILE_NAME="config"
FILE_CONTENT="
host master
        HostName master
        Port 22
        IdentityFile ~/.ssh/DE_12.pem
        User ubuntu"

# Create the file and add content
echo "$FILE_CONTENT" >> .ssh/"$FILE_NAME"

cd ~
# Install Java (required for Hadoop and Spark)
sudo apt-get install -y openjdk-8-jdk

# Set Java environment variables
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre" >> ~/.bashrc
source ~/.bashrc

# Download Hadoop
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
# Unpack Hadoop and rename it
tar -xf hadoop-3.3.6.tar.gz
mv hadoop-3.3.6 hadoop

# Download Spark
wget https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
tar -xf spark-3.5.1-bin-hadoop3.tgz
mv spark-3.5.1-bin-hadoop3 /usr/local/spark

# Set Hadoop environment variables
export HADOOP_HOME=/home/ubuntu/hadoop
export PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin
export PATH=$PATH:/usr/local/spark/bin
echo "export HADOOP_HOME=/home/ubuntu/hadoop" >> ~/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/bin" >> ~/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/sbin" >> ~/.bashrc
echo "export PATH=$PATH:/usr/local/spark/bin" >>~/.bashrc
source ~/.bashrc

# Clean up downloaded tar files
cd ~
rm hadoop-3.2.2.tar.gz
rm spark-3.1.2-bin-hadoop3.2.tgz

# Move from master config files of hadoop

PATH_SSH_KEY=~/.ssh/DE_12.pem
PATH_CONFIG_FILE=/home/ubuntu/hadoop/etc/hadoop
LOCAL_PATH=/home/ubuntu/hadoop/etc/hadoop
scp -i "$PATH_SSH_KEY" "$MASTER_HOSTNAME:$PATH_CONFIG_FILE/*" "$LOCAL_PATH/"

## new code edits

sudo mv spark-3.5.1-bin-hadoop3 /usr/local/spark

# Set Hadoop environment variables
export HADOOP_HOME=/home/ubuntu/hadoop
export PATH=${PATH}:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin
export PATH=$PATH:/usr/local/spark/bin
echo "export HADOOP_HOME=/home/ubuntu/hadoop" >> ~/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/bin" >> ~/.bashrc
echo "export PATH=$PATH:$HADOOP_HOME/sbin" >> ~/.bashrc
echo "export PATH=$PATH:/usr/local/spark/bin" >>~/.bashrc
source ~/.bashrc

# Clean up downloaded tar files
cd ~
rm hadoop-3.3.6.tar.gz
rm spark-3.5.1-bin-hadoop3.tgz

PATH_SSH_KEY=~/.ssh/DE_12.pem
PATH_CONFIG_FILE=/home/ubuntu/hadoop/etc/hadoop
LOCAL_PATH=/home/ubuntu/hadoop/etc/hadoop
MASTER_HOSTNAME=master
scp -r -i "$PATH_SSH_KEY" "$MASTER_HOSTNAME:$PATH_CONFIG_FILE" "$LOCAL_PATH/"
