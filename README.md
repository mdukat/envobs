# envobs
Docker-based developement/test environments observer (Grafana+PostgreSQL+Python3)

> Under development and ONLY for development/test environments. If you want/need to run this in production, you have bigger problems. 

## Use-case
Observe VM's with Docker containers to measure CPU/RAM usage in real time.

## How-to
You'll need two VM's. One for `envobs`, one for your project.

 - Make sure that port 8080 on `envobs` VM is accessible from your "environment" VM, and that you have installed dependencies (see "Agent requirements").
 - Copy `envobserveragent.py` to your environment VM, change server address at the beginning of the script to `envobs` VM address. Run the script in background (for example using tmux or screen).
 - On `envobs` VM run `docker-compose up -d` in this projects directory. After a while, you'll find Grafana UI on port 3000. Default login/pass is `admin/admin`.
 - In Grafana go to Dashboards -> Services -> Environment Observer.

That's all.

## Clean-up process
Database is not being cleared! It will get bigger and bigger if agent will be running non-stop.

To clean the `envobs` VM, stop compose and clean volumes:
```
$ docker-compose down
$ docker volume rm envobs_grafana_data envobs_postgres_data
```

## Agent requirements
Current agent script needs:
 - Python 3
 - python3-docker package
 - python3-psutil package

On Ubuntu, you can install these dependencies with:
```
$ sudo apt install python3 python3-docker python3-psutil
```

## TODO
 - Sum of containers RAM usage
 - Disk IO usage per container
 - Network IO usage per container
 - Dependency-less agent code

