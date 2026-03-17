---
description: Setup Convai Playground
---

# Convai Playground

Convai Playground provides an interactive UI to create, modify and test out your characters before they are released to your end-users.&#x20;

#### Image:

{% hint style="info" %}
The final image link may vary depending on the client environment and the services being used. Please note that the link shared here is private and can only be accessed by members within the organization.
{% endhint %}

```
convaitech/convai-playground-onprem-mp:v0.1.6
```

#### Environment Variable Setup

Create a .env file in your system. Lets assume a playground.env file exists at /var/secrets. Fill the file with the required configurations as specified by the team. Here is some sample data..

```
// playground.env
IS_ON_PREM=true
API_URL=http://localhsot:8000
BASE_URL=http://localhost:3000
REALTIME_API_URL=http://localhost:8002
DOMAIN_LINK=localhsot
# CONVAI_SECRET=dXv4+D...

LOGIN_URL=http://localhost:8081
...
```

#### Config Setup

The playground requires a JSON based config files that helps determing the services to expose to developer. The final list is based on the requirements specifed and can be extended based on growing requirements. Here is a sample config file data...

```
// playground-config.json
{
	"CHARACTER_DASHBOARD": {
		"DESCRIPTION": {
			"SPEAKING_STYLE": true
		},
		"LANGUAGE_AND_SPEECH": {
			"LANGUAGE": {
				"VIEW": true
			}
		},
		"CHATBOT": {
			"GET_RESPONSE_GRPC": true,
			"GET_RESPONSE_SSE": true
		},
		"STATE_OF_MIND": true,
		"EMBODIED_ACTIONS": true,
		"MEMORY": {
			"RECENT_MEMORY": true,
			"FILTERS_VIEW": true
		}
	},
	"EXPERIENCE_DASHBOARD": {
		"EMBED_EXPERIENCE": true,
		"DETAILS": true
	},
	"BILLING_PAGE": {
		"USAGE_SECTION": false
	}
}
```

#### Container Deployment:

Run the following docker command to start the server:

```
$ sudo docker run -d \
--name convai-playground-app   -p 3000:3000 \
-v "/var/secrets/playground-config.json:/app/config.json:ro"  \
--env-file "/var/secrets/playground.env" \
convaitech/convai-playground-onprem-mp:v0.1.6
```

#### Sample Helm Config

Here we are attaching a sample helm chart to host the service.

```
# charts/playground/values.yaml
replicaCount: 2
image:
  repository: <ECR_CLOUD>.dkr.ecr.us-west-1.amazonaws.com/convai-playground-onprem-mp
  tag: v0.1.6
service:
  type: ClusterIP
  port: 3000
ingress:
  enabled: true
  ingressClassName: aws-alb
  annotations:
    alb.ingress.kubernetes.io/scheme: internal
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/certificate-arn: arn:aws-us:acm:...
  hosts:
    - host: playground.internal.client
      paths: [{ path: /, pathType: Prefix }]
env:
  IS_ON_PREM: "true"
  API_URL: http://convai-rest-api.convai.svc.cluster.local:8000
  BASE_URL: https://playground.internal.agency.gov
  REALTIME_API_URL: http://convai-webrtc.convai.svc.cluster.local:8000
  LOGIN_URL: https://auth.internal.client
  DOMAIN_LINK: internal.client
existingSecret: convai-playground-secrets
configMap:
  enabled: true
  mountPath: /app/config.json
  subPath: config.json
  data: |
    { "CHARACTER_DASHBOARD": { "CHATBOT": { "GET_RESPONSE_GRPC": true } } }
resources:
  requests: { cpu: 200m, memory: 256Mi }
  limits:  { cpu: 500m, memory: 512Mi }
podDisruptionBudget:
  minAvailable: 1

```
