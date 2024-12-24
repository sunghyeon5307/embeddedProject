import time 
import urllib.request 
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

search = "angry" 
count = 10      
save_dir = "/Users/bagseonghyeon/Documents/융합프로젝트/angry"

chrome_driver = webdriver.Chrome()
driver = chrome_driver
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&ogbl") 

elem = driver.find_element(By.NAME, "q") 
elem.send_keys(search)
elem.send_keys(Keys.RETURN) 

SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()  # '더보기' 버튼 클릭하여 추가 이미지 로드
        except:
            break
    last_height = new_height

images = driver.find_elements(By.CSS_SELECTOR, "YQ4gaf")

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

for i, image in enumerate(images[:count], 1):
    try: 
        image.click()  # 이미지 클릭하여 확대
        time.sleep(2)  # 이미지를 클릭하고 2초 대기 (이미지가 로드될 시간)
        
        img_element = driver.find_element(By.CSS_SELECTOR,".sFlh5c.pT0Scc.iPVvYb")  # 이미지 URL이 담긴 element 찾기
        imgUrl = img_element.get_attribute("src")  # 이미지 URL 가져오기
        
        # URL이 제대로 가져와졌는지 확인
        if imgUrl:
            filename = os.path.join(save_dir, f"{search}_{i}.jpg")  # 이미지 저장 경로 설정
            urllib.request.urlretrieve(imgUrl, filename)  # 이미지 다운로드
            print(f"{i}번 이미지 다운로드 완료")
        else:
            print(f"{i}번 이미지 URL을 가져올 수 없습니다.")
        
    except Exception as e:
        print(f"{i}번 이미지 다운로드 실패:", e)

driver.quit()