# Deep Learning Prototype for WZT-Based Early Depression Prediction

이 프로젝트는 Kim et al. (2025)의 연구인  
*Predicting Early Depression in WZT Drawing Images Based on Deep Learning*을 참고하여 구현한 연구형 프로토타입입니다.

본 프로젝트는 실제 의료 진단 모델이 아니라, WZT 그림 기반 딥러닝 분석 파이프라인을 실험적으로 재구성하고 검증하기 위한 synthetic prototype입니다.

---

## Project Objective

실제 WZT 기반 우울 데이터는 개인정보 및 윤리 문제로 인해 공개 접근이 어렵다.  
따라서 본 프로젝트는 실제 임상 진단 성능을 목표로 하지 않으며, 논문 기반 이미지 분석 구조를 구현하고 실험적으로 검증하는 것을 목표로 한다.

본 프로젝트에서는 다음 내용을 중심으로 구현하였다.

1. WZT stimulus 기반 synthetic drawing dataset 생성
2. CNN-SoftMax 기반 이미지 분류 모델 구현
3. Hinge-loss 기반 CNN classifier 비교 실험
4. Grad-CAM 기반 시각적 해석 가능성 분석
5. Noise, blur, incomplete drawing, class overlap 등을 포함한 psychological ambiguity 반영

---

## Dataset Construction

Synthetic WZT dataset은 rule-based 방식으로 생성하였다.

각 이미지에는 다음과 같은 variability를 포함하였다.

- stroke thickness variation
- incomplete drawing
- broken line pattern
- Gaussian blur
- hand-drawing noise
- paper texture noise
- rotation / scaling augmentation
- class overlap
- label noise

이를 통해 실제 psychological drawing dataset에서 나타날 수 있는 ambiguity와 individual variability를 일부 반영하고자 하였다.

---

## Experimental Result

| Model | Accuracy |
|---|---|
| CNN + SoftMax | 0.87 |
| CNN + Hinge Loss | Under Evaluation |

Synthetic dataset 기준으로 CNN-SoftMax 모델은 약 87%의 test accuracy를 보였다.

Confusion matrix 기준으로 depressed / non-depressed 클래스 간 일부 overlap이 발생하도록 구성하였으며, 이는 실제 psychological data의 ambiguity를 반영하기 위한 목적이다.

다만 본 결과는 실제 임상 성능이 아니라, synthetic WZT dataset 상에서의 방법론 검증 결과로 해석해야 한다.

---

## Project Structure

```text
src/
 ├── 01_generate_wzt_dataset.py
 ├── 02_train_cnn.py
 └── 03_evaluate_and_gradcam.py

data/
 └── synthetic_wzt/

results_softmax/
 ├── model.keras
 ├── history.csv
 ├── classification_report.json
 ├── confusion_matrix.csv
 └── gradcam/

results_hinge/