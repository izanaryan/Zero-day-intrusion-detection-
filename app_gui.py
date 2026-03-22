import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image, ImageTk

# load trained model
model = load_model("./zero_day_malware_detection/model/malware_model.h5")

def upload_image():

    file_path = filedialog.askopenfilename()

    if file_path == "":
        return

    # display image
    img_display = Image.open(file_path)
    img_display = img_display.resize((200,200))

    img_tk = ImageTk.PhotoImage(img_display)

    image_label.config(image=img_tk)
    image_label.image = img_tk

    # preprocess image
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    img = cv2.resize(img,(128,128))
    img = img / 255.0
    img = img.reshape(1,128,128,1)

    prediction = model.predict(img)

    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction) * 100

    result_label.config(
        text=f"Predicted Malware Class: {predicted_class}\nConfidence: {confidence:.2f}%"
    )

# create window
window = tk.Tk()
window.title("Zero-Day Malware Detection")
window.geometry("500x450")

title = tk.Label(window,text="Zero-Day Malware Detection System",font=("Arial",16))
title.pack(pady=10)

upload_btn = tk.Button(window,text="Upload Malware Image",command=upload_image)
upload_btn.pack(pady=10)

image_label = tk.Label(window)
image_label.pack(pady=10)

result_label = tk.Label(window,text="Prediction Result")
result_label.pack(pady=20)

window.mainloop()










