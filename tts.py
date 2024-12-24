from gtts import gTTS
import os

def text_to_speech(text, lang="ko"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)

        tts.save("output.mp3")
        print("TTS 생성 완료! 'output.mp3' 파일이 저장되었습니다.")
        
        os.system("afplay output.mp3")  
        
    except Exception as e:
        print(f"TTS 생성 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    text = input("변환할 텍스트를 입력하세요: ")
    text_to_speech(text)