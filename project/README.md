# otus_software_architect
Software architect course, final project

# Description

## Pull monitoring
The project uses submodule https://github.com/stefanprodan/dockprom for monitoring, so you need to fetch submodule:
```shell
./repo_upd.sh
```

## Copy prometheus.yml

```shell
cp prometheus.yml monitoring/prometheus/prometheus.yml
```

## Start the project
```shell
ADMIN_USER=admin ADMIN_PASSWORD=admin docker-compose -f monitoring/docker-compose.yml -f services/docker-compose.monitoring.yml up -d
```

## Prometheus url
```shell
http://localhost:9090/
```

## Grafana url
```shell
http://localhost:3000/
```

## Services url
```shell
http://localhost/
```
