import tkinter as tk
from tkinter import filedialog, Label, Button
import cv2
import numpy as np
from PIL import Image, ImageTk

# Load pre-trained models (replace with your own model paths or methods)
def load_models():
    # Placeholder for loading age, gender, and emotion models
    age_model = None  # Load age detection model
    gender_model = None  # Load gender detection model
    emotion_model = None  # Load emotion detection model
    return age_model, gender_model, emotion_model

# Placeholder function to predict age, gender, and emotion
def predict_age_gender_emotion(image):
    # Dummy data for illustration, replace with actual model inference
    age = "25-30"
    gender = "Male"
    emotion = "Happy"
    return age, gender, emotion

class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Age, Gender, and Emotion Detection")
        self.image_path = None

        # UI elements
        self.browse_button = Button(root, text="Browse Image", command=self.browse_image)
        self.browse_button.pack()

        self.image_label = Label(root)
        self.image_label.pack()

        self.predict_button = Button(root, text="Predict", command=self.predict_result)
        self.predict_button.pack()

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if self.image_path:
            image = Image.open(self.image_path)
            image = image.resize((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def predict_result(self):
        if self.image_path:
            # Load the image using OpenCV
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Perform predictions (replace this with actual model predictions)
            age, gender, emotion = predict_age_gender_emotion(image)

            # Overlay results on the image
            cv2.putText(image, f"Age: {age}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(image, f"Gender: {gender}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(image, f"Emotion: {emotion}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Convert OpenCV image to PIL Image for displaying in Tkinter
            image = Image.fromarray(image)
            image = image.resize((300, 300))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
