# logregDocker
A simple model built on the Iris data with Sci-Kit Learn Logistic Regression is ready to be deployed as a service using docker.

How to build and run the service:
1. Find the path to the logregDocker directory
2. Run the command below:
```
docker-compose build
```
3. Once build is complete without errors, run the command below:
```
docker-compose up
```
4. The terminal should show that a service is up and running (also, the IP to the service).

How to send a request to a service:
```
import requests
import json

data = {"data": [[1,3],[5,2],[8,3]]}

input_data = json.dumps(data)

resp = requests.post("http://localhost:5000/predict", input_data)

resp.json()
```
