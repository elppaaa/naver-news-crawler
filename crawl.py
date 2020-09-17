# coding: utf-8

import requests
from bs4 import BeautifulSoup as bs4
from multiprocessing import Pool

import csv
import datetime
import time
import os


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


# 뉴스 정보 반환
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


# for category crawl error
def get_news_category(soup):
    try:
        return soup.select_one("em.media_end_categorize_item").text
    except:
        return "연예"


def crawl_inpage(_link):
    # select_one error
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
            if _i == None:
                _i = "None"
    finally:
        return date, text, category


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

    with open(fname, "w", newline="", encoding="utf-8") as f:
        file = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        # head
        file.writerow(["title", "date", "category", "text", "press", "link"])
        tmp = ""
        for page in range(267):
            url = n_url + "&start=" + str(page * 15 + 1)
            page_rows = crawl_whole_search_page(url)
            # 중복기록최소화
            if tmp != page_rows:
                file.writerows(page_rows)
                tmp = page_rows
    print("file: '{}' done".format(fname))
    # wirte finished file
    with open(DONEFILE, "a", encoding="utf-8") as done:
        done.write(fname + "\n")


# create data set
def setSearchList():
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
        9,
        8,
        11,
        277,
        18,
        366,
        123,
        14,
        15,
        16,
        92,
        79,
        629,
        119,
        138,
        29,
        417,
        6,
        293,
        31,
        47,
        30,
        2,
        24,
        308,
        586,
        262,
        94,
        243,
        33,
        37,
        53,
        353,
        36,
        50,
        127,
        607,
        584,
        310,
        7,
        152,
        640,
        44,
        296,
        346,
        87,
        88,
        82,
    ]
    KEYWORD = input("키워드 입력 : ")
    STARTDATE = list(map(int, input("시작 날짜 입력 예) 2020 1 31:   ").split(" ")))
    start_date = datetime.date(STARTDATE[0], STARTDATE[1], STARTDATE[2])

    ENDDATE = list(map(int, input("종료 날짜 입력 예) 2020 3 4:   ").split(" ")))
    end_date = datetime.date(ENDDATE[0], ENDDATE[1], ENDDATE[2])

    # 몇일 단위로 쪼개어 검색할지.
    DAYS = int(input("몇일치씩 다운로드 할까요? : "))

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


if __name__ == "__main__":
    search_list = setSearchList()
    pool = Pool(processes=8)
    pool.map(start_crawl, search_list)
