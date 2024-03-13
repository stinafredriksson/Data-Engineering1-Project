#!/usr/bin/python3
import os
import sys
import time
from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session

# Define the instance name to remove
instance_name_to_delete = "DE_12_worker7863"

# Authentication setup
loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=os.environ['OS_AUTH_URL'],
                                username=os.environ['OS_USERNAME'],
                                password=os.environ['OS_PASSWORD'],
                                project_name=os.environ['OS_PROJECT_NAME'],
                                project_domain_id=os.environ['OS_PROJECT_DOMAIN_ID'],
                                user_domain_name=os.environ['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("User authorization completed.")

# Find the instance
instances = nova.servers.list(search_opts={'name': instance_name_to_delete})
if instances:
    instance = instances[0]  # Take the first match
    print(f"Found instance with name '{instance_name_to_delete}' to delete.")
    
    # Delete the instance
    nova.servers.delete(instance.id)
    print(f"Instance '{instance_name_to_delete}' deletion initiated.")
    
    # Wait and check for deletion
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try to get the instance again
            instance = nova.servers.get(instance.id)
            print(f"Waiting for instance '{instance_name_to_delete}' to be deleted. Status: {instance.status}")
            time.sleep(5)
        except:
            # If the instance is not found, it means deletion was successful
            print(f"Instance '{instance_name_to_delete}' successfully deleted.")
            break
else:
    sys.exit(f"No instances found with the name '{instance_name_to_delete}'.")


