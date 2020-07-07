import json


def hello(event, context):

    response = {
        "statusCode": 200,
        "body": "hello"
    }

    return response


def welcome(event, context):
  
    response = {
        "statusCode": 200,
        "body": "welcome"
    }

    return response
