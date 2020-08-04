from io import BytesIO
import zipfile

import boto3


class Zip3:
    def __init__(self, s3_client, s3_bucket: str):
        self._s3 = s3_client
        self._s3_bucket = s3_bucket

    def _get_files_from_s3_directory(self, directory: str):
        my_bucket = self._s3.Bucket(self._s3_bucket)

        keys = dict()
        for object_summary in my_bucket.objects.filter(Prefix=directory):
            key = object_summary.key
            body = object_summary.get()["Body"]
            keys[key] = body

        return keys

    def _generate_zip_in_memory(self, s3_files: dict):
        mem_zip = BytesIO()

        with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            print(f"s3_files {s3_files}")
            for key, file_content in s3_files.items():
                print(f"key {key}; file_content {file_content}")
                zf.writestr(key, file_content.read())

        return mem_zip

    def generate(self, input_directory, output_key="archive.zip"):
        bucket = self._s3.Bucket(self._s3_bucket)
        objects = self._get_files_from_s3_directory(input_directory)
        archive = self._generate_zip_in_memory(objects)
        archive.seek(0)
        bucket.upload_fileobj(archive, output_key)

