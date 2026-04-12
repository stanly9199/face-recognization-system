import os
import cv2
import numpy as np
import onnxruntime
from scrfd import SCRFD
from arcface_onnx import ArcFaceONNX

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

def get_feature(img_path):
    """
    Compares two images and returns their similarity score and conclusion.
    
    Args:
        img1_path (str): Path to the first image.
        img2_path (str): Path to the second image.
    
    Returns:
        tuple: Similarity score and conclusion message.
    """
    # Read the images from the specified paths
    image1 = cv2.imread(img_path)

    # Detect faces in both images
    bboxes1, kpss1 = detector.autodetect(image1, max_num=1)
    if bboxes1.shape[0] == 0:
        return -1.0, "Face not found in Image-1"

    # Get the keypoints for alignment
    kps1 = kpss1[0]

    # Extract features using ArcFace model
    feature = rec.get(image1, kps1)
    
    return feature

def weighted_average_feature(features, weights):
    """
    Computes the weighted average of features based on the given weights.

    Args:
        features (list of np.ndarray): List of feature vectors.
        weights (list of float): List of weights corresponding to each feature.
    
    Returns:
        np.ndarray: Weighted average feature vector.
    """
    weighted_features = [f * w for f, w in zip(features, weights)]
    return np.sum(weighted_features, axis=0)

root = 'face_data'
subfolders = [f for f in os.listdir(root) if os.path.isdir(os.path.join(root, f))]

def main():    
    for i in range(len(subfolders)):
        all_features = []
        for num in range(5):
            feature = get_feature(f'{root}/person{i+1}/image_face/{num+1}.jpg')
            np.save(f'{root}/person{i+1}/feature/feature_{num+1}.npy', feature)
            all_features.append(feature)
        
        weights = [0.30, 0.175, 0.175, 0.175, 0.175]  # Weights for the 5 images
        avg_feature = weighted_average_feature(all_features, weights)
        
        np.save(f'{root}/person{i+1}/feature/avg_feature.npy', avg_feature)
        
        np.save(f'feature_data/person{i+1}_feature.npy', avg_feature)
        
        print(f'all features of person{i+1} saved!')
    
    print(f'all features saved!')

if __name__ == '__main__':
    main()