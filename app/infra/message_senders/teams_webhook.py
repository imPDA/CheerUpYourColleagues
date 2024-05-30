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
                "type": "Image",
                "url": kwargs.get('image'),
                "wrap": "true",
            }
        )

    if kwargs.get('text'):
        body.append(
            {
                "type": "TextBlock",
                "text": kwargs.get('text'),
                "horizontalAlignment": "center",
            }
        )

    message = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "contentUrl": None,
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.2",
                    "body": body
                }
            }
        ]
    }

    logging.getLogger('app').debug(f"Created message: {message}")

    return json.dumps(message)


@dataclass
class TeamsWebhookMessageSender(BaseMessageSender):
    webhook: str

    def send(self, **kwargs) -> None:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(
            self.webhook, headers=headers, json=generate_card(**kwargs)
        )
        response.raise_for_status()
