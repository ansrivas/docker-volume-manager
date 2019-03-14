# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""An experimental module to support uploads directly to s3."""


import boto3


def upload_to_s3(endpoint_url, access_key, secret, bucket, local_file_path, filename_on_s3=None):
    """Upload a given file name to s3.

    Args:
        endpoint_url (str) : The end point to upload the file to, for eg. https://db-backup.ams3.digitaloceanspaces.com
        access_key (str)   : ACCESS_KEY for this bucket.
        secret (str)       : SECRET to access this bucket.
        bucket (str)       : Bucket where we will upload this file
    """
    session = boto3.session.Session()
    client = session.client("s3",
                            endpoint_url=endpoint_url,
                            aws_access_key_id=access_key,
                            aws_secret_access_key=secret)

    client.upload_file(local_file_path, bucket, filename_on_s3)
