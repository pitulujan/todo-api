# todo-api
Simple Flask API for playing around with tasks implementing JWT for authentication, Blueprints for error handling, Draft7Validator , etc

### Comments
I decided to use JSON Web Tokens with Public Key Signatures, so if in the future we are gonna use microservices,and in order to avoid bottlenecks when verifying tokens, we can separate both the token generation from the token verification, giving us the ability to decode JWT in any service with access to the public key.

Each branch is gonna be leveraging on the preovious one, adding features and complexity. Master is the basic start off point.

### Run it 

In order to run the application, first you should create a private-public key pair ``ssh-keygen -t rsa -b 4096 `` and paste it as shown below

```
.
├── todo-api
│   ├── api                    # Application logic lives here          
│   │   ├── __init__.py
│   │   ├── json_validators.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── errors             
│   │       ├── __init__.py 
│   │       └──  api_errors.py
│   ├── jwt-key                # User should create it and paste it here 
|   ├── jwt-key.pub            # User should create it and paste it here
|   ├── requirements.txt
|   └── run.py
```

Then simply create a virtual environment, install requirements.txt and run.py!
