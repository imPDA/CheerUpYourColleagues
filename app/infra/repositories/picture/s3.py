from dataclasses import dataclass
from io import BytesIO
from typing import Any

from .base import BasePictureRepository, Picture


@dataclass
class S3PictureRepository(BasePictureRepository):
    bucket: Any

    def get(self, identifier) -> Picture:
        s3_object = self.bucket.Object(identifier)
        stream = BytesIO()
        s3_object.download_fileobj(stream)

        return Picture(obj=stream)

    def get_random(self) -> BytesIO:
        # for future
        raise NotImplementedError()
