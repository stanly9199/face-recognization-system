import os
import os.path as osp
import cv2
import numpy as np
import onnxruntime
from scrfd import SCRFD
from arcface_onnx import ArcFaceONNX
import time

os.environ['CUDA_LAUNCH_BLOCKING'] = '1'

# Set ONNX logging severity to suppress verbose logs
onnxruntime.set_default_logger_severity(3)

# Define the directory containing the ONNX models
assets_dir = 'models/buffalo_l'

# Initialize the face detector (SCRFD) and face recognizer (ArcFace)
detector = SCRFD(os.path.join(assets_dir, 'det_10g.onnx'))
detector.prepare(0)
model_path = os.path.join(assets_dir, 'w600k_r50.onnx')
rec = ArcFaceONNX(model_path)
rec.prepare(0)

def compare_images(img1_path, img2_feature):
    """
    Compares two images and returns their similarity score and conclusion.
    
    Args:
        img1_path (str): Path to the first image.
        img2_path (str): Path to the second image.
    
    Returns:
        tuple: Similarity score and conclusion message.
    """
    # Read the images from the specified paths
    image1 = cv2.imread(img1_path)

    # Detect faces in both images
    bboxes1, kpss1 = detector.autodetect(image1, max_num=1)
    if bboxes1.shape[0] == 0:
        return -1.0, "Face not found"

    # Get the keypoints for alignment
    kps1 = kpss1[0]

    # Extract features using ArcFace model
    feat1 = rec.get(image1, kps1)
    feat2 = np.load(img2_feature)

    # Compute similarity between two feature vectors
    sim = rec.compute_sim(feat1, feat2)

    # Determine if they are the same person based on similarity threshold
    # if sim < 0.5:
    #     conclu = 'They are NOT the same person'
    # elif sim >= 0.2 and sim < 0.28:
    #     conclu = 'They are LIKELY TO be the same person'
    # else:
    #     conclu = 'They ARE the same person'

    return sim


def recognition():
    # You can specify your image paths here
    img1 = "face0.jpg"
    
    sim_list: list[tuple[int, float]] = []
    
    for i in range(3):
        img2 = f'feature_data/person{i+1}_feature.npy'

        # Run the comparison
        similarity = compare_images(img1, img2)
        
        sim_list.append((i+1, similarity))

        # Output the result
        # print(f'Similarity: {similarity:.4f}, Message: {message}')
        print(f'Similarity: {similarity:.4f}')
    
    index, sim = max(sim_list, key=lambda x: x[1])
    
    if sim > 0.42:
        return f'person{index}'
    else:
        return 'unknown'
    

if __name__ == '__main__':
    while True:
        print(recognition())
        time.sleep(5)