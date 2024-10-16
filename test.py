import os
import boto3
from boto3.dynamodb.types import TypeDeserializer
from poolscraper import get_cars

def deserialize_items(items):
    deserializer = TypeDeserializer()
    deserialized_items = []

    for item in items:
        deserialized_item = {k: deserializer.deserialize(v) for k, v in item.items()}
        deserialized_items.append(deserialized_item)

    return deserialized_items


def write_items_to_dynamo(session, table_name, items):
    table = session.Table(table_name)

    # Use batch_writer for efficient batch writing
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)

import json
def send_item_to_sns(topic_arn, item):
    # Initialize SNS client
    sns_client = boto3.client('sns')
    
    # Convert item to JSON string
    message = json.dumps(item)
    
    # Publish message to SNS topic
    response = sns_client.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='New Car Item Added'
    )
    
    return response

username = os.getenv("USERNAME") 
password = os.getenv("PASSWORD") 

output = get_cars(username=username, password=password)
print(f"Cars in the deloitte pool: {len(output)}")


dynamo_table_name = "poolscraper"

session = boto3.Session()
dynamodb = session.resource('dynamodb')
client = session.client('dynamodb')
paginator = client.get_paginator('scan')
scan_params = {
        'TableName': dynamo_table_name,
        'ProjectionExpression': "id"  # Only fetch the specified partition key
    }

pk_only_items = []

# Iterate through each page of scan results
for page in paginator.paginate(**scan_params):
    items = page.get('Items', [])
    pk_only_items.extend(items)


dicts = deserialize_items(pk_only_items)

keys_in_dynamo= set()

for item in dicts:
    keys_in_dynamo.add(item['id'])

keys_in_front = set()
new_cars=[]
for car in output:
    if car['id'] not in keys_in_dynamo:
        new_cars.append(car)
    keys_in_front.add(car['id'])


new_cars_ids = keys_in_front - keys_in_dynamo

print(f"New Cars in the deloitte pool: {len(new_cars_ids)}")

if new_cars:
    write_items_to_dynamo(session=dynamodb, table_name=dynamo_table_name,items=new_cars)
    for item in new_cars:
        send_item_to_sns(topic_arn="arn:aws:sns:eu-west-1:994911977949:alert_pool_cars",item=item)
        print(f"new car: {item}")