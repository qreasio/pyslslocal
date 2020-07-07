import os
import boto3
import json
import time
import unittest

LAMBDA_ENDPOINT = 'http://localhost:3002'
REGION = 'us-east-1'
SFN_ENDPOINT = 'http://localhost:8083'
ACCOUNT_ID = '123456789012'

class TestStepFunctions(unittest.TestCase):
    def setUp(self):
        cmd = 'serverless offline start > /dev/null 2>&1 &'
        os.system(cmd)

    def tearDown(self):
        cmd = "ps aux  |  grep -i 'serverless offline'  |  awk '{print $2}'  |  xargs kill -9"
        os.system(cmd)
        cmd = "ps aux  |  grep -i 'StepFunctionsLocal.jar'  |  awk '{print $2}'  |  xargs kill -9"
        os.system(cmd)

    def test_hello(self):
        time.sleep(10)
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
        
        STATE_MACHINE_ARN = "arn:aws:states:us-east-1:%s:stateMachine:foo" % ACCOUNT_ID

        execution = sfn.start_execution(stateMachineArn=STATE_MACHINE_ARN,
        input='{"name":"James Bond"}')

        print(execution)
        print("=================")

        response = sfn.list_executions(stateMachineArn=STATE_MACHINE_ARN)
        
        status = sfn.describe_execution(executionArn=execution["executionArn"])
        print(status)
        print("=================")

        time.sleep(5)

        history = sfn.get_execution_history(
            executionArn=execution["executionArn"], reverseOrder=True)
        print(history)


if __name__ == '__main__':
    unittest.main()
