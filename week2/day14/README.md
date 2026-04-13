# Mini Data Analysis Project

## 목적
CSV 데이터를 읽고, 전처리하고, 시각화하는 기본 흐름을 익힌다.

## 구조
day14/
- data.csv
- analysis.py
- README.md

## 사용 기술
- Python
- pandas
- matplotlib

## 과정
1. CSV 파일을 pandas로 읽기
2. 결측치 확인 (isnull().sum())
3. 조건 필터링 (age >= 21)
4. 시각화
   - score: 히스토그램
   - age: 막대그래프

## 결과
- score 값의 분포 확인
- age별 데이터 개수 확인

## 배운 점
- 데이터를 직접 다루고 확인하는 과정이 중요함
- 전처리와 시각화를 통해 데이터를 이해할 수 있음

## 다음 단계
- 더 큰 데이터셋 적용
- 머신러닝 모델로 확장