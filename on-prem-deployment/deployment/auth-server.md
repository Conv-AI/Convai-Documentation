---
description: Setup Authentication Server with your organization SSO
---

# Auth Server

The Authentication Server is an important part of the Convai setup as it handles authentication of user and also validation across multiple subdomains of Convai services. It is essential to understand the exact requirement of the user's authentication service and create configuration files accordingly.

In the current setup, we assume a simple Authentication service from Firebase is being used.

#### Image:

{% hint style="info" %}
The final image link may vary depending on the client environment and the services being used. Please note that the link shared here is private and can only be accessed by members within the organization.
{% endhint %}

```
convaitech/convai-auth-onprem:v0.1.5
```

#### Environment Variable Setup

Create a .env file in your system. Lets assume a auth-server.env file exists at /var/secrets. Fill the file with the required configurations as specified by the team. Here is some sample data..

```
// auth-server.env
COOKIE_ENCRYPTION_KEY=random-token

# OPENID_CONNECT_KEY=5ar4f5jl9u...
# OPENID_CONNECT_SECRET=1rfu4nsa00ql91i33ieua...
# OPENID_CONNECT_DISCOVERY_URL=https://cognito-idp.us-west-1.amazonaws.com/us-wes.../.well-known/openid-configuration

COOKIE_DOMAIN=localhost
BASE_URL=http://localhost:8081
IS_ON_PREM=true
...
```

#### Container Deployment:

Run the following docker command to start the server:

```
$ sudo docker run -d \
--name auth-server -p 8081:8080 \
-v ~/Documents/secrets/auth-server-secrets.env:/app/secrets/secrets.env \
convaitech/convai-auth-onprem:v0.1.5
```

#### Sample Helm Config

Here we are attaching a sample helm chart to host the service.

```
# charts/auth-server/Chart.yaml
apiVersion: v2
name: convai-auth-server
version: 0.1.5
appVersion: "v0.1.5"
---
# charts/auth-server/values.yaml
replicaCount: 2
image:
  repository: <ECR_CLOUD>.dkr.ecr.us-west-1.amazonaws.com/convai-auth-onprem
  tag: v0.1.5
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8080
ingress:
  enabled: true
  ingressClassName: aws-alb
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internal
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws-us:acm:...
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS13-1-2-2021-06
  hosts:
    - host: auth.internal.agency.gov
      paths: [{ path: /, pathType: Prefix }]
env:
  COOKIE_DOMAIN: .internal.client
  BASE_URL: https://auth.internal.client
  IS_ON_PREM: "true"
existingSecret: convai-auth-secrets  # AWS Secrets Manager via ESO
resources:
  requests: { cpu: 250m, memory: 256Mi }
  limits:  { cpu: 500m, memory: 512Mi }
podDisruptionBudget:
  minAvailable: 1
networkPolicy:
  enabled: true
  ingress:
    - from: [{ namespaceSelector: { matchLabels: { name: convai } } }]
      ports: [{ port: 8080 }]
serviceAccount:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws-us:iam::<ACCOUNT>:role/convai-auth-role

```
