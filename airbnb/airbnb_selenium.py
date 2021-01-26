from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import re

driver = webdriver.Chrome('/Users/macbok/Downloads/chromedriver')

OFFSET = 20

# location = input("지역을 입력하세요 : ")
location = "마포"

URL = f"https://www.airbnb.co.kr/s/{location}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query&check_in=2021-02-16&check_out=2021-02-17"
count = 0


def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "_1px14rv"})
    links = pagination.find_all('a')

    pages = []
    for link in links[0:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    print("검색된 페이지 수 : " + max_page.__str__())
    return max_page


def extract_accommodation(html):
    link = html.find("a")["target"]
    room_number = link[8:]

    # 사진 5개
    driver.get(
        f"https://www.airbnb.co.kr/rooms/{room_number}?federated_search_id=f9a68ffc-8498-44a6-a0d6-e0281b30a491"
        "&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1&check_in=2025-02-12&check_out=2025"
        "-02-13")

    # 사진 전부
    # driver.get(
    #     f"https://www.airbnb.co.kr/rooms/{room_number}/photos?federated_search_id=dbb92de4-d73d-4db5-a219-3833d70d0f02&source_impression_id=p3_1611589387_BesBFgCKme%2FMznw2&guests=1&adults=1&check_in=2021-02-03&check_out=2021-02-04")

    time.sleep(3.5)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    title = extract_title(soup)
    # print(title.string)

    price = extract_price(soup)
    # print(price)

    star = extract_star(soup)
    # print(star)

    the_number_of_review = extract_the_number_of_review(soup)
    # print(the_number_of_review)

    description = soup.find("div", {"class": "_1y6fhhr"}).find("span").__str__() \
        .replace("<span>", "") \
        .replace("<br/>", "\n").replace(
        "<span class=\"_1di55y9\">",
        "").replace("</span>", "")
    # print(description)

    pictures = extract_pictures(soup)

    summary = soup.find("div", {"class": "_tqmy57"}).find("div", {"class": "_xcsyj0"}).string

    features = extract_features(soup)  # [최대 인원, 침실, 침대, 욕실]

    facilities = extract_facilities(soup)

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
            accommodation = extract_accommodation(result)
            accommodations.append(accommodation)

    print("\nFinish Scraping !")
    return accommodations


def get_accommodations():
    last_page = extract_pages()
    accommodations = extract_accommodations(last_page)
    return accommodations


def extract_pictures(html):
    pictures_html = html.find_all("img", {"class": "_6tbg2q"})
    pictures = []
    for picture_html in pictures_html:
        pictures.append(picture_html["data-original-uri"])

    return pictures


def extract_title(html):
    title = html.find("div", {"class": "_mbmcsn"}).find("h1")

    return title.stringdef


def extract_price(html):
    price = html.find("span", {"class": "_pgfqnw"}).string.replace(",", "").replace("₩", "")

    return price


def extract_star(html):
    star = html.find("span", {"class": "_1jpdmc0"})
    if star is not None:
        star = star.string
    else:
        star = 0

    return star


def extract_the_number_of_review(html):
    the_number_of_review = html.find("span", {"class": "_bq6krt"})
    if the_number_of_review is not None:
        the_number_of_review = the_number_of_review.string.replace("(", "").replace(")", "")
    else:
        the_number_of_review = 0

    return the_number_of_review


# 특징... 최대 인원, 침실, 침대, 욕실
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
