from flask import Flask, abort, request
import os
import boto3
import json
import logging

def get_secret(secret_name):
    try:
        # Create a Secrets Manager client
        region = os.getenv('AWS_REGION', 'us-east-1')
        client = boto3.client('secretsmanager', region_name=region)

        # Fetch the secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Parse and return the secret
        return json.loads(response['SecretString'])['MY_AWS_SECRET_KEY']
    except Exception as e:
        logging.exception("Error fetching AWS secret")
        return None

app = Flask(__name__)

def require_api_key():
    expected_key = os.getenv('AWS_SECRET_API_KEY')
    if not expected_key:
        abort(503, description="Secret access is not configured")
    provided_key = request.headers.get('X-API-Key')
    if provided_key != expected_key:
        abort(401, description="Unauthorized")

@app.route('/version')
def version():
    return {"version": "1.0.1"}

@app.route('/')
def hello():
    # Environment variables for app name and local secrets
    app_name = os.getenv('APP_NAME', 'HelloApp')

    return f"Hello from {app_name}!"

@app.route('/aws-secret')
def aws_secret():
    # Fetch secret from AWS Secrets Manager
    require_api_key()
    secret_name = os.getenv('AWS_SECRET_NAME', 'my-app-secrets')
    secret_value = get_secret(secret_name)
    if secret_value is None:
        abort(502, description="Unable to retrieve secret")
    return {"secret_name": secret_name, "status": "retrieved"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
