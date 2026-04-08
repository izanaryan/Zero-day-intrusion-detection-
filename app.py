import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image

# load trained model
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "malware_model.h5")

model = load_model(MODEL_PATH)

st.title("Zero-Day Malware Detection System")

st.write("Upload a malware image to detect its family.")

uploaded_file = st.file_uploader("Upload Malware Image", type=["png","jpg"])
class_names = [
"Adialer.C","Agent.FYI","Allaple.A","Allaple.L","Alueron.gen!J","Autorun.K",
"C2LOP.gen!g","C2LOP.P","Dialplatform.B","Dontovo.A","Fakerean","Instantaccess",
"Lolyda.AA1","Lolyda.AA2","Lolyda.AA3","Lolyda.AT","Malex.gen!J","Obfuscator.AD",
"Rbot!gen","Skintrim.N","Swizzor.gen!E","Swizzor.gen!I","VB.AT","Wintrim.BX","Yuner.A"
]

if uploaded_file is not None:

    image = Image.open(uploaded_file).convert("L")
    img = np.array(image)

    img = cv2.resize(img,(128,128))
    img = img / 255.0
    img = img.reshape(1,128,128,1)

    prediction = model.predict(img)

    predicted_class = np.argmax(prediction)

    st.image(uploaded_file, caption="Uploaded Malware Image", use_column_width=True)

    confidence = np.max(prediction) * 100
    malware_name = class_names[predicted_class]

    st.success(f"Detected Malware: {malware_name}")
    st.info(f"Confidence: {confidence:.2f}%")
    st.progress(int(confidence))
