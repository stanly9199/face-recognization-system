import requests
from linebot.v3.messaging import MessagingApi, ApiClient, Configuration
from linebot.v3.messaging.models import RichMenuRequest, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction, PostbackAction

# 設置你的 LINE Bot 設置
LINE_CHANNEL_ACCESS_TOKEN = 'nVKipaE+Eyon/3neezmYMUaXqkka7zN3gs/ltzzr91Rs/MSGkRpqulv1ZgQylQyI5wDdJGb6LdFf7zSrL89QzwchiFAb8OSp3H5X2v6QHbKatq0N5dm7leaoeRaaxI3lBkjsOawwfCz0RE+nXsqu2QdB04t89/1O/w1cDnyilFU='

# 初始化配置和 API 客戶端
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
api_client = ApiClient(configuration=configuration)
line_bot_api = MessagingApi(api_client)

# 創建第一個 Rich Menu
rich_menu_1 = RichMenuRequest(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="選單1",
    chat_bar_text="點擊這裡打開選單",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
            action=URIAction(uri="https://example.com", label="選項1")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=1250, y=0, width=1250, height=843),
            action=PostbackAction(data="action=buy", label="購買商品")
        )
    ]
)

# 創建並上傳第一個 Rich Menu
rich_menu_response_1 = line_bot_api.create_rich_menu(rich_menu_1)
rich_menu_id_1 = rich_menu_response_1.rich_menu_id  # 獲取 rich_menu_id

# 使用 HTTP 請求來上傳圖片
def upload_rich_menu_image(rich_menu_id, image_path):
    url = f"https://api.line.me/v2/bot/richmenu/{rich_menu_id}/content"
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "image/jpeg"
    }
    with open(image_path, 'rb') as f:
        response = requests.post(url, headers=headers, data=f)
    if response.status_code == 200:
        print(f"Rich Menu 圖片上傳成功，Rich Menu ID: {rich_menu_id}")
    else:
        print(f"上傳失敗: {response.status_code}, {response.text}")

# 上傳第一個選單的背景圖
upload_rich_menu_image(rich_menu_id_1, 'richmenu.png')

# 創建第二個 Rich Menu
rich_menu_2 = RichMenuRequest(
    size=RichMenuSize(width=2500, height=1686),
    selected=False,
    name="選單2",
    chat_bar_text="點擊這裡查看更多",
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=1250, height=843),
            action=URIAction(uri="https://anotherexample.com", label="選項2")
        )
    ]
)

# 創建並上傳第二個 Rich Menu
rich_menu_response_2 = line_bot_api.create_rich_menu(rich_menu_2)
rich_menu_id_2 = rich_menu_response_2.rich_menu_id  # 獲取 rich_menu_id

# 上傳第二個選單的背景圖
upload_rich_menu_image(rich_menu_id_2, 'richmenu.png')

# 將第一個 Rich Menu 設置為全域圖文選單
line_bot_api.set_default_rich_menu(rich_menu_id_1)

print(f"Rich Menu 1 已創建，ID: {rich_menu_id_1}")
print(f"Rich Menu 2 已創建，ID: {rich_menu_id_2}")
