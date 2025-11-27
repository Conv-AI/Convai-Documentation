---
description: Setup Authentication Server with your organization SSO
---

# Auth Server

The Authentication Server is an important part of the Convai setup as it handles authentication of user and also validation across multiple subdomains of Convai services. It is essential to understand the exact requirement of the user's authentication service and create configuration files accordingly.

In the current setup, we assume a simple Authentication service from Firebase is being used.

#### Image:

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
