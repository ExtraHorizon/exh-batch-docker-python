# Batch docker image python example

This is a template for a docker-based batch job on the Extra Horizon platform. It fetches the user linked to the credentials provided to the batch job, to showcase communication with the platform.

However, there are a few steps that need to be done in order to achieve this result:

1. Build your docker image
2. Authenticate yourself to the registry
3. Push the docker image to the registry

Before starting, Extra Horizon will need to provide you with the following:
* Docker registry URL (`registry-url`) where you can push your docker images
* AWS credentials (`AWS Access Key Id` and `AWS Secret Access Key`) to authenticate yourself to the registry.

## 🛠️ Building the docker image

You can build the example docker image as follows:

```sh
docker build -t <registry-url>:<your-tag> .
```

## 🔐 Authenticate yourself to the registry

You need to authenticate yourself to the docker registry in order to push images to it. Normally you should only do this once or when your credentials expire. For this, you will need the AWS client `aws`. See [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) for instructions on how to install this client.

After installing, use `aws configure` to set the `AWS Access Key Id` and `AWS Secret Access Key` credentials you should've received from Extra Horizon. See [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html) for more details.  

Once `aws` is set up correctly, use it to authenticate against the docker registry. This is explained [here](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html), but the easiest is probably to do

```sh
aws ecr get-login-password --region region | docker login --username AWS --password-stdin <registry-url>
```

## 🚚 Sending the docker image to the register

If the registry is authenticated, you need to:

```sh
docker push <registry-url>:<your-tag>
```

Remember to replace `<your-tag>` by whatever tag you chose in the build process

## ⚙️ Running the batch job

Extra Horizon will have setup a function in the Task Service for you to run (mentioned as `<your function name>`). You can run this function using the following snippet:

```py
# Assuming you've installed requests_oauthlib via pip: `pip install requests_oauthlib`
from requests_oauthlib import OAuth1Session

oAuth1Client = OAuth1Session(
    client_key='<your Extra Horizon consumer key>',
    client_secret='<your Extra Horizon consumer secret>',
    resource_owner_key='<your Extra Horizon access token>',
    resource_owner_secret='<your Extra Horizon token secret>'
)

# Normally the development URL will how the form of something like: api.dev.xxx
result = oAuth1Client.post(
  'https://<your development url>/tasks/v1/functions/<your function name>/execute', 
  json={
        "data":{
            "schemaId": "<your schema id>",
            "documentId": "<your document id>",
        }
  }
)

print("Response", result.json())
```   

This will immediately start the batch job on the Extra Horizon platform and return a response. You can check the status of the batch job in the AWS Batch console. The logs of the batch job can be found in the AWS Batch console as well.
