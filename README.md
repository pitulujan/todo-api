# todo-api
Simple Flask API for playing around with tasks implementing JWT for authentication, Blueprints for error handling, Draft7Validator , different Databases, etc

### Comments
I decided to use JSON Web Tokens with Public Key Signatures, so if in the future we are gonna use microservices,and in order to avoid bottlenecks when verifying tokens, we can separate both the token generation from the token verification, giving us the ability to decode JWT in any service with access to the public key.

#### New on this branch
In this branch i added a MongoDb implementation. In order to connect and to execute queries against the database, you are going to use a library created and maintained by MongoDB itself called pymongo. Since you might want to use another database in the future, it is a good idea to decouple your application from MongoDB. For the sake of simplicity we are going to create an abstract class to represent a Repository, this class should be the one used throughout your application.

### Run it 

In order to run the application, first you should create a private-public key pair ``ssh-keygen -t rsa -b 4096 `` and paste it as shown below

```
.
├── todo-api
│   ├── api                  # Application logic lives here          
│   │   ├── __init__.py
│   │   ├── json_validators.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── services.py
│   │   ├── errors          # Errors blueprint
│   │   |    ├── __init__.py 
│   │   |    └──  api_errors.py
│   │   └── flassger        # Flasgger blueprint
│   │        ├── yml
│   │        |   └── swagger_config.yml             
│   │        ├── __init__.py 
│   │        └──  api_flasgger.py
│   ├── config
│   │    └── config.py
│   ├── enviroment
│   │    ├── req_deploy.txt
│   │    └── req_dev.txt
│   ├── hooks
│   │    └── pre-commit-config.yaml
│   ├── repos
│   │    ├── __init__.py
│   │    └── mongo.py
│   ├── tests
│   │    └── __init__.py
│   ├── jwt-key              # User should create it and paste it here 
|   ├── jwt-key.pub          # User should create it and paste it here
|   ├── .env                 # MONGO_URL = 'mongodb+srv://``user``:```pass```@cluster0.jqc5t.mongodb.net/``cluster``?retryWrites=true&w=majority'
|   ├── run.py
|   └── setup.cfg            # Configuration file for pre-commit hooks
```
Then simply create a virtual environment, install req_deploy.txt, run.py and navigate to http://localhost:5000/apidocs/#/!
