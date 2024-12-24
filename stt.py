import speech_recognition as sr

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

if __name__ == "__main__":
    speech_to_text()