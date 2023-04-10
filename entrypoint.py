#!/usr/bin/env python3
'''
import boto3
import os,re,
import glob

BUCKET = "cber.lol"

client = boto3.client("s3")

file_types = {
'.css': 'text/css',
'.html': 'text/html',
'.jpeg': 'image/jpeg',
'.jpg': 'image/jpeg',
'.js': 'text/javascript',
'.png': 'image/png',
'.svg': 'image/svg+xml',
'.txt': 'text/plain',
}

file_list = glob.glob('**/*.*', recursive=True)

for a in file_list:
    for i in file_types.keys():
        my_regex = r".*" + re.escape(i) + r"$"
        if re.search(my_regex, a, re.IGNORECASE):
            ext = file_types.get(i)
            print(a, ext)
            client.upload_file(a, BUCKET, a, ExtraArgs={'ContentType': ext, 'ACL': 'public-read'})
            break
        else:
            client.upload_file(a, BUCKET, a, ExtraArgs={'ACL': 'public-read'})
'''
print("Hello World")