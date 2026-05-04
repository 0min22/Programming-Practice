import cv2
import numpy as np
import os
import random

# 저장 경로
base_path = "/content/wzt_data"
os.makedirs(base_path + "/class_0", exist_ok=True)
os.makedirs(base_path + "/class_1", exist_ok=True)

# 8칸 WZT 틀 생성
def create_wzt_template():
    img = np.ones((256, 256), dtype=np.uint8) * 255
    
    # 8칸 나누기
    for i in range(1, 4):
        cv2.line(img, (0, i*64), (256, i*64), 0, 1)
    for j in range(1, 4):
        cv2.line(img, (j*64, 0), (j*64, 256), 0, 1)
    
    return img

# class_0: 안정된 그림
def draw_stable(img):
    for _ in range(random.randint(3,6)):
        x1, y1 = random.randint(0,255), random.randint(0,255)
        x2, y2 = random.randint(0,255), random.randint(0,255)
        cv2.line(img, (x1,y1), (x2,y2), 0, 2)
    return img

# class_1: 불안정/왜곡된 그림
def draw_distorted(img):
    for _ in range(random.randint(8,15)):
        x1, y1 = random.randint(0,255), random.randint(0,255)
        x2, y2 = random.randint(0,255), random.randint(0,255)
        thickness = random.choice([1,2,3])
        cv2.line(img, (x1,y1), (x2,y2), 0, thickness)
    return img

# 데이터 생성
def generate_data(n=50):
    for i in range(n):
        # class 0
        img0 = create_wzt_template()
        img0 = draw_stable(img0)
        cv2.imwrite(f"{base_path}/class_0/img_{i}.png", img0)

        # class 1
        img1 = create_wzt_template()
        img1 = draw_distorted(img1)
        cv2.imwrite(f"{base_path}/class_1/img_{i}.png", img1)

generate_data(50)
print("데이터 생성 완료")