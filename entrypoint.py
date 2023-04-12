#!/usr/bin/env python3

import boto3
import os,re
import glob
from botocore.config import Config

print("plugin v1.4.1")
os.chdir(os.environ['WORKING_PATH'])

def upload_with_content_type_gzip(file):
    new_file = file[:-3]
    new_file_types = {
    '.css': 'text/css',
    '.js': 'text/javascript',
    }
    for i in new_file_types.keys():
        my_regex = r".*" + re.escape(i) + r"$"
        for m in re.findall(my_regex, new_file, re.IGNORECASE):
            new_ext = new_file_types.get(i)
            client.upload_file(file, os.environ['AWS_BUCKET'],
                f"{os.environ['AWS_BUCKET_KEY']}/{new_file}", ExtraArgs={'ContentType': new_ext,
                'ContentEncoding': 'gzip', 'ACL': 'public-read'})
            print(file, ext)

def upload_with_content_type(file, ext):
    client.upload_file(file, os.environ['AWS_BUCKET'],
        f"{os.environ['AWS_BUCKET_KEY']}/{file}", ExtraArgs={'ContentType': ext, 'ACL': 'public-read'})
    print(file, ext)

client = boto3.client('s3', 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'], 
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'], 
    region_name=os.environ['AWS_REGION']
)

file_types = {
'.bin': 'binary/octet-stream',
'.gltf': 'binary/octet-stream',
'.gz': 'application/x-gzip',
'.html': 'text/html',
'.jpeg': 'image/jpeg',
'.jpg': 'image/jpeg',
'.png': 'image/png',
'.svg': 'image/svg+xml',
'.txt': 'text/plain'
}

file_list = glob.glob('**/*.*', recursive=True)

for file in file_list:
    for i in file_types.keys():
        my_regex = r".*" + re.escape(i) + r"$"
        for m in re.findall(my_regex, file, re.IGNORECASE):
            ext = file_types.get(i)
            if ext == 'application/x-gzip':
                upload_with_content_type_gzip(file)
            else:
                upload_with_content_type(file, ext)
