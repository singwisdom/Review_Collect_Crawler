import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import *

############### 스마트스토어 리뷰 크롤러 ###############################

print("URL을 입력하세요: ")
URL=input()

def GetReview(URL):

    words = []

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()
    # options.add_argument('headless') # 헤드리스
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

    # 스마트스토어 페이지 이동
    driver.get(URL)
    htmlSource = driver.page_source

    
    soup = BeautifulSoup(htmlSource, "lxml")
    time.sleep(uniform(2.0,5.0))

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(uniform(1.5,3.0))

    # 리뷰 페이지로 이동
    driver.find_element_by_xpath("//*[@id='_productTabContainer']/div/div[3]/ul/li[2]").click()
    time.sleep(uniform(1.5,3.0))
  
    soup = BeautifulSoup(htmlSource, "lxml")

    #리뷰 크롤링
    Review_Keywords =driver.find_elements_by_class_name("_3jZQShkMWY")

    # 리뷰들을 리스트에 저장
    for word in Review_Keywords:
        words.append(word.text)

    # # 다음 페이지로 이동
    # driver.find_element_by_class_name("UWN4IvaQza N=a:rvs.page").click()


    driver.quit()
    return words

print(GetReview(URL))
    







    
