#!/usr/bin/env python3

import boto3
import os,re
import glob
from botocore.config import Config

print("plugin v1.5.0")
os.chdir(os.environ['WORKING_PATH'])

file_types = {
'.bin': 'binary/octet-stream',
'.css': 'text/css',
'.gltf': 'model/gltf+json',
'.gz': 'application/x-gzip',
'.hdr': 'binary/octet-stream',
'.html': 'text/html',
'.jpeg': 'image/jpeg',
'.jpg': 'image/jpeg',
'.js': 'text/javascript',
'.png': 'image/png',
'.svg': 'image/svg+xml',
'.txt': 'text/plain',
'.webp': 'binary/octet-stream'
}

def upload_with_content_type_gzip(file):
    new_file = file[:-3]

    for i in file_types.keys():
        my_regex = r".*" + re.escape(i) + r"$"
        for m in re.findall(my_regex, new_file, re.IGNORECASE):
            new_ext = file_types.get(i)
            client.upload_file(file, os.environ['AWS_BUCKET'],
                f"{os.environ['AWS_BUCKET_KEY']}/{new_file}", ExtraArgs={'ContentType': new_ext,
                'ContentEncoding': 'gzip', 'ACL': 'public-read'})
            print("compessed ", file, ext)

def upload_with_content_type(file, ext):
    client.upload_file(file, os.environ['AWS_BUCKET'],
        f"{os.environ['AWS_BUCKET_KEY']}/{file}", ExtraArgs={'ContentType': ext, 'ACL': 'public-read'})
    print(file, ext)

client = boto3.client('s3', 
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'], 
    aws_secret_access_key=os.environ['AWS_SECRET_KEY'], 
    region_name=os.environ['AWS_REGION']
)



file_list = glob.glob('**/*.*', recursive=True)


for file in file_list:
    for i in file_types.keys():
        my_regex = r".*" + re.escape(i) + r"$"
        for m in re.findall(my_regex, file, re.IGNORECASE):
            ext = file_types.get(i)
            if ext != 'application/x-gzip':
                upload_with_content_type(file, ext)
            elif ext == 'application/x-gzip':
                if os.environ['CDN_COMPRESSION'] == True:
                    upload_with_content_type_gzip(file)
