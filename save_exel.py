import openpyxl
from tqdm import tqdm

def save_to_excel_file(URL : str, data : list):

    wb = openpyxl.Workbook() # 워크북 생성
    sheet=wb.active # Sheet 활성
    wb.title ="리뷰 크롤러" # Sheet 이름 설정
    sheet.append(["입력한 URL : " + URL])  # 데이터 프레임 내 변수명 생성
    sheet.append(["옵션", "카운트"]) 


    # 리뷰 카운트 및 정렬
    get_count={}
    for i in data:
        try: get_count[i] += 1
        except: get_count[i] = 1

    sort_dict = sorted(get_count.items(), key=lambda x:x[1], reverse=True) # value 값 기준으로 다시 정렬
    [sheet.append([sort_dict[i][0],sort_dict[i][1]]) for i in tqdm(range(0, len(sort_dict)), desc="모든 리뷰 분석 진행상황")]  # 엑셀에 저장

    wb.save("리뷰 분석 .xlsx")  # 엑셀 파일로 저장
    print("\n>> 모든 작업이 끝났습니다. 엑셀파일로 변환됩니다. <<")
