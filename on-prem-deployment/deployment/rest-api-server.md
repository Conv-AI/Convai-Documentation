---
description: Aka the Middleman
---

# REST API Server

The REST API Server handles all Rest API calls with the DB associated with creating and configuring a character and its resources.

#### Image:

```
convaitech/rest-api-server:v0.3.2
```

#### Container Deployment:

Run the following docker command to start the server:

```
$ sudo docker run   --name convai-api \
-p 8000:8000 \
-v "/home/convai/db-setup/admin-users.json:/app/admin-users.json"  \
-e DATABASE_URL="postgresql+asyncpg://convai_user:<password>@convai_postgres:5432/convai_db"  \
-e REDIS_URL="redis://convai_redis:6379" \
-e HOST="0.0.0.0"  \
-e PORT="8000"  \
convaitech/rest-api-server:v0.3.2
```
