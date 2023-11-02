# Cisco Cyber Vision Flow Exporter
This prototype allows you to export Cyber Vision flows to an external PostgreSQL database. This way, you can limit the amount of flows to be stored on the Cyber Vision appliance and ensure high performance.

![](/IMAGES/workflow.png)

## Contacts
* Stien Vanderhallen (stienvan@cisco.com)

## Solution Components
* Cyber Vision
* Cyber Vision REST API
* Docker

## Installation/Configuration

1. Clone this project

```
$ git clone https://github.com/Stienvdh/cybervision_flow_export.git
```

2. Navigate to the frontend project

```
$ cd frontend
```

3. Fill out the appropriate parameters in `.env`

4. Build and run the frontend container

```
$ docker build . -t cybervision-flow-front
$ docker run -p 8888:8888 cybervision-flow-front
```

5. Navigate to the backend project

```
$ cd ../backend
```

6. Fill out the appropriate parameters in `.env`

7. Build and run the backend container

```
$ docker build . -t cybervision-flow-back
$ docker run cybervision-flow-back
```

## Usage
To access the app, navigate to localhost:8888 in your local browser.


# Workflow

![](/IMAGES/usage.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
