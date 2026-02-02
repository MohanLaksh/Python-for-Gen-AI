import streamlit as st
from basic_core import tutor, quiz

st.title("🧠 Mini Smart Study Assistant")

role = st.selectbox("Choose role", ["Tutor", "Quiz"])
topic = st.text_input("Enter topic")

if role == "Tutor":
    level = st.selectbox("Level", ["beginner", "intermediate", "advanced"])
    if st.button("Explain"):
        st.write(tutor(topic, level))

elif role == "Quiz":
    if st.button("Start Quiz"):
        st.write(quiz(topic))
