import os
import speech_recognition as sr
import openai
from gtts import gTTS
import pygame

openai.api_key = "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"

def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        print("말하세여")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)

        print("...")
        text = recognizer.recognize_google(audio, language="ko-KR")
        print("텍스트:", text)
        return text

    except sr.UnknownValueError:
        print("인식 실패")
        return None
    except sr.RequestError as e:
        return None

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("api 오류:", e)
        return "통신 실패"

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang='ko')
        tts.save("output.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("output.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
        os.remove("output.mp3")
    except Exception as e:
        print("오류:", e)

if __name__ == "__main__":
    print("시작")
    user_input = speech_to_text()

    if user_input:
        print("질문 전달 중!!!")
        gpt_response = chat_with_gpt(user_input)
        print("GPT 응답:", gpt_response)

        print("음성으로 출력 중...")
        text_to_speech(gpt_response)
    else:
        print("음성 출력 실패")