import time
import openpyxl
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from random import uniform
from tqdm import tqdm

############### 스마트스토어 리뷰 크롤러 ###############################

wb = openpyxl.Workbook() # 워크북 생성
sheet=wb.active # Sheet 활성
wb.title ="리뷰 크롤러" # Sheet 이름 설정
sheet.append(["옵션", "카운트"])  # 데이터 프레임 내 변수명 생성

def get_review(URL: str) :    
    review = []

    if "smartstore" in URL: # 입력한 링크에 smartstore이 포함되어있는 경우
        pass
    else :
        print("※ 스마트스토어 페이지가 아닙니다. 다른 URL을 입력해주세요 ※")
        return 2

    # 크롬드라이버 옵션 설정
    options = webdriver.ChromeOptions()
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
    time.sleep(uniform(1.0, 2.0))

    # 스크롤 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
    time.sleep(uniform(1.5, 2.0))

    try:
        driver.find_element_by_xpath("//*[@id='_productTabContainer']/div/div[3]/ul/li[2]").click()  # 리뷰 페이지로 이동
        time.sleep(uniform(1.5, 2.0))

    except NoSuchElementException or AttributeError or Exception as e:
        print("※ 분석할 수 없는 페이지입니다. 다른 URL을 입력해주세요 ※")
        return 2

    length=len(driver.find_elements_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a")) # 리뷰 버튼 전체 개수 구하기
    is_next_page_exist=True
    count=1

    while (is_next_page_exist):
        for i in tqdm(range(2, length+1), desc='{} ~ {} 페이지 분석 진행상황'.format(count, count+9)) : # 1페이지 부터 순서대로 수집
            try:
                driver.find_element_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[%d]"%i).click()
                time.sleep(uniform(1.0, 1.5))
                soup = BeautifulSoup(htmlSource, "lxml")
                time.sleep(uniform(1.0, 2.0))
                if i==12:
                    pass
                else :
                    Review_Keywords = driver.find_elements_by_class_name("_3jZQShkMWY") # 리뷰 크롤링                       
                    [review.append(word.text) for word in Review_Keywords] # 리뷰들을 리스트에 저장
            except ElementNotInteractableException or NoSuchElementException or AttributeError or Exception as e: 
                is_next_page_exist = False #다음 페이지가 존재하는지 확인
                break
            count += 10
    driver.quit() # 드라이버 종료

    #리뷰 카운트 및 정렬
    get_count={}
    for i in review:
        try: get_count[i] +=1
        except: get_count[i]=1

    sort_dict = sorted(get_count.items(), key=lambda x:x[1], reverse=True) # value 값 기준으로 다시 정렬
    [sheet.append([sort_dict[i][0],sort_dict[i][1]]) for i in tqdm(range(0, len(sort_dict)), desc="모든 리뷰 분석 진행상황")]  # 엑셀에 저장

    wb.save("리뷰 분석.xlsx")  # 엑셀 파일로 저장
    print("\n>> 모든 작업이 끝났습니다. 엑셀파일로 변환됩니다. <<")
