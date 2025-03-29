import json
import numpy as np
import cv2 as cv
from skimage.measure import ransac
from skimage.transform import AffineTransform

def load_minutiae_from_json(file_path):
    """Đọc danh sách minutiae từ file JSON"""
    with open(file_path, "r") as f:
        return json.load(f)

def fingerprint_matching_ransac(minutiae1, minutiae2):
    """ So khớp hai danh sách minutiae bằng RANSAC """
    
    # Chuyển đổi danh sách minutiae thành numpy array
    keypoints1 = np.array([[m["x"], m["y"]] for m in minutiae1 if "x" in m and "y" in m])
    keypoints2 = np.array([[m["x"], m["y"]] for m in minutiae2 if "x" in m and "y" in m])

    num_matches = min(len(keypoints1), len(keypoints2))
    keypoints1 = keypoints1[:num_matches]
    keypoints2 = keypoints2[:num_matches]

    if len(keypoints1) < 3 or len(keypoints2) < 3:
        return 0  # Không đủ điểm để khớp

    # Áp dụng RANSAC
    model, inliers = ransac((keypoints1, keypoints2),
                             AffineTransform, min_samples=3,
                             residual_threshold=10, max_trials=1000)
    
    return np.sum(inliers) if inliers is not None else 0
