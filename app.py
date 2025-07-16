from flask import Flask
import os
import boto3
import json

def get_secret(secret_name):
    try:
        # Create a Secrets Manager client
        client = boto3.client('secretsmanager', region_name='us-east-1')  # Change region if needed

        # Fetch the secret value
        response = client.get_secret_value(SecretId=secret_name)

        # Parse and return the secret
        return json.loads(response['SecretString'])['MY_AWS_SECRET_KEY']
    except Exception as e:
        return f"Error fetching AWS secret: {str(e)}"

app = Flask(__name__)

@app.route('/')
def hello():
    # Environment variables for app name and local secrets
    app_name = os.getenv('APP_NAME', 'HelloApp')
    secret_key = os.getenv('MY_SECRET', 'not_set')
    aws_secret = os.getenv('AWS_SECRET_FROM_MANAGER', 'aws_default')

    return f"Hello from {app_name}! Secret: {secret_key}, AWS Secret: {aws_secret}"

@app.route('/aws-secret')
def aws_secret():
    # Fetch secret from AWS Secrets Manager
    secret_name = os.getenv('AWS_SECRET_NAME', 'my-app-secrets')
    secret_value = get_secret(secret_name)
    return f"AWS Secret Value: {secret_value}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
