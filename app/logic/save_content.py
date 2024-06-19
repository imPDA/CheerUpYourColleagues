from io import BytesIO

import pendulum
import requests

from infra.repositories.picture.base import BasePictureRepository, PictureObject
from infra.repositories.statistics.base import BaseStatisticsRepository, QuoteObject
from logic.init import init_container


def save_image_to_s3(*, image_url: str) -> str:
    container = init_container()

    response = requests.get(image_url)
    response.raise_for_status()

    mime_type, mime_subtype = response.headers['content-type'].split('/')

    if mime_type != 'image':
        raise Exception(f'Wrong content: {type}')

    picture_obj = PictureObject(
        ext=mime_subtype,
        obj=BytesIO(response.content),
    )

    picture_repository: BasePictureRepository = container.resolve(BasePictureRepository)

    picture_repository.create(picture_obj)

    return picture_obj.name


def save_statistics(*, ds: str, quotation_dict: dict, image_dict: dict) -> None:
    container = init_container()
    statistics_repository: BaseStatisticsRepository = container.resolve(
        BaseStatisticsRepository
    )
    quote_object = QuoteObject(
        quote=quotation_dict['text'],
        author=quotation_dict.get('author', ''),
        send_dt=int(pendulum.from_format(ds, 'YYYY-MM-DD').timestamp()),
        picture_url=image_dict['url'],
        picture_name=image_dict['name'],
    )
    statistics_repository.create(quote_object)
