# Naver News Crawler



#### used module

- bs4 
- reqeusts

- multiprocessing



- csv
- datetime
- time





#### usage

`ptyhon3 crawl.py`

키워드 입력 : [검색할 키워드]

시작 날짜 입력 예) 2020 1 31:  [시작 날짜]

종료 날짜 입력 예) 2020 3 4:   [종료 날짜]

몇일치씩 다운로드 할까요? : [2로 설정하면 2일치씩 검색을 수행함]



#### output

`키워드_언론사번호_검색범위.csv`

ex) `김치_005_0101_0131.csv`



#### info

- utf-8로 인코딩되어 엑셀에서 깨져 보일 수 있습니다.

- 네이버 뉴스 모바일 검색을 기반으로 수집합니다.
- 네이버 뉴스 화면으로 표시 가능한 모든 언론사에서 수집합니다.
- 네이버 뉴스는 최대 4000건의 검색 결과를 지원하므로 검색을 작은 단위(1,2일)로 검색하는 것을 추천합니다
- 언론사를 특정하려면 아래 셀을 참고하여 press_num_list를 수정하면 됩니다.
- 검색에 벤을 먹을 경우 30초 단위로 재시도를 수행합니다.

- 중복을 최소화하려 하였으나 일부 중복되어 쌓입니다.



| title     | date      | category                   | text                | press           | link      |
| --------- | --------- | -------------------------- | ------------------- | --------------- | --------- |
| 뉴스 제목 | 작성 일자 | 네이버에서 분류한 카테고리 | 기사 내용(전처리 X) | 언론사 고유번호 | 뉴스 링크 |



|     언론사      | 고유번호 |
| :-------------: | -------- |
|    경향신문     | 32       |
|    국민일보     | 5        |
|    동아일보     | 20       |
|    문화일보     | 21       |
|    서울신문     | 81       |
|    세계일보     | 22       |
|    조선일보     | 23       |
|    중앙일보     | 25       |
|     한겨례      | 28       |
|    한국일보     | 469      |
|      JTBC       | 437      |
|       KBS       | 56       |
|       MBC       | 214      |
|       MBN       | 57       |
|    SBS\_cnbc    | 374      |
|       SBS       | 55       |
|    TVchosun     | 448      |
|       YTN       | 52       |
|      news1      | 421      |
|     newsis      | 3        |
|    연합뉴스     | 1        |
|   연합뉴스TV    | 422      |
|    channel A    | 449      |
|    한국경제     | 215      |
|    매일경제     | 9        |
|  MTO머니투데이  | 8        |
|    서울경제     | 11       |
|   아시아경제    | 277      |
|    이데일리     | 18       |
|    chosunBiz    | 366      |
|    조세일보     | 123      |
|  파이낸셜뉴스   | 14       |
|    한국경제     | 15       |
|   헤럴드경제    | 16       |
|   zdNetKorea    | 92       |
|    노컷뉴스     | 79       |
|    THE FACT     | 629      |
|    데일리안     | 119      |
|  디지털데일리   | 138      |
|  디지털 타임스  | 29       |
|     Money S     | 417      |
|   미디어오늘    | 6        |
|     BLOTER      | 293      |
|   아이뉴스24    | 31       |
|   오마이뉴스    | 47       |
|    전자신문     | 30       |
|    프레시안     | 2        |
|   애경economy   | 24       |
|     시사in      | 308      |
|    시사저널     | 586      |
|     신동아      | 262      |
|     월간 산     | 94       |
|  이코노미스트   | 243      |
|    주간경향     | 33       |
|    주간동아     | 37       |
|    주간조선     | 53       |
|   중앙SUNDAY    | 353      |
|    한겨례21     | 36       |
|  한경Business   | 50       |
|   기자협회보    | 127      |
|    뉴스타파     | 607      |
|  동아사이언스   | 584      |
|    여성신문     | 310      |
|      일다       | 7        |
|     참세상      | 152      |
| 한국중앙 데일리 | 640      |
|  코리아 헤럴드  | 44       |
|   코메디닷컴    | 296      |
|    헬스조선     | 346      |
|    강원일보     | 87       |
|    매일신문     | 88       |
|    부산일보     | 82       |