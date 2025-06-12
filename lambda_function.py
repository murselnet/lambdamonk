import sys
sys.path.insert(0, 'paketler')





from mangum import Mangum
from main import app  # main.py dosyasındaki FastAPI/Flask 'app' nesnesini import ediyoruz

handler = Mangum(app)



"""
import requests

def lambda_handler(event, context):
    response = requests.get("https://api.github.com")
    return {
        "statusCode": 200,
        "body": response.json()
    }
"""



"""
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda! From MRS MURSEL GitHub Actions!')
    }
"""
