import cv2
import numpy as np
from ultralytics import YOLO
from tensorflow.keras.models import load_model

yolo_model = YOLO("/Users/bagseonghyeon/Documents/융합프로젝트/face/yolov8n-face.pt")

emotion_model = load_model('/Users/bagseonghyeon/Documents/융합프로젝트/face/model/emotion_model2 (2).keras')

def predict_emotion(face_image):
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)  
    face_image = cv2.resize(face_image, (48, 48))  
    face_image = np.expand_dims(face_image, axis=0)  
    face_image = np.expand_dims(face_image, axis=-1)  
    face_image = face_image / 255.0 
    emotion_pred = emotion_model.predict(face_image)
    emotion_label = np.argmax(emotion_pred)
    emotions = ['anger', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
    return emotions[emotion_label]

image_path = "/Users/bagseonghyeon/Documents/융합프로젝트/face/image copy.png"
frame = cv2.imread(image_path)
if frame is None:
    exit()

results = yolo_model(frame)

for result in results:
    boxes = result.boxes.xyxy.cpu().numpy()
    for box in boxes:
        x1, y1, x2, y2 = map(int, box[:4])
        face_img = frame[y1:y2, x1:x2]

        if face_img.size == 0:
            continue

        emotion = predict_emotion(face_img)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, emotion, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        print(f"Detected Emotion: {emotion}")

cv2.imshow("Emotion Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

output_path = "/path/to/your/output_image.jpg"
cv2.imwrite(output_path, frame)
print(f"결과 이미지 저장: {output_path}")