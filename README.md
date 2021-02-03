# logregDocker
A simple model built on the Iris data with Sci-Kit Learn Logistic Regression is ready to be deployed as a service using docker.

How to send a request to a service:
```
import requests
import json

data = {"data": [[1,3],[5,2],[8,3]]}

input_data = json.dumps(data)

resp = requests.post("http://localhost:5000/predict", input_data)

resp.json()
```
