# FILEPATH

"""
This folder contains the necessary files for deploying a socket server application.

- ss-deployment.yaml: Defines the deployment configuration for the socket server.
- ss-service.yaml: Defines the service configuration for the socket server.
- ss-ingress.yaml: Defines the ingress configuration for the socket server.
- Dockerfile: Specifies the instructions for building the Docker image of the socket server.
- socketServer.py: The main Python file that implements the socket server functionality.

Please refer to the individual files for more detailed information on their contents and usage.
"""


Forward the port of the socket server to the local machine:
```shell
kubectl port-forward service/socket 5001:5001
```