from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont

from infra.repositories.picture.base import Picture
from infra.repositories.quote.base import Quote

WHITE_SEMITRANSPARENT = (255, 255, 255, 181)
BLACK = (0, 0, 0)
TRANSPARENT = (0, 0, 0, 0)
RADIUS = 10
TEXT_PADDING = 5
MIN_FONT_SIZE = 14
LINE_SPACING = 1.15
MARGIN_BETWEEN_TEXTS = 10


def create_pil_image(picture: Picture) -> Image:
    true_image = Image.open(picture.obj)
    return true_image


def render_text(words: list[str], font: FreeTypeFont, max_width: int) -> Image:
    x = (max_width - TEXT_PADDING) * 0.5
    y = TEXT_PADDING

    lines = []
    text_on_current_line = ''

    for next_word in words:
        x0, y0, x1, y1 = font.getbbox(f'{text_on_current_line} {next_word}'.strip())
        total_line_width = x1 - x0
        line_height = y1 - y0

        if total_line_width + TEXT_PADDING > max_width:
            lines.append(((x, y), text_on_current_line.strip()))
            y += line_height * LINE_SPACING
            text_on_current_line = next_word
        else:
            text_on_current_line = f'{text_on_current_line} {next_word}'.strip()

    lines.append(((x, y), text_on_current_line.strip()))

    image = Image.new(
        'RGBA',
        (max_width, int(y + line_height * LINE_SPACING + TEXT_PADDING)),
        TRANSPARENT,
    )
    draw = ImageDraw.Draw(image)
    for position, text in lines:
        draw.text(position, text, font=font, fill=BLACK, anchor='ma')

    return image


def create_quotation_container(
    size: tuple[int, int],
    quotation_text: str,
    quotation_author: str,
    quotation_text_font_path: str = 'arial.ttf',
    quotation_author_font_path: str = 'ariali.ttf',
) -> Image:
    print(quotation_text, quotation_author)

    font_size = 32
    container_width, container_height = size

    while font_size >= MIN_FONT_SIZE:
        text_font = ImageFont.truetype(quotation_text_font_path, font_size)
        author_font = ImageFont.truetype(
            quotation_author_font_path, int(font_size * 0.75)
        )

        text_image = render_text(quotation_text.split(), text_font, container_width)
        author_image = render_text(
            quotation_author.split(), author_font, container_width
        )

        if (
            text_image.height + author_image.height + MARGIN_BETWEEN_TEXTS
            < container_height
        ):
            print(text_image.height, author_image.height, font_size)
            break

        font_size -= 1
    else:
        raise Exception('Quotation is too long! Can`t fit in into container size.')

    text_container = Image.new(
        'RGBA',
        (
            container_width,
            int(text_image.height + author_image.height + MARGIN_BETWEEN_TEXTS),
        ),
        TRANSPARENT,
    )
    text_container.paste(text_image, (0, 0))
    text_container.paste(author_image, (0, text_image.height))

    return text_container


def combine_image_and_quote(picture: Picture, quote: Quote) -> Picture:
    pil_image: Image = create_pil_image(picture)

    rect_w = pil_image.width * 0.8  # rectangle 80% of image width
    rect_h = pil_image.height * 0.33  # and 1/3 of image height

    rect_x0 = (pil_image.width - rect_w) * 0.5
    rect_y0 = (pil_image.height - rect_h) * 0.5
    rect_x1 = rect_x0 + rect_w
    rect_y1 = rect_y0 + rect_h

    draw = ImageDraw.Draw(pil_image, 'RGBA')
    draw.rounded_rectangle(
        (rect_x0, rect_y0, rect_x1, rect_y1), fill=WHITE_SEMITRANSPARENT, radius=RADIUS
    )

    quotation_container = create_quotation_container(
        (int(rect_w), int(rect_h)), quote.text, f'~ {quote.author} ~'
    )
    pil_image.paste(
        quotation_container,
        (
            int(rect_x0 + (rect_w - quotation_container.width + TEXT_PADDING) * 0.5),
            int(rect_y0 + (rect_h - quotation_container.height + TEXT_PADDING) * 0.5),
        ),
        mask=quotation_container.split()[3],
    )

    buff = BytesIO()
    return Picture(pil_image.save(buff, format='jpg'))


if __name__ == '__main__':
    from infra.repositories.picture.base import BasePictureRepository
    from infra.repositories.quote.base import BaseQuoteRepository, Quote
    from logic.init import init_container

    container = init_container()

    picture_repository = container.resolve(BasePictureRepository)
    quotes_repository = container.resolve(BaseQuoteRepository)

    picture = picture_repository.get_random()
    quote = quotes_repository.get_random()

    picture_with_quote = combine_image_and_quote(picture, quote)
