import cv2
import numpy as np
import pygame
from ultralytics import YOLO
from tensorflow.keras.models import load_model
import socket
import serial  # STM32 UART 통신을 위한 라이브러리 추가

# 모델 로딩
face = YOLO("/Users/bagseonghyeon/Documents/embeddedProject/face/yolov8n-face.pt")
emotion = load_model('/Users/bagseonghyeon/Documents/embeddedProject/face/model/my_model2.keras')

# UDP 설정 (Unity와의 통신 유지)
UDP_IP = "0.0.0.0"
UDP_PORT = 5009
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sock.settimeout(0.5)

# STM32 UART 설정 (예시: COM 포트와 보레이트를 설정)
uart = serial.Serial('/dev/ttyUSB0', 115200)  # UART 포트와 보레이트를 수정해 주세요.

def predict_emotion(face_image):
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
    face_image = cv2.resize(face_image, (48, 48))
    face_image = np.expand_dims(face_image, axis=0)
    face_image = np.expand_dims(face_image, axis=-1)
    face_image = face_image / 255.0
    emotion_pred = emotion.predict(face_image)
    emotion_label = np.argmax(emotion_pred)
    emotions =  ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]
    return emotions[emotion_label]

def recommend_song(emotion):
    songs = {
        "angry": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "sad": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "happy": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "neutral": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3",
        "surprise": "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3"
    }
    return songs.get(emotion, "/Users/bagseonghyeon/Documents/embeddedProject/face/song/lyrics.mp3")

def play_song(song_path):
    pygame.mixer.init()
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

def send_emotion_to_uart(emotion):
    emotion_map = {
        "happy": 1,
        "sad": 2,
        "angry": 3,
        "neutral": 0,
        "surprise": 4,
        "disgust": 5,
        "fear": 6
    }
    
    emotion_value = emotion_map.get(emotion, -1)  # 감정에 해당하는 숫자 값을 얻음, 기본값은 -1 (알 수 없는 감정)
    uart.write(f"{emotion_value}\n".encode())  # 숫자 값을 UART로 전송

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        data, addr = sock.recvfrom(1024)
        if data.decode('utf-8') == "1":
            results = face(frame)
            for result in results:
                boxes = result.boxes.xyxy.cpu().numpy()
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box[:4])
                    face_img = frame[y1:y2, x1:x2]
                    if face_img.size == 0:
                        continue
                    emotion_label = predict_emotion(face_img)
                    print(f"Detected emotion: {emotion_label}")

                    song_path = recommend_song(emotion_label)
                    try:
                        play_song(song_path)
                        print(f"Playing song: {song_path}")
                    except pygame.error as e:
                        print(f"Error playing song: {e}")

                    # UART로 감정 전송
                    send_emotion_to_uart(emotion_label)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, emotion_label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    except socket.timeout:
        continue

    cv2.imshow("cam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
uart.close()  # UART 종료