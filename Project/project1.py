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

import pandas as pd

def extract_features(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # resize
    img = cv2.resize(img, (128, 128))

    # binary (흑백)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # black pixel 비율
    black_pixel_ratio = np.sum(thresh == 255) / (128*128)

    # edge
    edges = cv2.Canny(img, 50, 150)
    edge_ratio = np.sum(edges > 0) / (128*128)

    # 중심
    coords = np.column_stack(np.where(thresh == 255))
    if len(coords) > 0:
        center_y, center_x = np.mean(coords, axis=0)
        center_x /= 128
        center_y /= 128
    else:
        center_x, center_y = 0, 0

    # contour 개수
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_count = len(contours)

    return [black_pixel_ratio, edge_ratio, center_x, center_y, contour_count]

data = []
labels = []

for label in ["class_0", "class_1"]:
    folder = base_path + "/" + label
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        features = extract_features(path)
        data.append(features)
        labels.append(0 if label == "class_0" else 1)

# DataFrame
df = pd.DataFrame(data, columns=[
    "black_ratio", "edge_ratio", "center_x", "center_y", "contour_count"
])
df["label"] = labels

print(df.head())

from sklearn.model_selection import train_test_split

X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1:", f1_score(y_test, y_pred))

from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

importances = model.feature_importances_

for name, val in zip(X.columns, importances):
    print(name, ":", val)
