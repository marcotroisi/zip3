import boto3
import botocore
from botocore import response
from moto import mock_s3

from zip3 import Zip3

bucket_name = "test_bucket"

@mock_s3
def test_get_files():
    """Returns Key and Body of objects from a directory in an S3 bucket"""
    conn = boto3.resource("s3", region_name="us-east-1")
    conn.create_bucket(Bucket=bucket_name)

    s3 = boto3.client("s3", region_name="us-east-1")
    s3.put_object(Bucket=bucket_name, Key="test_directory/file1.txt", Body="abcde")
    s3.put_object(Bucket=bucket_name, Key="test_directory/file2.txt", Body="hghid")

    Z3 = Zip3(conn, s3_bucket=bucket_name)
    objects = Z3._get_files_from_s3_directory("test_directory")
    body = objects["test_directory/file1.txt"].read().decode("utf-8")
    assert len(objects) is 2
    assert body == "abcde"

@mock_s3
def test_generate_zip_in_memory(capsys):
    """Generates a zip archive in memory with a number of files in it"""
    with capsys.disabled():
        conn = boto3.resource("s3", region_name="us-east-1")
        conn.create_bucket(Bucket=bucket_name)
        Z3 = Zip3(conn, s3_bucket=bucket_name)
        
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.put_object(Bucket=bucket_name, Key="test_directory/file1.txt", Body="abcde")
        s3.put_object(Bucket=bucket_name, Key="test_directory/file2.txt", Body="hghid")

        objects = Z3._get_files_from_s3_directory("test_directory")
        print("objects")
        print(objects)
        archive = Z3._generate_zip_in_memory(objects)
        print("archive")
        print(archive)
        s3.put_object(Bucket=bucket_name, Key="test_directory/archive.zip", Body=archive)

@mock_s3
def test_generate_zip_in_memory_and_put_in_s3():
    """Generates a zip archive in memory and saves it on S3"""
    conn = boto3.resource("s3", region_name="eu-west-2")
    # Create Bucket
    conn.create_bucket(Bucket=bucket_name)
    # Save some objects in the bucket
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.put_object(Bucket=bucket_name, Key="test_directory/file1.txt", Body="abcde")
    s3.put_object(Bucket=bucket_name, Key="test_directory/file2.txt", Body="hghid")
    # Generate ZIP and save it on S3
    Z3 = Zip3(conn, s3_bucket=bucket_name)
    output_key = "test_folder/archive2.zip"
    Z3.generate(input_directory="test_folder", output_key=output_key)

    bucket = conn.Bucket(bucket_name)
    objs = list(bucket.objects.filter(Prefix=output_key))
    exists = any([w.key == output_key for w in objs])
    assert exists == True