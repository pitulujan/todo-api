# todo-api
Simple Flask API for playing around with tasks implementing JWT for authentication, Blueprints for error handling, Draft7Validator , etc

### Comments
I decided to use JSON Web Tokens with Public Key Signatures, so if in the future we are gonna use microservices,and in order to avoid bottlenecks when verifying tokens, we can separate both the token generation from the token verification, giving us the ability to decode JWT in any service with access to the public key.
