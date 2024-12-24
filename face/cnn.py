import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# 이미지 전처리 및 증강
train_datagen = ImageDataGenerator(
    rescale=1./255,            # 픽셀 값을 0과 1 사이로 정규화
    rotation_range=30,         # 회전
    width_shift_range=0.2,     # 수평 이동
    height_shift_range=0.2,    # 수직 이동
    shear_range=0.2,           # 기울기 변환
    zoom_range=0.2,            # 확대/축소
    horizontal_flip=True,      # 수평 반전
    fill_mode='nearest'        # 채워지지 않은 부분을 채우는 방식
)

test_datagen = ImageDataGenerator(rescale=1./255)  # 테스트 데이터는 정규화만 진행

# 훈련 데이터 로드
train_generator = train_datagen.flow_from_directory(
    '/Users/bagseonghyeon/Documents/융합프로젝트/face/dataset/train',  # 훈련 데이터가 있는 폴더
    target_size=(48, 48),  # 이미지 크기
    batch_size=32,
    class_mode='categorical',  # 원핫 인코딩
    classes=['angry', 'sad', 'happy', 'neutral']  # 4개의 감정만 지정
)

# 테스트 데이터 로드
test_generator = test_datagen.flow_from_directory(
    '/Users/bagseonghyeon/Documents/융합프로젝트/face/dataset/test',  # 테스트 데이터가 있는 폴더
    target_size=(48, 48),  # 이미지 크기
    batch_size=32,
    class_mode='categorical',  # 원핫 인코딩
    classes=['angry', 'sad', 'happy', 'neutral']  # 4개의 감정만 지정
)

# CNN 모델 설계
model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(48, 48, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(4, activation='softmax'))  # 4개의 감정 클래스 (화남, 슬픔, 기쁨, 무표정)

# 모델 컴파일
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# 모델 학습
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=50,
    validation_data=test_generator,
    validation_steps=test_generator.samples // test_generator.batch_size
)

# 모델 저장
model.save('emotion_model_4class.h5')