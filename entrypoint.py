#!/usr/bin/env python3

import boto3
import os,re
import glob
import time
from botocore.config import Config

print("plugin v1.6.0")
os.chdir(os.environ['WORKING_PATH'])

file_types = {
'.bin': 'binary/octet-stream',
'.css': 'text/css',
'.gltf': 'model/gltf+json',
'.hdr': 'image/vnd.radiance',
'.html': 'text/html',
'.jpeg': 'image/jpeg',
'.jpg': 'image/jpeg',
'.js': 'text/javascript',
'.mind': 'binary/octet-stream',
'.png': 'image/png',
'.svg': 'image/svg+xml',
'.txt': 'text/plain',
'.webp': 'image/webp',
'.gz': 'application/x-gzip'
}


def upload_with_content_type_gzip(file):
    new_file = file[:-3]

    for i in file_types.keys():
        my_regex = r".*" + re.escape(i) + r"$"
        for m in re.findall(my_regex, new_file, re.IGNORECASE):
            new_ext = file_types.get(i)
            s3.upload_file(file, os.environ['AWS_BUCKET'],
                f"{os.environ['AWS_BUCKET_KEY']}/{new_file}", ExtraArgs={'ContentType': new_ext,
                'ContentEncoding': 'gzip', 'ACL': 'public-read'})
            print("compessed ", file, ext)


def upload_with_content_type(file, ext):
    s3.upload_file(file, os.environ['AWS_BUCKET'],
        f"{os.environ['AWS_BUCKET_KEY']}/{file}", ExtraArgs={'ContentType': ext, 'ACL': 'public-read'})
    print(file, ext)


def create_invalidation():
    res = cf.create_invalidation(
        DistributionId=os.environ['DISTRIBUTION_ID'],
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/*'
                ]
            },
            'CallerReference': str(time.time()).replace(".", "")
        }
    )
    invalidation_id = res['Invalidation']['Id']
    return invalidation_id


s3 = boto3.client('s3', 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'], 
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'], 
    region_name=os.environ['AWS_REGION']
)

cf = boto3.client('cloudfront', 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'], 
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'], 
    region_name=os.environ['AWS_REGION']
)


file_list = glob.glob('**/*.*', recursive=True)

for i in file_types.keys():
    for file in file_list:
    
        my_regex = r".*" + re.escape(i) + r"$"
        for m in re.findall(my_regex, file, re.IGNORECASE):
            ext = file_types.get(i)
            if ext != 'application/x-gzip':
                upload_with_content_type(file, ext)
            elif ext == 'application/x-gzip':
                upload_with_content_type_gzip(file)


ida = create_invalidation()
print("Invalidation created successfully with Id: " + ida)
