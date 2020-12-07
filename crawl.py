# coding: utf-8


# 필요한 패키지 설치
import requests
from bs4 import BeautifulSoup as bs4
from multiprocessing import Pool

import csv
import datetime
import time
import os
import sys

# request 보낼 시에 사용할 헤더 미리 생성함.
headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.1 Mobile/15E148 Safari/604.1",
    "authority": "news.naver.com",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "dnt": "1",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,da;q=0.5",
}

# 프로그램 실행 도중 중단을 대비하여 완료된 파일 저장.
# done.txt에 있는 파일은 다시 동일 내용 실행 시에도 중복으로 수행되지 않음.
DONEFILE = "done.txt"

if os.path.isfile(DONEFILE):
    with open(DONEFILE, "r", encoding="utf-8") as done:
        done_list = done.readlines()
    done_list = [_t.replace("\n", "") for _t in done_list]
else:
    done_list = []


# 뉴스 검색 결과 한페이지 정보 수집
# '네이버뉴스' 일 경우 csv 파일에 기록
def crawl_whole_search_page(link):
    while True:
        ## 차단 확인
        tmp = requests.get(link, headers=headers)
        if "200" not in str(tmp):
            print("load err, wait 30sec")
            time.sleep(30)
        else:
            break
    soup = bs4(tmp.text, "html.parser")
    new_div_list = soup.select("div.group_news > ul  div.news_wrap")
    tmp = []
    for _news in new_div_list:
        _data = crawl_news(_news)
        if _data is not None:
            tmp.append(_data)
    return tmp


# 뉴스 기사 파싱하는 코드
def crawl_news(_news):
    if "네이버뉴스" in str(_news.select_one("div.news_info")):
        title = _news.select_one("div.api_txt_lines").text
        link = _news.select_one("a.news_tit")["href"]
        press = _news.select_one("a.info.press")["href"]
        press = press.split("/")[-1]
        date, text, category = crawl_inpage(link)
        return [title, date, category, text, press, link]
    else:
        return None


# 연예 카테고리가 DOM 구조가 다른 경우를 위해 애러 처리함.
def get_news_category(soup):
    try:
        return soup.select_one("em.media_end_categorize_item").text
    except:
        return "연예"


#뉴스 기사 페이지를 파싱함.
def crawl_inpage(_link):
    date = ""
    text = ""
    category = ""
    # DOM 구조가 다를 경우를 대비해 예외처리
    try:
        tmp = requests.get(_link, headers=headers)
        soup = bs4(tmp.text, "html.parser")
        # date = soup.select_one("div.media_end_head_info div  span")["data-date-time"]
        date = soup.select_one("span._ARTICLE_DATE_TIME")["data-date-time"]
        text = soup.select_one("div#dic_area").text
        text = text.replace("\n", "")
        category = get_news_category(soup)
    except AttributeError:
        for _i in [date, text, category]:
            if _i == "":
                _i = "None"
    finally:
        return date, text, category


# 파싱할 날짜, 키워드, 기간, 언론사가 포함된 딕셔너리 파일을 기준으로 파싱 수행.
def start_crawl(_dict):
    global done_list
    baseurl = "https://m.search.naver.com/search.naver?where=m_news&query={keyword}&sm=mtb_tnw&sort=0&photo=0&field=0&pd=3&ds={org_start}&de={org_end}&docid=&related=0&mynews=1&office_type=1&office_section_code=1&news_office_checked=1{press}&nso=so%3Ar%2Cp%3Afrom{start}to{end}"
    keyword = _dict["keyword"]
    org_start = _dict["start"]
    org_end = _dict["end"]
    press = _dict["pressnum"]
    start = org_start.replace(".", "")
    end = org_end.replace(".", "")

    fname = "./{}_{}_{}_{}.csv".format(keyword, press, start[4:], end[4:])
    n_url = baseurl.format(
        keyword=keyword,
        org_start=org_start,
        org_end=org_end,
        press=press,
        start=start,
        end=end,
    )

    if fname in done_list:
        return

    # 파일에 저장
    with open(fname, "w", newline="", encoding="utf-8") as f:
        file = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        # header
        file.writerow(["title", "date", "category", "text", "press", "link"])
        tmp = ""
        for page in range(267):
            url = n_url + "&start=" + str(page * 15 + 1)
            page_rows = crawl_whole_search_page(url)
            # 중복기록최소화를 위해 이전과 동일한 기사인 경우 저장하지 않음
            if tmp != page_rows:
                file.writerows(page_rows)
                tmp = page_rows
    print("file: '{}' done".format(fname))
    # 파싱 내용 저장 완료후 저장함 
    with open(DONEFILE, "a", encoding="utf-8") as done:
        done.write(fname + "\n")


# 파싱할 목록 생성 
def setSearchList():
    # 사용할 언론사 고유 번호
    press_num_list = [
        32,
        5,
        20,
        21,
        81,
        22,
        23,
        25,
        28,
        469,
        437,
        56,
        214,
        57,
        374,
        55,
        448,
        52,
        421,
        3,
        1,
        422,
        449,
        215,
    ]
    
    # commandline 지원
    if len(sys.argv) == 5:
        KEYWORD = sys.argv[1]
        STARTDATE = sys.argv[2]
        ENDDATE = sys.argv[3]
        DAYS = int(sys.argv[4])
    else:
        KEYWORD = input("키워드 입력 : ")
        STARTDATE = input("시작 날짜 입력 예) 20200131:  ")
        ENDDATE = input("종료 날짜 입력 예) 20200131:  ")
        # 몇일 단위로 쪼개어 검색할지.
        DAYS = int(input("몇일치씩 다운로드 할까요? : "))

    start_date = datetime.date(
        int(STARTDATE[0:4]), int(STARTDATE[4:6]), int(STARTDATE[6:])
    )
    end_date = datetime.date(int(ENDDATE[0:4]), int(ENDDATE[4:6]), int(ENDDATE[6:]))

    # 입력받은 기간과, 키워드를 기준으로 DAYS 단위로 딕셔너리 생성.
    arr = []
    date = start_date
    while date <= end_date:
        start = str(date).replace("-", ".")
        date += datetime.timedelta(days=DAYS - 1)
        if date > end_date:
            date = end_date
        end = str(date).replace("-", ".")
        date += datetime.timedelta(days=1)
        for press in press_num_list:
            press = "%03d" % press
            dic = {"keyword": KEYWORD, "start": start, "end": end, "pressnum": press}
            arr.append(dic)
    return arr


# main 메서드
if __name__ == "__main__":
    search_list = setSearchList()
    pool = Pool(processes=8)
    pool.map(start_crawl, search_list)
