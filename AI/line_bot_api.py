from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage

app = Flask(__name__)

# Set your channel access token and secret
LINE_CHANNEL_ACCESS_TOKEN = 'b8nOKxEmd1G+PCkDp4+SlMAJe6atx84R54xFcB9a+dE4YMkpU906DqH8w6ZNF9osAWPyqHEL7sRM5dggC43hzTVeps5fjYyW9Pz6ZWnz3hFHMPsxB/OsIJ8zSF0+MpMheBZIitYRtor/DcL1oaxrtQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'e9974ba82af1cb994fd0da98a03e3ec6'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def broadcast_message_with_image(user_ids, image_url, preview_image_url=None):
    if preview_image_url is None:
        preview_image_url = image_url

    # message = TextSendMessage(text=message_text)
    image_message = ImageSendMessage(
        original_content_url=image_url,
        preview_image_url=preview_image_url
    )

    for user_id in user_ids:
        line_bot_api.push_message(user_id, image_message)

if __name__ == "__main__":
    app.run()
