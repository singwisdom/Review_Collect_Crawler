import time
from sys import exit
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import uniform
import openpyxl

############### 스마트스토어 리뷰 크롤러 ###############################

# 워크북 생성
wb = openpyxl.Workbook()

# Sheet 활성
sheet=wb.active

# Sheet 이름 설정
wb.title ="리뷰 크롤러"

# 데이터 프레임 내 변수명 생성
sheet.append(["옵션","카운트"])

# URL을 입력받음
print("URL을 입력하세요: ")
URL=input()

review = []

# 크롬드라이버 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")

driver = webdriver.Chrome("chromedriver", chrome_options=options)

# 대기 설정
wait = WebDriverWait(driver, 3)
visible = EC.visibility_of_element_located  # DOM에 나타남, 웹에 보여야 조건 만족

is_smartstore = "smartstore"

if is_smartstore in URL: # 입력한 링크에 smartstore이 포함되어있는 경우
    pass
else :
    print("스마트스토어 페이지가 아닙니다. 다른 URL을 입력해주세요")
    exit()


# 스마트스토어 페이지 이동
driver.get(URL)
htmlSource = driver.page_source

soup = BeautifulSoup(htmlSource, "lxml")
time.sleep(uniform(1.0,2.0))

# 스크롤 내리기
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
time.sleep(uniform(1.5,3.0))

try:
    driver.find_element_by_xpath("//*[@id='_productTabContainer']/div/div[3]/ul/li[2]").click()     # 리뷰 페이지로 이동
    time.sleep(uniform(1.5,2.0))
except:
    print("다른 URL을 입력해주세요")
    exit()

length=len(driver.find_elements_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a")) # 리뷰 버튼 전체 개수 구하기

is_next_page_exist=True # 다음 페이지가 있는지 없는지 확인 하는 변수

# 리뷰 개수에 따라 다음페이지가 있는 경우와 없는 경우를 구분

if(length<12): # 다음페이지가 있는 경우
    
    for i in range(2,length):

        driver.find_element_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[%d]"%i).click()  # 다음 페이지로 이동

        soup = BeautifulSoup(htmlSource, "lxml")
        time.sleep(uniform(1.0,3.0))

        Review_Keywords =driver.find_elements_by_class_name("_3jZQShkMWY")  #리뷰 크롤링

        [review.append(word.text) for word in Review_Keywords]    # 리뷰들을 리스트에 저장

else: # 다음페이지가 없는 경우

    while is_next_page_exist:
        for i in range(2,length+1):
            if i==12:
                # 다음 페이지로 이동
                try:
                    driver.find_element_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[%d]"%i).click()
                except: 
                # 다음 페이지가 존재하는지 확인
                    is_next_page_exist = False
                    break

                time.sleep(uniform(1.0, 2.0))
                soup = BeautifulSoup(htmlSource, "lxml")
                time.sleep(uniform(1.0, 2.0))
            else:
                # 다음 페이지로 이동
                try:
                    driver.find_element_by_xpath("//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[%d]"%i).click()
                    time.sleep(uniform(2.0, 3.0))

                    soup = BeautifulSoup(htmlSource, "lxml")
                    time.sleep(uniform(1.0, 2.0))

                    #리뷰 크롤링
                    Review_Keywords =driver.find_elements_by_class_name("_3jZQShkMWY")

                    # 리뷰들을 리스트에 저장
                    [review.append(word.text) for word in Review_Keywords]
                        
                except: 
                # 다음 페이지가 존재하는지 확인 (현재 페이지가 마지막 페이지인지 확인)
                    is_next_page_exist = False
                    break
driver.quit()

# 리뷰 카운트 및 정렬
get_count={}
for i in review:
    try: get_count[i] +=1
    except: get_count[i]=1


sort_dict = sorted(get_count.items(),key=lambda x:x[1], reverse=True) # value 값 기준으로 다시 정렬

[sheet.append([sort_dict[i][0],sort_dict[i][1]]) for i in range(0,len(sort_dict))]  # 엑셀에 저장

print("모든 작업이 끝났습니다. 엑셀파일로 변환됩니다.")

wb.save("리뷰옵션 정렬파일.xlsx")  # 엑셀 파일로 저장

