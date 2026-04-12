
#upload_image_administrator
Invoke-WebRequest -Uri "https://api-data.line.me/v2/bot/richmenu/richmenu-789396dcc982f7174e75407b8ee54318/content" `
-Method POST `
-Headers @{"Authorization"="Bearer b8nOKxEmd1G+PCkDp4+SlMAJe6atx84R54xFcB9a+dE4YMkpU906DqH8w6ZNF9osAWPyqHEL7sRM5dggC43hzTVeps5fjYyW9Pz6ZWnz3hFHMPsxB/OsIJ8zSF0+MpMheBZIitYRtor/DcL1oaxrtQdB04t89/1O/w1cDnyilFU="; "Content-Type"="image/png"} `
-InFile "F:\line-bot\richMenu-admin.png"

#link richmenu to linebot
Invoke-RestMethod -Uri "https://api.line.me/v2/bot/user/all/richmenu/richmenu-789396dcc982f7174e75407b8ee54318" -Method POST -Headers @{ Authorization = "Bearer b8nOKxEmd1G+PCkDp4+SlMAJe6atx84R54xFcB9a+dE4YMkpU906DqH8w6ZNF9osAWPyqHEL7sRM5dggC43hzTVeps5fjYyW9Pz6ZWnz3hFHMPsxB/OsIJ8zSF0+MpMheBZIitYRtor/DcL1oaxrtQdB04t89/1O/w1cDnyilFU=" }




#delete richmenu
#Invoke-RestMethod -Uri "https://api.line.me/v2/bot/richmenu/richmenu-3ebf30ecb761c036f4fb3d66233dd38a" -Method DELETE -Headers @{ Authorization = "Bearer nVKipaE+Eyon/3neezmYMUaXqkka7zN3gs/ltzzr91Rs/MSGkRpqulv1ZgQylQyI5wDdJGb6LdFf7zSrL89QzwchiFAb8OSp3H5X2v6QHbKatq0N5dm7leaoeRaaxI3lBkjsOawwfCz0RE+nXsqu2QdB04t89/1O/w1cDnyilFU=" }


#admin richmenuid=richmenu-0b7b4b8180aedba888812d659ea9d1de
