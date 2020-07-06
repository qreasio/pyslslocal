import os
import boto3
import json
import unittest

LAMBDA_ENDPOINT='http://localhost:3002'
REGION='us-east-1'
STATE_MACHINE_ARN='arn:aws:states:us-east-1:123456789:stateMachine:foo'

class TestStatus(unittest.TestCase):
    def setUp(self):
        cmd = 'serverless offline > /dev/null 2>&1 &'
        os.system(cmd)

    def tearDown(self):
        cmd = "ps aux  |  grep -i 'serverless offline'  |  awk '{print $2}'  |  xargs kill -9"
        os.system(cmd)

    def test_hello(self):
        client = boto3.client('lambda', endpoint_url=LAMBDA_ENDPOINT, region_name=REGION)
        response = client.invoke(
            FunctionName='theFirst',
            InvocationType = 'RequestResponse',
            Payload = "{}"
        )

        res_json = json.loads(response['Payload'].read().decode("utf-8"))
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(res_json['statusCode'], 200)

        response = client.invoke(
            FunctionName='theSecond',
            InvocationType = 'RequestResponse',
            Payload = "{}"
        )

        res_json = json.loads(response['Payload'].read().decode("utf-8"))
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(res_json['statusCode'], 200)


if __name__ == '__main__': 
    unittest.main() 