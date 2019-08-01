#http://parking.seoul.go.kr/
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pymongo

from pprint import pprint
#크롬 드라이버 설정
driver = webdriver.Chrome('chromedriver')
driver.get("http://parking.seoul.go.kr")
# mongo 디비 연결 설정 및 collection 받기
client = pymongo.MongoClient("<please input mongodb url>")
db = client.get_database('seoul_parking')
collection = db.get_collection('parking_lot')

data = []
# cf) 매개변수 district_index 2~26까지 2는 강남구 26 중랑구
start_time = time.time()
for district_index in range(2,3):
    # 검색조건 체크박스 찾기
    search = driver.find_element_by_xpath('//*[@id="inpBox2"]/div[1]/a')
    search.click()
    time.sleep(1)
    # 검색조건 체크박스중 district_index번째 li태그(해당구)클릭
    search_checkbox = driver.find_element_by_xpath('//*[@id="inpBox2"]/div[1]/ul/li['+str(district_index)+']/a')
    search_checkbox.click()
    time.sleep(1)
    # 검색버튼 클릭
    search_submit = driver.find_element_by_xpath('//*[@id="parking_search"]')
    search_submit.click()
    time.sleep(3)
    result = driver.find_elements_by_css_selector('#pk_search_view > ul a')
    for result_li in result:
        result_li.click()
        time.sleep(0.2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        park_name = soup.select_one('.pop_detail > .hd h3').text
        park_addr = soup.select_one('.pop_detail .addr2').text
        park_count = soup.select_one('.pop_detail .fl > .stxt').text
        print('이름 : %s, 주소 : %s, 전체주차면 : %s' % (park_name, park_addr, park_count))
        data = {"pname" : park_name, "addr2" : park_addr, "total" : park_count}
        collection.insert_one(data)

print("강남구 처리 시간 : ", time.time()-start_time)