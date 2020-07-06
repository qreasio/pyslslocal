import os
import boto3
import json
import time
import unittest

LAMBDA_ENDPOINT = 'http://localhost:3000'
REGION = 'us-east-1'
STATE_MACHINE_ARN = 'arn:aws:states:us-east-1:123456789:stateMachine:foo'
SFN_ENDPOINT = 'http://localhost:4584'


class TestStatus(unittest.TestCase):
    def setUp(self):
        cmd = 'serverless offline > /dev/null 2>&1 &'
        os.system(cmd)

    def tearDown(self):
        cmd = "ps aux  |  grep -i 'serverless offline'  |  awk '{print $2}'  |  xargs kill -9"
        os.system(cmd)

    def test_hello(self):
        client = boto3.client('lambda',
                              endpoint_url=LAMBDA_ENDPOINT,
                              region_name=REGION)
        response = client.invoke(FunctionName='theFirst',
                                 InvocationType='RequestResponse',
                                 Payload="{}")

        res_json = json.loads(response['Payload'].read().decode("utf-8"))
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(res_json['statusCode'], 200)

        sfn = boto3.client('stepfunctions',
                           region_name=REGION,
                           endpoint_url=SFN_ENDPOINT)

        sm_arn = 'arn:aws:states:us-east-1:123456789:stateMachine:foo'

        execution = sfn.start_execution(stateMachineArn=sm_arn)

        response = sfn.list_executions(stateMachineArn=sm_arn)

        status = sfn.describe_execution(executionArn=execution["executionArn"])

        time.sleep(5)

        history = sfn.get_execution_history(
            executionArn=execution["executionArn"], reverseOrder=True)
        print(history)


if __name__ == '__main__':
    unittest.main()
