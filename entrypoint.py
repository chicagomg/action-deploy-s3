#!/usr/bin/env python3

import boto3
import os,re
import glob
from botocore.config import Config

os.chdir(os.environ['WORKING_PATH'])

def upload_with_content_type_gzip(file, ext):
    client.upload_file(file, os.environ['AWS_BUCKET'],
        file, ExtraArgs={'ContentType': ext,
        'ContentEncoding': 'gzip', 'ACL': 'public-read'})
    print(file, ext)

def upload_with_content_type(file, ext):
    client.upload_file(file, os.environ['AWS_BUCKET'],
        file, ExtraArgs={'ContentType': ext, 'ACL': 'public-read'})
    print(file, ext)

client = boto3.client('s3', 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'], 
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'], 
    region_name=os.environ['AWS_REGION']
)

file_types = {
'.bin': 'binary/octet-stream',
'.css': 'text/css',
'.gltf': 'binary/octet-stream',
'.gz': 'application/x-gzip',
'.html': 'text/html',
'.jpeg': 'image/jpeg',
'.jpg': 'image/jpeg',
'.js': 'text/javascript',
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
            if ext == 'text/javascript' or ext == 'text/css':
                upload_with_content_type_gzip(file, ext)
            else:
                upload_with_content_type(file, ext)
