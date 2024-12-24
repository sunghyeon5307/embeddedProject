import speech_recognition as sr
from gtts import gTTS
import os
import platform

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
    except sr.RequestError as e:
        print(f"STT 서비스에 연결할 수 없어염: {e}")
        return None

def text_to_speech(text, lang="ko"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)

        tts.save("output.mp3")
        print("완료!")

        if platform.system() == "Darwin":  
            os.system("afplay output.mp3")
                    
    except Exception as e:
        print(f"인식불가 {e}")

if __name__ == "__main__":
    stt_text = speech_to_text()
    
    if stt_text:
        text_to_speech(stt_text)
