"""
Telegram bot module

Stores bots and provides interface for message sending
"""

# Third party imports
import telegram

# Local application imports
from config import CONFIG


PROXY_REQUEST = telegram.utils.request.Request(
    proxy_url='socks5://localhost:9999/',
    urllib3_proxy_kwargs={
        'username': '',
        'password': '',
    }
)

BOT = telegram.Bot(
    token=CONFIG.get('bot_token'),
    request=PROXY_REQUEST,
)


def send_message(message, chats):
    """ Sends message """
    for chat in chats:
        BOT.send_message(
            chat_id=chat,
            text=message,
            parse_mode='Markdown',
            disable_web_page_preview=True,
        )
