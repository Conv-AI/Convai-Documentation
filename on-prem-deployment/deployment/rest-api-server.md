---
description: Aka the Middleman
---

# REST API Server

The REST API Server handles all Rest API calls with the DB associated with creating and configuring a character and its resources.

#### Image:

{% hint style="info" %}
The final image link may vary depending on the client environment and the services being used. Please note that the link shared here is private and can only be accessed by members within the organization.
{% endhint %}

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

#### Sample Helm Config

Here we are attaching a sample helm chart to host the service.

```
# charts/rest-api/values.yaml
replicaCount: 2
image:
  repository: <ECR_CLOUD>.dkr.ecr.us-west-1.amazonaws.com/convai-rest-api-server
  tag: v0.3.2
service:
  type: ClusterIP
  port: 8000
ingress:
  enabled: true
  ingressClassName: aws-alb
  annotations:
    alb.ingress.kubernetes.io/scheme: internal
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
  hosts:
    - host: api.internal.client
      paths: [{ path: /, pathType: Prefix }]
env:
  HOST: "0.0.0.0"
  PORT: "8000"
  DATABASE_URL:
    valueFrom:
      secretKeyRef: { name: convai-rest-api-secrets, key: database-url }
  REDIS_URL:
    valueFrom:
      secretKeyRef: { name: convai-rest-api-secrets, key: redis-url }
volumes:
  - name: admin-users
    configMap: { name: convai-admin-users }
volumeMounts:
  - name: admin-users
    mountPath: /app/admin-users.json
    subPath: admin-users.json
livenessProbe:
  httpGet: { path: /health, port: 8000 }
  initialDelaySeconds: 30
readinessProbe:
  httpGet: { path: /ready, port: 8000 }
  initialDelaySeconds: 15
hpa:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
podDisruptionBudget:
  minAvailable: 1

```
