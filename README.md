# Action Deploy S3
### it is waiting for next variables <br>
WORKING_PATH - working directory from which files deploy <br>
AWS_BUCKET <br>
AWS_ACCESS_KEY <br>
AWS_SECRET_KEY <br>
AWS_REGION <br>
AWS_BUCKET_KEY <br>


### script dosen't copy next types of files: <br>.js, .css, .hdr, .gltf, .bin files. <br>It just takes .gz version of them, cuts .gz, and pushes them to s3 with right metadata, like Content-Type and Content-Encoding:gzip.
