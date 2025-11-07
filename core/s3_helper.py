def upload_file_to_s3(file_path, bucket_name, region):
    print(f"Uploading {file_path} to s3://{bucket_name}/ in region {region}")
    return f"{file_path.name}"
