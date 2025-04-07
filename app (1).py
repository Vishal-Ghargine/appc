# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xlek13v6DpmCjRznI8SJW2G736hz_vcL
"""

# car_app.py
pip install scikit-learn
import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# ---------- Styling ----------
st.set_page_config(page_title="Car Evaluation", page_icon="🚗", layout="centered")
st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
    }
    .stApp {
        background-color: #F0F2F6;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Load Data ----------
@st.cache_data
def load_data():
    return pd.read_csv("car.csv")

df = load_data()
df.fillna(df.mode().iloc[0], inplace=True)

# ---------- Encode Data ----------
label_encoders = {}
for col in df.columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# ---------- Train Model ----------
X = df.drop('class', axis=1)
y = df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(multi_class='multinomial', max_iter=1000)
model.fit(X_train, y_train)

# ---------- Sidebar Info ----------
with st.sidebar:
    st.title("🔧 How It Works")
    st.markdown("""
    1. Choose car features below
    2. App will predict the *evaluation score*
    3. Built using *Logistic Regression*
    """)
    st.info("Data: [UCI Car Evaluation Dataset](https://archive.ics.uci.edu/dataset/19/car+evaluation)", icon="📄")

# ---------- App Title ----------
st.title("🚗 Car Evaluation Predictor")
st.caption("Predict the quality of a car based on its attributes")

st.markdown("---")
st.subheader("🧾 Input Car Attributes")

# ---------- Input Form ----------
cols = st.columns(3)
user_input = {}
for i, col in enumerate(X.columns):
    options = label_encoders[col].classes_
    with cols[i % 3]:  # Rotate across 3 columns
        user_input[col] = st.selectbox(f"{col.capitalize()}", options)

# ---------- Prepare Data ----------
input_df = pd.DataFrame([user_input])
for col in input_df.columns:
    input_df[col] = label_encoders[col].transform(input_df[col])

# ---------- Predict ----------
prediction = model.predict(input_df)[0]
predicted_label = label_encoders['class'].inverse_transform([prediction])[0]

# ---------- Display Result ----------
st.markdown("---")
st.subheader("🔮 Prediction Result")
st.success(f"**This car is rated as: {predicted_label.upper()}**", icon="✅")

st.caption("This prediction is based on a logistic regression model trained on the UCI dataset.")