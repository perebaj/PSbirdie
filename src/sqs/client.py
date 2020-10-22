#!/usr/bin/python3
# -*- coding: utf-8 -
import boto3

# Create SQS client
sqs = boto3.client('sqs')


def send_message(message, queue_url):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=1,
        MessageBody=message
    )

    return response['MessageId']

def receive_message(queue_url):
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    if 'Messages' in response:
        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
        # print(type(message['Body']))
        return message['Body']
    else:
        return None

