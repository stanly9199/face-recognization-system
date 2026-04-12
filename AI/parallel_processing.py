import cv2
from ultralytics import YOLO
import face_recognition_v2 as r
import database_api as db
import torch
from datetime import datetime
import asyncio

model = YOLO('yolov8n-face.pt')
cap = cv2.VideoCapture(0)

async def process_yolo(frame):
    result = model(frame)
    annonated_frame = result[0].plot()
    
    for box in result[0].boxes:
        class_id = int(box.cls)
        class_label = result[0].names[class_id]
        conf = box.conf.item()
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if class_label == 'face' and conf >= 0.83:
            roi = frame[y1:y2, x1:x2]
            square_roi = extract_square_face(roi, x1, y1, x2, y2)
            return square_roi, annonated_frame
    return None, annonated_frame

def extract_square_face(frame, x1, y1, x2, y2):
    width = x2 - x1
    height = y2 - y1
    side_length = max(width, height)
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    new_x1 = max(center_x - side_length // 2, 0)
    new_y1 = max(center_y - side_length // 2, 0)
    new_x2 = min(center_x + side_length // 2, 640)
    new_y2 = min(center_y + side_length // 2, 480)
    
    return frame[new_y1:new_y2, new_x1:new_x2]

async def process_arcface(square_roi):
    face_result = r.recognition()  # Perform face recognition
    img_time = datetime.now().strftime("%y%m%d-%H%M%S")
    cv2.imwrite(f'record/image_{img_time}.jpg', square_roi)
    db.insert_result(face_result, img_time)
    return face_result

async def main_loop():
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        square_roi, annonated_frame = await process_yolo(frame)
        cv2.imshow("Face Recognition Inference", annonated_frame)

        if square_roi is not None:
            await process_arcface(square_roi)

        if cv2.waitKey(1) & 0xFF == ord(" "):
            break

if __name__ == "__main__":
    asyncio.run(main_loop())

cap.release()
cv2.destroyAllWindows()
