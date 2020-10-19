#!/usr/bin/python3
# -*- coding: utf-8 -

import boto3

def put_table(item, table='Refrigerators'):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table)
    table.put_item(Item=item)

