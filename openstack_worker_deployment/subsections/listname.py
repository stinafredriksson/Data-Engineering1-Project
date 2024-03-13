import os
from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session

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

# Fetch all instances
instances = nova.servers.list()

# Print the names of all instances
print("List of all instances:")
for instance in instances:
    print(instance.name)

