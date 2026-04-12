import cv2
from ultralytics import YOLO

# model=YOLO('face_700.pt')
model=YOLO('yolov8n-face.pt')

cap=cv2.VideoCapture(0)

while cap.isOpened():
    succeess, frame=cap.read()

    if succeess:
        result=model(frame)

        annonated_frame = result[0].plot()
        
        class_label = None
        conf = 0
        for box in result[0].boxes:
            class_id = int(box.cls)
            class_label = result[0].names[class_id]
            conf = box.conf.item()
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # 根據邊界框提取ROI
            roi = frame[y1:y2, x1:x2]
            # cv2.imwrite(f'face0.jpg', roi)
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

            # 提取正方形ROI
            square_roi = frame[new_y1:new_y2, new_x1:new_x2]

            # 保存正方形ROI
            cv2.imwrite('face0.jpg', square_roi)

        cv2.imshow("Face Recognition Inference" , annonated_frame)

        # time.sleep(0.5)

        if cv2.waitKey(1) & 0xFF == ord(" "):
            break
    else:
        break
cap.release()
cv2.destroyAllWindows()