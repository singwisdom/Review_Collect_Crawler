import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from random import uniform
from tqdm import tqdm
import chromedriver_autoinstaller

############### 스마트스토어 리뷰 크롤러 ###############################

def get_review(URL: str) :    

    review = []
    if "smartstore" in URL: # 입력한 링크에 smartstore이 포함되어있는 경우
        pass
    else :
        print("※ 스마트스토어 페이지가 아닙니다. 다른 URL을 입력해주세요 ※\n")
        return 2

    check_chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0] # 크롬 버전 확인
    
    options = webdriver.ChromeOptions()  # 크롬드라이버 옵션 설정
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        driver = webdriver.Chrome(f'./{check_chrome_ver}/chromedriver.exe', chrome_options=options)
    except Exception as e:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{check_chrome_ver}/chromedriver.exe', chrome_options=options)

    # 대기 설정
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

    # 스마트스토어 페이지 이동
    driver.get(URL)
    htmlSource = driver.page_source
    time.sleep(1.0)

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(1.3)

    try:
        driver.find_element_by_xpath("//*[@id='_productTabContainer']/div/div[3]/ul/li[2]").click()  # 리뷰 페이지로 이동
        time.sleep(uniform(1.0, 1.5))

    except (NoSuchElementException, AttributeError, Exception) as e:
        print("※ 분석할 수 없는 페이지입니다. 다른 URL을 입력해주세요 ※\n")
        return 2

    length=len(driver.find_elements_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a")) # 리뷰 버튼 전체 개수 구하기
    is_next_page_exist=True
    count=1

    while (is_next_page_exist):
        for i in tqdm(range(2, length+1), desc='{} ~ {} 페이지 분석 진행상황'.format(count, count+9)) : # 1페이지 부터 순서대로 수집
            
            try:
                driver.find_element_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[%d]"%i).click()
                time.sleep(uniform(1.0, 1.5))
                count += 1
                if i==12:
                    pass
                    count -= 1
                else :
                    Review_Keywords = driver.find_elements_by_class_name("_3jZQShkMWY") # 리뷰 크롤링
                    # Review_Keywords = soup.select("#REVIEW > div > div > div > div > ul > li > div > div > div > div > div > div > div > div > div > div > button > span")                 
                    [review.append(word.text.replace('\n옵션명 더보기','')) for word in Review_Keywords] # 리뷰들을 리스트에 저장
            except (ElementNotInteractableException, NoSuchElementException, AttributeError, Exception) as e: 
                is_next_page_exist = False # 다음 페이지가 존재하는지 확인
                break
            
    driver.quit() # 드라이버 종료

    return review
