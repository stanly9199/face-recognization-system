from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, PostbackEvent
from linebot.models.send_messages import ImageSendMessage
app = Flask(__name__)

# 設置你的 LINE Bot 設置
LINE_CHANNEL_SECRET = 'e9974ba82af1cb994fd0da98a03e3ec6'
LINE_CHANNEL_ACCESS_TOKEN = 'b8nOKxEmd1G+PCkDp4+SlMAJe6atx84R54xFcB9a+dE4YMkpU906DqH8w6ZNF9osAWPyqHEL7sRM5dggC43hzTVeps5fjYyW9Pz6ZWnz3hFHMPsxB/OsIJ8zSF0+MpMheBZIitYRtor/DcL1oaxrtQdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 管理員的 LINE User IDs
ADMIN_USER_IDS = ['U1c91959f1415d1838f704fb8a19bed3a']

# 判斷是否為管理員
def is_admin(user_id):
    return user_id in ADMIN_USER_IDS

# 通知管理員門鎖已開啟
def notify_admins():
    for admin_id in ADMIN_USER_IDS:
        line_bot_api.push_message(admin_id, TextSendMessage(text="門鎖已開啟"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理使用者開始與 Bot 互動時的 Follow Event
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id

    if is_admin(user_id):
        # 如果是管理員，告知管理員模式已啟用
        reply_message = "管理員模式已啟用"
    else:
        # 一般使用者的歡迎訊息
        reply_message = "歡迎使用，我是您的機器人助理。"

    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# 當使用者發送訊息時檢查身份
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # 檢查是否為管理員
    if is_admin(user_id):
        # 管理員身份通知
        status_message = "管理員模式已啟用。"
    else:
        # 一般使用者身份通知
        status_message = "您是一般使用者，歡迎使用。"

    # 如果使用者發送 "open" 指令，通知管理員門鎖已開啟
    if user_message.lower() == "open" or user_message == '開鎖':
        notify_admins()
        reply_message = f"{status_message}\n管理員已收到通知。"
    elif user_message == "ID":
        reply_message = f"{status_message}\n你的 LINE ID 是: {user_id}"
    else:
        reply_message = f"{status_message}\n你說的是: {user_message}"

    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# 處理 postback 事件
@handler.add(PostbackEvent)
def handle_postback(event):
    # Log incoming event for debugging
    print(f"PostbackEvent received: {event}")
    
    # Get postback data and user ID
    data = event.postback.data
    user_id = event.source.user_id

    # Process only if the data matches 'open'
    if data == 'open':
        if user_id in ADMIN_USER_IDS:
        # Reply to the user
            # with tempfile.NamedTemporaryFile(mode='w', delete=False, prefix='linebot', suffix='.txt') as temp_file:
            #         temp_file.write('True')
            with open('linebot.txt', 'w') as f:
                f.write('True')
            # write.w()
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='門鎖已開啟')
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text='已送出開門請求')
                ]
            )
            image = ImageSendMessage(
                original_content_url='https://lab305.ngrok.pro/image/linebot_preview.jpg',
                preview_image_url='https://lab305.ngrok.pro/image/linebot_preview.jpg'
            )
            for admin_id in ADMIN_USER_IDS:
                line_bot_api.push_message(admin_id, image)
        # Additional backend logic
        print(f"User {user_id} switched to menu 2")

if __name__ == "__main__":
    app.run(host="localhost", port=5000)



