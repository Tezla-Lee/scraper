from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import re

driver = webdriver.Chrome('/Users/macbok/Downloads/chromedriver')

time.sleep(3)

OFFSET = 20

# location = input("지역을 입력하세요 : ")
location = "마포"

URL = f"https://www.airbnb.co.kr/s/{location}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type" \
      f"=calendar&source=structured_search_input_header&search_type=search_query&check_in=2021-02-16&check_out=2021" \
      f"-02-17 "
count = 0


# 검색 결과 페이지 수
def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "_1px14rv"})
    links = pagination.find_all('a')

    pages = []
    for link in links[0:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    print(f"{location} 검색...")
    print("검색된 페이지 수 : " + max_page.__str__())
    return max_page


def extract_accommodation(html):
    link = html.find("a")["target"]
    room_number = link[8:]

    # 사진 5개
    # driver.get(
    #     f"https://www.airbnb.co.kr/rooms/{room_number}?federated_search_id=f9a68ffc-8498-44a6-a0d6-e0281b30a491"
    #     "&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1&check_in=2025-02-12&check_out=2025"
    #     "-02-13")

    # 사진 전부
    # driver.get(
    #     f"https://www.airbnb.co.kr/rooms/{room_number}/photos?federated_search_id=dbb92de4-d73d-4db5-a219-3833d70d0f02&source_impression_id=p3_1611589387_BesBFgCKme%2FMznw2&guests=1&adults=1&check_in=2021-02-03&check_out=2021-02-04")

    # 후기 모두 보기
    driver.get(
        f"https://www.airbnb.co.kr/rooms/{room_number}/location?reviews?federated_search_id=f9a68ffc-8498-44a6-a0d6"
        f"-e0281b30a491&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1&check_in=2025-02-12"
        f"&check_out=2025 "
        "-02-13")

    time.sleep(10)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    title = extract_title(soup)
    # print(title)

    price = extract_price(soup)
    # print(price)

    rating = extract_rating(soup)
    # print(rating)

    the_number_of_review = extract_the_number_of_review(soup)
    # print(the_number_of_review)

    accommodation_description = extract_accommodation_description(soup)
    # print(accommodation_description)

    pictures = extract_pictures(soup)
    # print(pictures)

    summary = soup.find("div", {"class": "_tqmy57"}).find("div", {"class": "_xcsyj0"}).string
    # print(summary)

    features = extract_features(soup)  # [최대 인원, 침실, 침대, 욕실]
    # print(features)

    facilities = extract_facilities(soup)
    # print(facilities)

    # address = extract_address(soup)
    # print(address)

    host_name = extract_host_name(soup)
    # print(host_name)

    host_review_num = extract_host_review_num(soup)
    # print(host_review_num)

    type = extract_house_type(soup)
    # print(type)

    reviews = extract_reviews(soup)

    host_desc = extract_host_description(soup)
    # print(host_desc)

    location_description = extract_location_description(soup)
    # print(location_description)

    transportation_description = extract_transportation_description(soup)
    # print(transportation_description)

    coordinate = extract_coordinate(soup)
    print(coordinate)

    return


def extract_accommodations(last_page):
    accommodations = []
    count = 1
    for page in range(last_page):
        print(f"Scraping AirBnB page: {page}")
        result = requests.get(f"{URL}&items_offset={page * OFFSET}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "_8s3ctt"})
        for result in results:
            print(f"{count} ...")
            count += 1
            try:
                accommodation = extract_accommodation(result)
                accommodations.append(accommodation)
            except Exception as e:
                print(e)
                pass
    print("\nFinish Scraping !")
    return accommodations


def get_accommodations():
    last_page = extract_pages()
    accommodations = extract_accommodations(last_page)
    return accommodations


# 사진
def extract_pictures(html):
    pictures_html = html.find_all("img", {"class": "_6tbg2q"})
    pictures = []
    for picture_html in pictures_html:
        pictures.append(picture_html["data-original-uri"])

    return pictures


# 제목
def extract_title(html):
    title = html.find("div", {"class": "_mbmcsn"}).find("h1")

    return title.string


# 기본 요금 (1박)
def extract_price(html):
    price = html.find("span", {"class": "_pgfqnw"}).string.replace(",", "").replace("₩", "")

    return price


# 별점
def extract_rating(html):
    rating = html.find("span", {"class": "_1jpdmc0"})
    if rating is not None:
        rating = rating.string
    else:
        rating = 0

    return rating


# 후기 수
def extract_the_number_of_review(html):
    the_number_of_review = html.find("span", {"class": "_bq6krt"})
    if the_number_of_review is not None:
        the_number_of_review = the_number_of_review.string.replace("(", "").replace(")", "")
    else:
        the_number_of_review = 0

    return the_number_of_review


# 특징(?) 최대 인원, 침실, 침대, 욕실
def extract_features(html):
    results = html.find("div", {"class": "_tqmy57"}).find_all("span")
    features = []
    for result in results:
        number = re.findall("\d+", result.string)
        if number:
            features.append(number[0])
    return features


# 편의시설
def extract_facilities(html):
    results = html.find_all("div", {"class": "_1nlbjeu"})
    facilities = []
    for result in results:
        facility = result.find("div").string
        if facility:
            facilities.append(facility)
    return facilities


# 위치 (X)
def extract_address(html):
    result = html.find("div", {"class": "_1yocemr"})
    # if not result:
    #     result = html.find("div", {"class": "_nu65sd"})

    return remove_tag(result.__str__())


# 호스트 이름
def extract_host_name(html):
    result = html.find("div", {"class": "_xcsyj0"})

    return result.string.split(" ")[0].replace("님이", "")


# 건물 유형, 숙소 유형
def extract_house_type(html):
    result = html.find("div", {"class": "_xcsyj0"})

    results = result.string.split(" ")[-1].split(" ")
    results[0] = results[0].replace("의", "")
    # print(results)
    return results


# 후기 [id, date, content]
def extract_reviews(html):
    results = html.find_all("div", {"class": "_1gjypya"})
    reviews = []
    for result in results:
        review = []
        date = result.find("div", {"class": "_1ixuu7m"}).string
        name = result.find("div", {"class": "_1lc9bb6"}).__str__()
        content = result.find("div", {"class": "_1y6fhhr"}).find("span").__str__()
        id = remove_tag(name).replace(date, "")

        review.append(id)
        review.append(date)
        review.append(remove_tag(content))

        reviews.append(review)
        print(id)
    return reviews


# 태그 제거
def remove_tag(content):
    cleaner = re.compile("<.*?>")
    clean_text = re.sub(cleaner, "", content)

    return clean_text


# 숙소 설명
def extract_accommodation_description(html):
    description = html.find("div", {"class": "_1y6fhhr"}).find("span").__str__() \
        .replace("<span>", "") \
        .replace("<br/>", "\n").replace(
        "<span class=\"_1di55y9\">",
        "").replace("</span>", "")

    return description


# 위치 상세 설명
def extract_location_description(html):
    try:
        description = html.find("div", {"class": "_vd6w38n"}).find("div", {"class": "_1y6fhhr"}).find("span").__str__() \
            .replace("<span>", "") \
            .replace("<br/>", "\n").replace(
            "<span class=\"_1di55y9\">",
            "").replace("</span>", "")
        return description
    except Exception as e:
        pass

    return ""


# 교통편 상세 설명
def extract_transportation_description(html):
    try:
        description = html.find("div", {"class": "_8uj869"}).find("div", {"class": "_1y6fhhr"}).find("span").__str__() \
            .replace("<span>", "") \
            .replace("<br/>", "\n").replace(
            "<span class=\"_1di55y9\">",
            "").replace("</span>", "")
        return description
    except Exception as e:
        pass

    return ""


# 호스트의 후기 개수
def extract_host_review_num(html):
    try:
        review_num = html.find("li", {"class": "_1belslp"}).find("span", {"class": "_pog3hg"}).string
        review_num = review_num.split(" ")

        return review_num[1].replace("개", "")
    except Exception as e:
        pass

    return 0


# 호스트 소개
def extract_host_description(html):
    try:
        desc = html.find("div", {"class": "_uz1jgk"}).find("div", {"class": "_1y6fhhr"}).__str__() \
            .replace("<span>", "") \
            .replace("<br/>", "\n").replace("<div class=\"_1y6fhhr\">", "").replace("</div>", "")

        return desc
    except Exception as e:
        pass

    return ""


# 좌표 [위도, 경도]
def extract_coordinate(html):
    coordinate = html.find("div", {"class": "_8uj869"}).find("a")["href"] \
        .replace("https://maps.google.com/maps?ll=", "").replace("&z=14&t=m&hl=ko&gl=KR&mapclient=apiv3", "")

    coordinate = coordinate.split(",")

    if coordinate.__len__() != 2:
        raise Exception('좌표가 없습니다.')

    return coordinate
