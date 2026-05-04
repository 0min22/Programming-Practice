# WZT 기반 Drawing Classification: Feature-based Preliminary Study

## 1. 서론

Wartegg Zeichentest (WZT)는 그림을 기반으로 인지 상태를 평가하는 검사로, 최근에는 이를 활용한 early-stage dementia prediction 연구가 진행되고 있다. 기존 연구에서는 Convolutional Neural Network (CNN)을 사용하여 WZT 이미지로부터 시각적 특징을 자동으로 학습하고 분류를 수행한다.

본 연구는 이러한 접근 이전 단계에서 다음 질문을 다룬다.

> WZT와 유사한 그림 데이터 자체에 분류 가능한 시각적 패턴이 존재하는가?

이를 위해 CNN을 직접 적용하기보다, handcrafted feature와 classical machine learning을 활용하여 해당 가정을 검증하였다.

---

## 2. 문제 정의

입력 이미지 \( I \)에 대해, 다음을 확인하는 것을 목표로 한다.

- 이미지 내에 의미 있는 시각적 구조가 존재하는가  
- 이러한 구조가 명시적 feature로 표현 가능한가  
- 해당 feature를 통해 분류가 가능한가  

본 문제는 binary classification 형태로 설정하였다.

---

## 3. 데이터셋 구성

공개된 WZT 데이터셋이 존재하지 않기 때문에, WZT 형식을 참고한 synthetic dataset을 생성하였다.

- 4×4 grid 구조의 drawing image 생성  
- 두 클래스 정의:
  - Class 0: 상대적으로 균형 잡힌 공간 분포  
  - Class 1: 더 높은 fragmentation, spatial imbalance, noise 포함  

데이터 난이도를 높이기 위해 다음 요소를 포함하였다.

- class 간 feature overlap  
- broken stroke  
- random noise  
- blur, erosion, dilation  

이로 인해 단순 규칙 기반 분류가 어려운 환경을 구성하였다.

---

## 4. Feature Extraction

이미지를 직접 입력으로 사용하는 대신, 다음과 같은 handcrafted feature를 추출하였다.

- pixel density: `black_ratio`  
- edge structure: `edge_ratio`  
- spatial distribution: `center_x`, `center_y`  
- structural complexity: `contour_count`  
- shape properties: `bbox_area`, `aspect_ratio`  
- density variation: `horizontal_density_std`, `vertical_density_std`  
- grid-based distribution: `cell_occupancy_count`, `cell_density_std`  
- symmetry: `symmetry_score`  

이러한 feature들은 이미지의 구조적 특성을 정량적으로 표현한다.

---

## 5. 실험 설정

다음 모델을 비교하였다.

- K-Nearest Neighbors (KNN)  
- Decision Tree  
- Random Forest  
- Support Vector Machine (SVM)  
- Logistic Regression  

평가 지표는 Accuracy, Precision, Recall, F1-score를 사용하였다.

---

## 6. 결과

### 6.1 모델 성능

SVM이 가장 높은 성능을 보였으며, 이는 feature 공간에서 비선형 경계가 형성되어 있음을 시사한다.  
반면 Decision Tree는 상대적으로 낮은 성능을 보였으며, 이는 복잡한 패턴을 안정적으로 분할하지 못한 결과로 해석된다.

### 6.2 Feature Importance

Random Forest 기반 분석 결과, 다음 feature들이 높은 중요도를 보였다.

- `edge_ratio`  
- `cell_density_std`  
- `mean_intensity`  
- `symmetry_score`  

이는 단순한 선의 개수보다, 구조적 분포와 형태적 특성이 분류에 더 중요한 역할을 함을 의미한다.

### 6.3 Ablation Study

feature 그룹별 성능 비교 결과:

- 단일 feature 그룹만으로는 충분한 성능 확보가 어려움  
- 다양한 feature를 결합할 때 성능이 향상됨  

이는 WZT-like 이미지 분류가 다차원적 시각 정보를 요구함을 보여준다.

---

## 7. 논문과의 관계

기존 연구:

WZT image → CNN → prediction

본 연구:

WZT-like image → handcrafted feature → classical ML → classification

본 프로젝트는 기존 연구를 재현하는 것이 아니라, 다음 가정을 검증한다.

> WZT 이미지에는 학습 가능한 시각적 패턴이 존재한다

이를 통해 CNN이 이러한 패턴을 자동으로 학습할 수 있다는 점을 간접적으로 뒷받침한다.

---

## 8. 한계

- synthetic dataset 사용  
- 실제 임상 데이터와의 차이  
- 의료적 해석 불가능  
- handcrafted feature의 표현력 제한  

---

## 9. 향후 연구

- CNN 기반 end-to-end 학습 적용  
- 실제 WZT 데이터셋 확보 및 검증  
- Grad-CAM을 통한 feature 해석  
- CNN과 feature-based 접근 비교  

---

## 10. 결론

본 연구는 WZT-like drawing 이미지에서 분류 가능한 시각적 패턴이 존재함을 확인하였다.  
또한 이러한 패턴은 handcrafted feature를 통해 일정 수준까지 표현 가능하며, classical machine learning 모델을 통해 분류가 가능함을 보였다.

이는 WZT 이미지 기반 classification 접근의 기초적인 가능성을 확인하는 preliminary study로 볼 수 있다.