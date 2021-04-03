# Serverless API Service
Serverless generic API service using API Gateway, Lambda Functions and FastAPI framework...
___________________________________________________________________


### Create Python Virtual Environment
```batch
virtualenv --python=python3.8 .venv
source .venv/bin/activate
```

### Install dependencies
```batch
pip install -r requirements.txt
```

### Run project locally
```batch
uvicorn main:app --reload
python manage.py run
```

### Run project with Docker
```batch
docker build -t serverless-api-service .
docker run -p 8080:8080 \
  --env REGION=us-east-1 \
  --env ACTIVE_SERVICES=MockService,DynamoService \
  serverless-api-service
```

### Environment Variables
```batch
export AWS_SAM_STACK_NAME=serverless-api-service
export ACTIVE_SERVICES=MockService,DynamoService
export REGION=us-east-1
```

### Create a bucket
```
aws s3api create-bucket \
  --bucket serverless-api-service \
  --region us-east-1 \
  --acl private
```

### Deploy the application
AWS SAM provides you with a command line tool, the AWS SAM CLI (you need 
to install it), that makes it easy for you to create and manage 
serverless applications.
```batch
sam build
sam deploy --stack-name serverless-api-service --s3-bucket serverless-api-service --capabilities CAPABILITY_NAMED_IAM
```

### Insert some records in DynamoDB
```batch
aws dynamodb put-item --table-name users --item '{"id": {"S": "000-1"}, "full_name": {"S": "User X"}, "gender": {"S": "M"}}' --return-consumed-capacity TOTAL
aws dynamodb put-item --table-name users --item '{"id": {"S": "000-2"}, "full_name": {"S": "User Y"}, "gender": {"S": "F"}}' --return-consumed-capacity TOTAL
```
