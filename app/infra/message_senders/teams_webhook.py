import json
import logging
from dataclasses import dataclass

import requests

from .base import BaseMessageSender


def generate_card(**kwargs) -> str:
    body = []

    if kwargs.get('image'):
        body.append(
            {
                'type': 'Image',
                'url': kwargs.get('image'),
                'wrap': 'true',
                'horizontalAlignment': 'Center',
            }
        )

    if kwargs.get('quote'):
        body.append(
            {
                'type': 'TextBlock',
                'text': kwargs.get('quote'),
                'horizontalAlignment': 'right',
                'size': 'Medium',
            }
        )

    if kwargs.get('author'):
        body.append(
            {
                'type': 'TextBlock',
                'text': kwargs.get('author'),
                'horizontalAlignment': 'right',
                'size': 'Medium',
            }
        )

    body.append(
        {
            'type': 'TextBlock',
            'text': '_sent by Dmitry Patryshev_',
            'horizontalAlignment': 'right',
            'size': 'Small',
        }
    )

    message = {
        'type': 'message',
        'attachments': [
            {
                'contentType': 'application/vnd.microsoft.card.adaptive',
                'contentUrl': None,
                'content': {
                    '$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',
                    'type': 'AdaptiveCard',
                    'version': '1.2',
                    'body': body,
                },
            }
        ],
    }

    return json.dumps(message)


@dataclass
class TeamsWebhookMessageSender(BaseMessageSender):
    webhook: str

    def send(self, **kwargs) -> None:
        headers = {'Content-Type': 'application/json'}
        payload = generate_card(**kwargs)

        logging.getLogger('app').debug(f'Sending message: {payload}')

        response = requests.post(self.webhook, headers=headers, data=payload)

        logging.getLogger('app').debug('Get response: %s', response.content)

        response.raise_for_status()
