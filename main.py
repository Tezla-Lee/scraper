from airbnb.save import save_to_file_json
from airbnb.save import add_data
from airbnb.airbnb_selenium import get_accommodations
from airbnb.save import make_directory
from airbnb.save import save_ac_id
from airbnb.save import read_ac_id
from airbnb.save import save_cr_index
from airbnb.save import read_cr_index
from airbnb.save import read_all_id
from airbnb.save import save_all_id
from selenium import webdriver
import time
import datetime

city = "서울특별시"
gus = {"종로구", "성동구", "광진구", "중랑구", "성북구", "도봉구", "노원구", "은평구", "서대문구", "강서구",
       "영등포구", "동작구", "관악구", "서초구", "강동구"}
driver = webdriver.Chrome('/Users/macbok/Downloads/chromedriver')

start_time = time.time()
first_start_id = int(read_ac_id())
all_id = int(read_all_id())
save_all_id(all_id + 1)

for gu in gus:
    start_id = int(read_ac_id())
    crawl_id = int(read_cr_index())
    print(f"크롤링 {crawl_id} 번째 구 시작")
    print(f"숙박 시작 번호 : {start_id}")
    start = time.time()
    accommodations_info = get_accommodations(city, gu, start_id, driver)
    accommodations = accommodations_info[0]
    pictures = accommodations_info[1]
    reviews = accommodations_info[2]
    print()
    print(f"{accommodations_info[3] - start_id}개 추가 완료")
    end_id = accommodations_info[3]
    save_ac_id(int(end_id))
    save_cr_index(crawl_id + 1)

    make_directory(city)

    save_to_file_json(accommodations, pictures, reviews, city, gu, crawl_id, start_id)
    print(f"{city} {gu} 저장")
    add_data(accommodations, pictures, reviews, all_id, city, first_start_id)

    sec = time.time() - start
    times = str(datetime.timedelta(seconds=sec)).split(".")
    times = times[0]
    print()
    print(times)


print()
print(f"총 걸린 시간 : {str(datetime.timedelta(seconds=time.time() - start_time))}")
driver.close()
