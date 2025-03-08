import docker
import requests
import time
import psutil
import datetime

# CHANGE ME!
# Address needs protocol and '/' at the end. Unsecure string operations ahead!
obsserveraddress = "http://192.168.0.232:8080/"

client = docker.from_env()

while True:
    # Ask containers for their stuff
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

        r = requests.post(obsserveraddress + "container", json=j)

    # Ask OS for it's stuff
    cpu_perc = psutil.cpu_percent()
    
    ram = psutil.virtual_memory()
    rambytes = ram.used
    maxrambytes = ram.total
    
    swap = psutil.swap_memory()
    swapbytes = swap.used
    maxswapbytes = swap.total

    now = datetime.datetime.now(datetime.UTC)
    nanoseconds = f"{time.time_ns() % 1_000_000_000:09d}"
    timestamp = now.strftime(f"%Y-%m-%dT%H:%M:%S.{nanoseconds}Z")

    j = {"timestamp": timestamp, "cpupercent": cpu_perc, "rambytes": rambytes, "maxrambytes": maxrambytes, "swapbytes": swapbytes, "maxswapbytes": maxswapbytes}
    print(j)

    r = requests.post(obsserveraddress + "host", json=j)

    time.sleep(5)

