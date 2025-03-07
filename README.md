# envobs
Docker-based developement/test environments observer (Grafana+PostgreSQL+Python3)

> Under development and ONLY for development/test environments. If you want/need to run this in production, you have bigger problems. 

## Use-case
Observe VM's with Docker containers to measure CPU/RAM usage.

## How-to
You'll need two VM's. One for `envobs`, one for your project.

 - Copy `envobserveragent.py` to your project VM, change server address at the beginning of the script. Run the script in background.
 - On `envobs` VM run `docker-compose up -d` in this projects directory. After a while, you'll find Grafana UI on port 3000. Default login/pass is `admin/admin`.
 - In Grafana go to Dashboards -> Environment Observer.

That's all.

## TODO
 - Host CPU usage
 - Sum of containers RAM usage
 - Host RAM+SWAP+SUM usage
 - Disk IO usage per container
 - Network IO usage per container
 - Dependency-less agent code

