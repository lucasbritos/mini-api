# lambda_handler.py
import json
from app import app
from serverless_wsgi import handle_request

def lambda_handler(event, context):
    print("Received event:", event)

    response = handle_request(app, event, context)

    return response