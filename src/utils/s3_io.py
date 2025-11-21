# src/utils/s3_io.py
import boto3
import json

s3 = boto3.client("s3")

def upload_json(bucket, key, data):
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

def download_json(bucket, key):
    obj = s3.get_object(Bucket=bucket, Key=key)
    
    return json.loads(obj["Body"].read().decode("utf-8"))