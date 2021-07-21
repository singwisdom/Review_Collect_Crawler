import openpyxl
from tqdm import tqdm

def save_to_excel_file(URL : str, title : str, data : list, count:int):

    wb = openpyxl.Workbook() # 워크북 생성
    sheet=wb.active # Sheet 활성
    sheet.append(["입력한 URL : " + URL])  # 데이터 프레임 내 변수명 생성
    sheet.append(["품목명 : %s" %title])
    sheet.append(["옵션", "카운트"]) 


    # 리뷰 카운트 및 정렬
    get_count={}
    for i in data:
        try: get_count[i] += 1
        except: get_count[i] = 1

    sort_dict = sorted(get_count.items(), key=lambda x:x[1], reverse=True) # value 값 기준으로 다시 정렬
    [sheet.append([sort_dict[i][0],sort_dict[i][1]]) for i in range(0, len(sort_dict))]  # 엑셀에 저장

    wb.save("리뷰 분석(%d) .xlsx" %count)  # 엑셀 파일로 저장
    
