# Counter Service home assignment

The home assignment contains: 

1) A Python FastAPI ws
    * POST requests to increment a counter
    * GET requests to return the counter
2) A Redis image, containting the count, so even if ws is restarted or deleted the count persists.
 
3) A Jenkins with SSL enabled installation with a ci-cd pipeline, that receives branch name, builds the branch and deploy it into the e2c server
    * The pipeline can be triggered manually with BRANCH_NAME param
    * On commit and push of the git repo the webhook triggers the build, and the branch name is parsed from the github webhook payload.

## prerequisite
* To access the jenkins site using https, the self signed certificate must be installed. It will be sent seperatly

## Usage

To access the Jenkins pipeline:
```bash
https://{E2C_HOSTNAME}:443/job/deploy-branch/
```

Counter Service requests snippets:
```bash
curl --location --request GET "http://{E2C_HOSTNAME}:80"
Response:
{"counter": 2}

curl --location --request POST "http://{E2C_HOSTNAME}:80"
Response:
{"message": "Counter incremented"}
```
