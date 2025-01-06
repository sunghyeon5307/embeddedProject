import cv2
import numpy as np
import pygame
from ultralytics import YOLO
from tensorflow.keras.models import load_model
import tkinter as tk
from PIL import Image, ImageTk

face = YOLO("/Users/bagseonghyeon/Documents/embeddedProject/face/yolov8n-face.pt")
emotion = load_model('/Users/bagseonghyeon/Documents/embeddedProject/face/model/my_model4.keras')

def predict_emotion(face_image):
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = cv2.resize(face_image, (48, 48))
    face_image = np.expand_dims(face_image, axis=0)
    face_image = np.expand_dims(face_image, axis=-1)
    face_image = face_image / 255.0
    emotion_pred = emotion.predict(face_image)
    emotion_label = np.argmax(emotion_pred)
    emotions = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
    return emotions[emotion_label]

def recommend_song(emotion):
    recommendations = {
        "angry": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "sad": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "happy": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "neutral": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "surprise": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3"
    }
    return recommendations.get(emotion, "/Users/bagseonghyeon/Documents/embeddedProject/face/song/default_song.mp3")

def play_song(song_path):
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

root = tk.Tk()
root.title("Emotion-Based Music Player")

frame = tk.Frame(root)
frame.pack()

camera_label = tk.Label(frame)
camera_label.grid(row=0, column=0, padx=10, pady=(20, 10))

capture_label = tk.Label(frame)
capture_label.grid(row=0, column=1, padx=10, pady=(20, 10))

capture_button = tk.Button(root, text="버튼", command=lambda: capture_emotion())
capture_button.pack(pady=20)

cap = cv2.VideoCapture(0)
IMG_WIDTH = 700
IMG_HEIGHT = 500

capture_frame = None

def update_camera():
    ret, frame = cap.read()
    if not ret:
        return

    frame_resized = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
    img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk)

    root.after(50, update_camera)

def capture_emotion():
    global capture_frame

    ret, frame = cap.read()
    if not ret:
        return

    frame_resized = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
    results = face(frame_resized)

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        for box in boxes:
            x1, y1, x2, y2 = map(int, box[:4])
            face_img = frame[y1:y2, x1:x2]

            if face_img.size == 0:
                continue

            emotion = predict_emotion(face_img)
            print(f"기분: {emotion}")

            song_path = recommend_song(emotion)
            try:
                play_song(song_path)
                print(f"노랭: {emotion}")
            except pygame.error as e:
                print(f"노래안나옴: {e}")

            cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame_resized, emotion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    capture_frame = frame_resized.copy()
    display_frame = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    display_img = Image.fromarray(display_frame)
    display_imgtk = ImageTk.PhotoImage(image=display_img)
    capture_label.imgtk = display_imgtk
    capture_label.configure(image=display_imgtk)

update_camera()
root.mainloop()
cap.release()
cv2.destroyAllWindows()