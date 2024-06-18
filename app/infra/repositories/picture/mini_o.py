from dataclasses import dataclass
from io import BytesIO

from minio import Minio

from .base import BasePictureRepository, PictureObject


@dataclass
class MinioPictureRepository(BasePictureRepository):
    client: Minio
    bucket_name: str

    def create(self, picture_object: PictureObject) -> None:
        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            self.client.make_bucket(self.bucket_name)

        self.client.put_object(
            self.bucket_name,
            f'{picture_object.uid}.jpg',
            picture_object.obj,
            picture_object.size,
        )

    def read(self, filename: str) -> PictureObject:
        uid, ext, *tail = filename.split('.')
        if tail:
            raise ValueError(f'Invalid identifier: {filename}')

        try:
            response = self.client.get_object(self.bucket_name, filename)
            obj = BytesIO(response.data)
        finally:
            response.close()
            response.release_conn()

        return PictureObject(uid=uid, obj=obj, ext=ext)

    def delete(self, filename: str) -> None:
        uid, ext, *tail = filename.split('.')
        if tail:
            raise ValueError(f'Invalid identifier: {filename}')

        self.client.remove_object(self.bucket_name, filename)
