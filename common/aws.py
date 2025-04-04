import re

import boto3 as boto3
from botocore.exceptions import ClientError
from src.settings import Settings
from common.logger import get_logger

logger = get_logger(__name__)


class S3:
    BUCKET_URL = f"https://{Settings.aws_s3.BUCKET_NAME}.s3.amazonaws.com/"

    @staticmethod
    def get_object_url(object_key: str) -> str:
        return S3.BUCKET_URL + object_key

    @staticmethod
    def get_object_key_from_uri(uri: str) -> str | None:
        regex = r"s3\.amazonaws\.[\w-]+/"
        try:
            _, object_key = re.split(regex, uri)
        except ValueError:
            return None
        return object_key

    def __init__(self):
        # for local use you maybe need add param profile_name
        self.__s3client = boto3.Session(region_name=Settings.aws_s3.REGION_NAME).client("s3")

    def delete_object(self, object_key: str):
        self.__s3client.delete_object(Bucket=Settings.aws_s3.BUCKET_NAME, BucKey=object_key)

    def get_object(self, object_key: str):
        return self.__s3client.get_object(Bucket=Settings.aws_s3.BUCKET_NAME, Key=object_key)[
            "Body"
        ]

    def get_presigned_post_data(self, object_key, fields=None, conditions=None, expiration=3600):
        if conditions is None:
            conditions = [["content-length-range", 100, 26214400]]

        try:
            response = self.__s3client.generate_presigned_post(
                Bucket=Settings.aws_s3.BUCKET_NAME,
                Key=object_key,
                Fields=fields,
                ExpiresIn=expiration,
                Conditions=conditions,
            )
        except (ClientError, TypeError) as e:
            logger.error(f"Generate presigned post data error: {str(e)}")
            return None
        return response
