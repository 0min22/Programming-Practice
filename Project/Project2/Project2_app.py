import streamlit as st
import pandas as pd
import joblib

# 모델 불러오기
model = joblib.load("models/random_forest_model.pkl")

st.title("전자상거래 구매 확률 예측 시스템")

st.write("사용자 정보와 상품 정보를 입력하면 구매 확률을 예측합니다.")

# 입력값
click = st.selectbox("광고 클릭 여부", [0, 1])

user_age = st.number_input(
    "나이",
    min_value=10,
    max_value=100,
    value=25
)

product_price = st.number_input(
    "상품 가격",
    min_value=0,
    value=50000
)

product_rating = st.slider(
    "상품 평점",
    min_value=0.0,
    max_value=5.0,
    value=4.0,
    step=0.1
)

time_on_page = st.number_input(
    "페이지 체류 시간",
    min_value=0.0,
    value=30.0
)

product_type = st.selectbox(
    "상품 종류",
    ["Books", "Clothing", "Electronics"]
)

user_gender = st.selectbox(
    "성별",
    ["Male", "Female"]
)

user_location = st.selectbox(
    "지역",
    ["Urban", "Suburban", "Rural"]
)

# 예측 버튼
if st.button("구매 확률 예측"):

    input_df = pd.DataFrame(
        {
            "click": [click],
            "user_age": [user_age],
            "product_price": [product_price],
            "product_rating": [product_rating],
            "time_on_page": [time_on_page],
            "product_type": [product_type],
            "user_gender": [user_gender],
            "user_location": [user_location]
        }
    )

    input_df = pd.get_dummies(input_df)

    # 모델 학습 당시 컬럼과 맞추기
    model_columns = model.feature_names_in_

    input_df = input_df.reindex(
        columns=model_columns,
        fill_value=0
    )

    probability = model.predict_proba(input_df)[:, 1][0]

    st.subheader("예상 구매 확률")
    st.write(f"{probability * 100:.2f}%")

    if probability >= 0.45:
        st.success("추천 대상 사용자입니다.")
    else:
        st.warning("구매 가능성이 낮은 사용자입니다.")