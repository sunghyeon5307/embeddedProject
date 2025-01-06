import speech_recognition as sr
import openai
import pyttsx3  # pyttsx3 사용
import os

OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

def speech_to_text():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        print("말하세용")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        print("...")
        text = recognizer.recognize_google(audio, language="ko-KR")
        print("텍스트:", text)
        return text

    except sr.UnknownValueError:
        print("음성을 인식할 수 없어염")
        return None

def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("GPT API 오류:", e)
        return "통신 오류."

def text_to_speech(text):
    engine = pyttsx3.init()  # pyttsx3 초기화
    engine.setProperty("rate", 150)  # 음성 속도 설정
    engine.setProperty("voice", "com.apple.speech.synthesis.voice.kyoko")  # 한국어 여성 목소리 (macOS의 경우)
    engine.say(text)  # 텍스트를 음성으로 변환
    engine.runAndWait()  # 음성 실행$

if __name__ == "__main__":
    print("시작!")
    user_input = speech_to_text()
     
    if user_input:
        print("GPT에게 질문 전달 중...")
        gpt_response = chat_with_gpt(user_input)
        print("GPT의 응답:", gpt_response)
        
        print("응답을 음성으로 출력 중...")
        text_to_speech(gpt_response)