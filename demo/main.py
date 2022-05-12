from turtle import circle
import pandas as pd
import numpy as np
import urllib.request
import cv2
from models.detector import face_detector
from models.verifier.face_verifier import FaceVerifier
from apps import db, login_manager
from apps.authentication.models import Users,Students

def resize_image(im, max_size=768):
    if np.max(im.shape) > max_size:
        ratio = max_size / np.max(im.shape)
        print(f"Resize image to ({str(int(im.shape[1]*ratio))}, {str(int(im.shape[0]*ratio))}).")
        return cv2.resize(im, (0,0), fx=ratio, fy=ratio)
    return im
url="https://scontent.fhan5-9.fna.fbcdn.net/v/t39.30808-1/c0.0.160.160a/p160x160/271153042_1012777712609393_6682807788287512087_n.jpg?_nc_cat=109&ccb=1-5&_nc_sid=7206a8&_nc_ohc=7RG4W2gWhqMAX_vdsgy&_nc_ht=scontent.fhan5-9.fna&oh=00_AT8CwyZohemL_cuoEGi1qhzgstBSUi0smsgFGDfgZiKGeQ&oe=61F69C91"
response = urllib.request.urlopen(url)
image = np.asarray(bytearray(response.read()), dtype="uint8")
im1 = cv2.imdecode(image, cv2.IMREAD_COLOR)
# im1 = cv2.imread(response)[..., ::-1]
url2="https://image.vtc.vn/resize/th/upload/2020/11/11/le-quyen-4-16254478.jpg"
response2 = urllib.request.urlopen(url2)
image2 = np.asarray(bytearray(response2.read()), dtype="uint8")
im2 = cv2.imdecode(image2, cv2.IMREAD_COLOR)
im1 = resize_image(im1)
im2 = resize_image(im2)

fd = face_detector.FaceAlignmentDetector(
        lmd_weights_path="./models/detector/FAN/2DFAN-4_keras.h5"# 2DFAN-4_keras.h5, 2DFAN-1_keras.h5
)
    
# prs.set_detector(fd)
fv = FaceVerifier(classes=512, extractor="facenet")
fv.set_detector(fd)
result1, distance1 = fv.verify(im1, im2, threshold=0.5, with_detection=True, with_alignment=False, return_distance=True)
print(result1)