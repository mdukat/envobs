import docker
import requests
import time

# CHANGE ME!
obsserveraddress = 'http://192.168.0.232:8080/'

client = docker.from_env()

while True:
    containers = client.containers.list()

    for container in containers:
        stats = container.stats(decode=False, stream=False)

        # https://stackoverflow.com/a/77924494
        cpu_usage = (stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage'])
        cpu_system = (stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage'])
        num_cpus = stats['cpu_stats']["online_cpus"]
        cpu_perc = (cpu_usage / cpu_system) * num_cpus * 100

        j = {"timestamp": stats['read'], "containername": stats['name'], "cpupercent": cpu_perc, "rambytes": stats['memory_stats']['usage']}
        print(j)

        r = requests.post(obsserveraddress, json=j)

        time.sleep(5)

