import cv2
import os
from ultralytics import YOLO

# 加載YOLO模型
model = YOLO('yolov8n-face.pt')

def main():
    # 圖像數量
    image_num = 5

    # 資料夾路徑
    folder_path = 'face_data'
    folder_list = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    num_folders = len(folder_list)

    # 循環處理每個資料夾和圖像
    for id in range(num_folders):
        for i in range(image_num):
            file_path = f"face_data/person{id+1}/image/{i+1}.jpg"
            save_dir = f"face_data/person{id+1}/image_face"

            # 檢查保存目錄是否存在，如果不存在則創建
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                print(f"Directory {save_dir} created.")

            # 檔名的邏輯：如果沒有標記就加上_unmark，否則使用正常的檔名
            save_path = os.path.join(save_dir, f"{i+1}.jpg")
            unmarked_save_path = os.path.join(save_dir, f"{i+1}_unmark.jpg")

            # 讀取圖像
            cap = cv2.imread(file_path)
            if cap is None:
                print(f"Error loading image {file_path}")
                continue

            # 使用YOLO進行偵測
            result = model(cap)

            # 獲取圖像的尺寸
            cap_h, cap_w = cap.shape[:2]

            # 如果YOLO沒有偵測到任何物件
            if len(result[0].boxes) == 0:
                # 保存未標記的圖像並在檔名中加上_unmark
                if cv2.imwrite(unmarked_save_path, cap):
                    print(f"Unmarked image saved at {unmarked_save_path}")
                else:
                    print(f"Failed to save unmarked image at {unmarked_save_path}")
                continue

            # 如果有偵測到物件，處理YOLO標記的物件
            for box in result[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # 邊界框座標
                
                # 計算寬度和高度
                width = x2 - x1
                height = y2 - y1

                # 計算正方形邊長
                side_length = max(width, height)

                # 計算正方形的中心位置
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2

                # 根據邊長計算新的正方形框，確保不超出邊界
                new_x1 = max(center_x - side_length // 2, 0)
                new_y1 = max(center_y - side_length // 2, 0)
                new_x2 = min(center_x + side_length // 2, cap_w)
                new_y2 = min(center_y + side_length // 2, cap_h)

                # 提取正方形ROI
                square_roi = cap[new_y1:new_y2, new_x1:new_x2]

                # 保存調整大小後的ROI，並檢查是否成功
                if cv2.imwrite(save_path, square_roi):
                    print(f"Resized image saved at {save_path}")
                else:
                    print(f"Failed to save image at {save_path}")

    print("Process completed!")

if __name__ == '__main__':
    main()