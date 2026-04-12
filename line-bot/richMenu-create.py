import requests
import json
# 設定 headers，輸入你的 Access Token，記得前方要加上「Bearer 」( 有一個空白 )
headers = {'Authorization':'Bearer b8nOKxEmd1G+PCkDp4+SlMAJe6atx84R54xFcB9a+dE4YMkpU906DqH8w6ZNF9osAWPyqHEL7sRM5dggC43hzTVeps5fjYyW9Pz6ZWnz3hFHMPsxB/OsIJ8zSF0+MpMheBZIitYRtor/DcL1oaxrtQdB04t89/1O/w1cDnyilFU=','Content-Type':'application/json'}

body = {
    'size': {'width': 2500, 'height': 1146},   # 設定尺寸
    'selected': 'true',                        # 預設是否顯示
    'name': 'Richmenu demo',                   # 選單名稱
    'chatBarText': '選單',            # 選單在 LINE 顯示的標題
    'areas':[                                  # 選單內容
        {
          'bounds': {'x': 0, 'y': 0, 'width':1250, 'height': 1146},
          'action': {'type': 'postback', 'data': 'open'}
        },
        {
          'bounds': {'x': 1250, 'y': 0, 'width': 1250, 'height': 1146},
          'action': {'type': 'uri', 'label': '請至網站上傳圖片', 'uri': 'https://lab305.ngrok.pro/'}
        }
        
    ]
  }
# 向指定網址發送 request
req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                      headers=headers,data=json.dumps(body).encode('utf-8'))
# 印出得到的結果
print(req.text)

# import requests
# import json

# headers = {
#     'Authorization': 'nVKipaE+Eyon/3neezmYMUaXqkka7zN3gs/ltzzr91Rs/MSGkRpqulv1ZgQylQyI5wDdJGb6LdFf7zSrL89QzwchiFAb8OSp3H5X2v6QHbKatq0N5dm7leaoeRaaxI3lBkjsOawwfCz0RE+nXsqu2QdB04t89/1O/w1cDnyilFU=',
#     'Content-Type': 'application/json'
# }

# body = {
#     'size': {'width': 2500, 'height': 1146},  # 調整後的尺寸
#     'selected': True,
#     'name': 'Richmenu demo',
#     'chatBarText': '選單',
#     'areas': [
#         {
#             'bounds': {'x': 0, 'y': 0, 'width': 1250, 'height': 1146},
#             'action': {'type': 'message', 'text': '開鎖'}
#         },
#         {
#             'bounds': {'x': 1250, 'y': 0, 'width': 1250, 'height': 1146},
#             'action': {'type': 'message', 'text': '上傳圖片'}
#         }
#     ]
# }

# try:
#     response = requests.post('https://api.line.me/v2/bot/richmenu',
#                              headers=headers,
#                              data=json.dumps(body).encode('utf-8'))
#     response.raise_for_status()
#     print("Rich Menu 創建成功！")
#     print("Rich Menu ID:", response.json().get('richMenuId'))
# except requests.exceptions.RequestException as e:
#     print("發生錯誤:", e)
#     print("響應內容:", response.text)
