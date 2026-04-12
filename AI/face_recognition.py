import os
import os.path as osp
import cv2
import numpy as np
import onnxruntime
from scrfd import SCRFD
from arcface_onnx import ArcFaceONNX

# Set ONNX logging severity to suppress verbose logs
onnxruntime.set_default_logger_severity(3)

# Define the directory containing the ONNX models
assets_dir = 'models'

# Initialize the face detector (SCRFD) and face recognizer (ArcFace)
detector = SCRFD(os.path.join(assets_dir, 'buffalo_l/det_10g.onnx'))
# detector = SCRFD(os.path.join(assets_dir, 'version-RFB-640.onnx'))
detector.prepare(0)
model_path = os.path.join(assets_dir, 'buffalo_l/w600k_r50.onnx')
# model_path = os.path.join(assets_dir, '../model.onnx')
rec = ArcFaceONNX(model_path)
rec.prepare(0)

def compare_images(img1_path, img2_path):
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
    image2 = cv2.imread(img2_path)

    # Detect faces in both images
    bboxes1, kpss1 = detector.autodetect(image1, max_num=1)
    if bboxes1.shape[0] == 0:
        return -1.0, "Face not found in Image-1"

    bboxes2, kpss2 = detector.autodetect(image2, max_num=1)
    if bboxes2.shape[0] == 0:
        return -1.0, "Face not found in Image-2"

    # Get the keypoints for alignment
    kps1 = kpss1[0]
    kps2 = kpss2[0]

    # Extract features using ArcFace model
    feat1 = rec.get(image1, kps1)
    feat2 = rec.get(image2, kps2)

    # Compute similarity between two feature vectors
    sim = rec.compute_sim(feat1, feat2)

    # Determine if they are the same person based on similarity threshold
    if sim < 0.2:
        conclu = 'They are NOT the same person'
    elif sim >= 0.2 and sim < 0.28:
        conclu = 'They are LIKELY TO be the same person'
    else:
        conclu = 'They ARE the same person'

    return sim, conclu


def recognition(img1, img2):
    # You can specify your image paths here
    # img1 = "1.jpg"
    # img2 = "4.jpg"

    # Run the comparison
    similarity, message = compare_images(img1, img2)

    # Output the result
    # print(f'Similarity: {similarity:.4f}, Message: {message}')
    
    # if similarity > 0.3:
    #     return 'same'
    # else:
    #     return 'diff'
    return similarity
    

if __name__ == '__main__':
    recognition()