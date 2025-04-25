import streamlit as st
from fastai.vision.all import *
from PIL import Image
import os
import pathlib
import platform

if platform.system() == 'Windows':
    pathlib.PosixPath = pathlib.WindowsPath


st.title("🩺 Pneumoniya aniqlovchi AI model")


file = st.file_uploader("Rasmni yuklang (JPG yoki JPEG formatda)", type=["jpg", "jpeg"])


@st.cache_resource
def load_model():
    learn = load_learner("pneumonia_classifier.pkl")
    return learn

model = load_model()



if file is not None:
    img = Image.open(file).convert("RGB")
    st.image(img, caption="Yuklangan rasm")

    if st.button("🔍 Bashorat qilish"):
        pred, pred_idx, probs = model.predict(PILImage.create(img))
        st.markdown(f"### 🧠 Natija: **{pred}**")
        st.markdown(f"**Ishonchlilik darajasi:** {probs[pred_idx] * 100:.2f} %")

        if str(pred) == "PNEUMONIA":
            st.error("⚠️ Pneumoniya aniqlandi. Shifokorga murojaat qilish tavsiya etiladi!")
        else:
            st.success("✅ Pneumoniya aniqlanmadi. Hammasi joyida.")