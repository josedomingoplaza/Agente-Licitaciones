# Agente-Licitaciones

# Instrucciones para correr el filtro de licitaciones

Primero correr:

```
docker-compose up -d etcd minio milvus
/bin/sh -c 'until curl -sf http://localhost:9091/healthz; do echo waiting; sleep 2; done; echo milvus is healthy'
```

Luego:

```
docker-compose build agente-licitaciones
```

Finalmente:

```
docker-compose run --service-ports --rm -it agente-licitaciones python -m licitation_filter.scripts.01_run_discovery
```