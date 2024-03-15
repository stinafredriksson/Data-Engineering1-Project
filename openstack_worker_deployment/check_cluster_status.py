import requests

# Replace with your Spark master's web UI address and port
spark_master_web_ui = 'http://130.238.28.228:8080'

response = requests.get(f"{spark_master_web_ui}/json/")
cluster_info = response.json()

print(f"cores: {cluster_info['cores']}")
print(f"cores used: {cluster_info['coresused']}")