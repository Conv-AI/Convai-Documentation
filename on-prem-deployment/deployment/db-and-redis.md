---
description: Setup the base Database and a Redis cache server
---

# DB and Redis

Setting up a Database and a Cache server is essential for the applications to run. We provide the initial scripts to run during a DB setup that prepare for the next set of applications to spin up. Furhter updates to the schema and the data are communicated directly to the team.

#### Repository

```
git clone https://github.com/Conv-AI/DB-Onprem-Setup
```

#### DB Docker Command

Run the following docker command to bring up the DB server

```
$ cd DB-Onprem-Setup/

$ sudo docker run -d   --name convai_postgres \
-p 0.0.0.0:5432:5432   -e POSTGRES_DB=convai_db \
-e POSTGRES_USER=convai_user \
-e POSTGRES_PASSWORD=<password> \
-e POSTGRES_INITDB_ARGS="--encoding=UTF8 --lc-collate=C --lc-ctype=C"  \
-v convai_db_data:/var/lib/postgresql/data  \
-v ./init-scripts:/docker-entrypoint-initdb.d  \
--health-cmd="pg_isready -U convai_user -d convai_db"  \
--health-interval=10s   --health-timeout=5s   --health-retries=5  \
--restart=unless-stopped \
postgres:15
```

#### Redis Docker Command \[Optional]

Run the following docker command to bring up a redis cache server in case you do not already have one configured.

```
$ sudo docker run -d   --name convai_redis \
-p 0.0.0.0:6379:6379   -v redis_data:/data  \
--health-cmd="redis-cli ping" \
--health-interval=10s   --health-timeout=5s   --health-retries=5  \
--restart=unless-stopped   \
redis:7-alpine   redis-server \
--appendonly yes
```
