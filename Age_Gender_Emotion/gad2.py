import cv2
import tkinter as tk
from tkinter import filedialog


from deepface import DeepFace
from PIL import Image, ImageTk
from PIL import ImageTk, Image
def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes

def detect_from_image(image_path):
    frame = cv2.imread(image_path)
    process_frame(frame)

def detect_from_Video():
    file_path = filedialog.askopenfilename()
    video = cv2.VideoCapture(file_path)
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break
        process_frame(frame)


def detect_from_webcam():
    video = cv2.VideoCapture(0)
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break
        process_frame(frame)

def process_frame(frame):
    resultImg, faceBoxes = highlightFace(faceNet, frame)
    padding = 20
    correction_factor = 5  # Offset correction for age underestimation
    if not faceBoxes:
        print("No face detected")
    for faceBox in faceBoxes:
        face = frame[max(0, faceBox[1] - padding): min(faceBox[3] + padding, frame.shape[0] - 1),
                     max(0, faceBox[0] - padding): min(faceBox[2] + padding, frame.shape[1] - 1)]

        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]

        ageNet.setInput(blob)
        agePreds = ageNet.forward()

        # Improved weighted age calculation
        weighted_age = sum([
            ((int(ageList[i].split('-')[0].replace('(', '')) + int(ageList[i].split('-')[1].replace(')', ''))) / 2) * float(agePreds[0][i])
            for i in range(len(ageList))
        ])
        corrected_age = weighted_age + correction_factor
        age_label = f"{corrected_age:.1f} years"

        try:
            analysis = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
        except:
            emotion = "Unknown"

        print(f'Gender: {gender}, Age: {age_label}, Emotion: {emotion}')

        cv2.putText(resultImg, f'{gender}, {age_label}, {emotion}', (faceBox[0], faceBox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Detection Result", resultImg)

# Initialize models
faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
ageProto = "age_deploy.prototxt"
ageModel = "age_net.caffemodel"
genderProto = "gender_deploy.prototxt"
genderModel = "gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

# Create UI
root = tk.Tk()
root.geometry('1200x800')
root.title("Face Detection with Emotion Recognition")
img= tk.PhotoImage(file='bg.png', master=root)
img_label= tk.Label(root,image=img)
img_label.place(x=0, y=0)
def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        detect_from_image(file_path)

browse_button = tk.Button(root, text="Browse Image", command=browse_file)
browse_button.pack(pady=10)

webcam_button = tk.Button(root, text="Live Detection", command=detect_from_webcam)
webcam_button.pack(pady=10)

Video_button = tk.Button(root, text="Video Detection", command=detect_from_Video)
Video_button.pack(pady=10)

root.mainloop()
