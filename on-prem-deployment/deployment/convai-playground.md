---
description: Setup Convai Playground
---

# Convai Playground

Convai Playground provides an interactive UI to create, modify and test out your characters before they are released to your end-users.&#x20;

#### Image:

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
