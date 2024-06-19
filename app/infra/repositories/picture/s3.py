from dataclasses import dataclass
from io import BytesIO
from typing import TypeVar

import boto3
from botocore.exceptions import ClientError

from .base import BasePictureRepository, PictureObject

S3_Client = TypeVar('S3_Client', bound=boto3.client)


@dataclass
class S3PictureRepository(BasePictureRepository):
    client: S3_Client
    bucket_name: str

    def __post_init__(self):
        try:
            self.client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise Exception(f'Bucket {self.bucket_name} not found') from e
            else:
                raise

    def create(self, picture_object: PictureObject) -> None:
        self.client.put_object(
            Bucket=self.bucket_name,
            Body=picture_object.obj.getvalue(),
            Key=picture_object.name,
        )

    def read(self, filename: str) -> PictureObject:
        uid, ext, *tail = filename.split('.')

        if tail:
            raise Exception(f'Wrong filename: {filename}')

        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=filename,
        )

        return PictureObject(
            uid=uid,
            ext=ext,
            obj=BytesIO(response['Body'].read()),
        )

    def delete(self, filename: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=filename,
        )

    def url_for(self, filename: str) -> str:
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=filename,
            )
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                raise Exception(f'File {filename} not found') from e
            else:
                raise

        return f'{self.client._endpoint.host}/{self.bucket_name}/{filename}'


if __name__ == '__main__':
    # TODO: mv -> tests
    from botocore.config import Config as AWSConfig

    from settings.config import BASE_PATH, Config

    config = Config(_env_file=BASE_PATH.parent / '.env')

    s3_client = boto3.client(
        's3',
        endpoint_url=config.timeweb_s3_endpoint_url,
        region_name=config.timeweb_s3_region_name,
        aws_access_key_id=config.timeweb_s3_access_key,
        aws_secret_access_key=config.timeweb_s3_secret_key,
        config=AWSConfig(s3={'addressing_style': 'path'}),
    )

    path_to_file = r'I:\Discord\cat_jam.jpg'
    with open(path_to_file, 'rb') as file:
        name, ext = path_to_file.split('.')
        picture = PictureObject(ext=ext, obj=BytesIO(file.read()))

        s3_repo: BasePictureRepository = S3PictureRepository(
            s3_client, config.timeweb_s3_pictures_bucket_name
        )
        s3_repo.create(picture)
