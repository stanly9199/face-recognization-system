import cv2
from ultralytics import YOLO
import face_recognition_v2 as r
import database_api as db
from datetime import datetime
from line_bot_api import broadcast_message_with_image
import serial # type: ignore

# COM_PORT = 'COM3'  # 請自行修改序列埠名稱
# BAUD_RATES = 9600
# ser = serial.Serial(COM_PORT, BAUD_RATES)

def face_capture(result):
    class_label = None
    conf = 0.0
    for box in result[0].boxes:
        class_id = int(box.cls)
        class_label = str(result[0].names[class_id])
        conf = box.conf.item()
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        # 計算寬度和高度
        width = x2 - x1
        height = y2 - y1

        # 計算正方形邊長
        side_length = max(width, height)

        # 計算正方形的中心位置
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # 根據邊長計算新的正方形框
        new_x1 = max(center_x - side_length // 2, 0)
        new_y1 = max(center_y - side_length // 2, 0)
        new_x2 = min(center_x + side_length // 2, 640)
        new_y2 = min(center_y + side_length // 2, 480)

        # 提取正方形
        square = frame[new_y1:new_y2, new_x1:new_x2]

        # 保存正方形
        cv2.imwrite('face0.jpg', square)
        
        return class_label, conf
    
def arcface_process(img):
    face_result = r.recognition()
    print(face_result)
    cv2.putText(img, f'{face_result}', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)  
    img_time = datetime.now().strftime("%y%m%d-%H%M%S")
    cv2.imwrite(f'../image/record/image_{img_time}.jpg', img)
    db.insert_result(face_result, img_time)
    
    return img_time, face_result

model=YOLO('yolov8n-face.pt')

cap=cv2.VideoCapture(0)

arcface_rest = 0

line_admin = db.get_admin()

ngrok = 'https://lab305.ngrok.pro/image'

while cap.isOpened():
    succeess, frame=cap.read()

    if succeess:
        result=model(frame)

        # cv2.imwrite('../image/linebot.jpg', frame)
        frame_resize = cv2.resize(frame, (200, 150))
        cv2.imwrite('../image/linebot_preview.jpg', frame_resize)

        annonated_frame = result[0].plot()

        cv2.imshow("Face Recognition Inference" , annonated_frame)
        
        class_label = None
        conf = 0.0
        
        face_capture_result = face_capture(result)
        
        if face_capture_result is not None:
            class_label, conf = face_capture_result

        with open('../linebot.txt', 'r') as f:
            linebot_open = f.read()
        if (class_label == 'face' and conf > 0.83 and arcface_rest == 0) or linebot_open == 'True':
            img_path, face_result = arcface_process(frame)
            with open('face_result.txt', 'w') as f:
                # write elements of list
                f.write('%s\n' %face_result)
            arcface_rest = 100
            # user_ids = line_admin
            user_ids = ['U1c91959f1415d1838f704fb8a19bed3a']
            # broadcast_message_with_image(user_ids, f'{ngrok}/record/image_{img_path}.jpg')
            # ser.write(b'28')
            with open('../linebot.txt', 'w') as f:
                f.write('False')

        if arcface_rest > 0:
            arcface_rest -= 1

        if cv2.waitKey(1) & 0xFF == ord(" "):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()