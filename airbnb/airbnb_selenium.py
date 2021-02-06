from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import re

OFFSET = 20

time_cycle = 5


def get_accommodations(city, gu, start, driver):
    URL = f"https://www.airbnb.co.kr/s/{gu}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query&check_in=2021-04-05&check_out=2021-04-06"

    last_page = extract_pages(URL, city, gu)
    accommodations = extract_accommodations(last_page, URL, city, gu, start, driver)

    return accommodations


# 검색 결과 페이지 수
def extract_pages(URL, city, gu):
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "_1px14rv"})
    links = pagination.find_all('a')

    pages = []
    for link in links[0:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    print(f"{city} {gu} 크롤링 시작...\n")
    print("검색된 페이지 수 : " + max_page.__str__())
    return max_page


def extract_accommodation(html, city, gu, number, driver, accommodation_id):
    link = html.find("a")["target"]
    room_number = link[8:]

    # 위치 상세 설명 모두 보기
    driver.get(
        f"https://www.airbnb.co.kr/rooms/{room_number}/description?federated_search_id=f9a68ffc-8498-44a6-a0d6"
        f"-e0281b30a491&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1&check_in=2021-04-05&check_out=2021-04-06")

    time.sleep(time_cycle)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    accommodation_description = extract_accommodation_description(soup)
    # print(accommodation_description)

    reviews = extract_reviews(soup, number)
    # print(reviews)

    driver.get(
        f"https://www.airbnb.co.kr/rooms/{room_number}/location?federated_search_id=f9a68ffc-8498-44a6-a0d6"
        f"-e0281b30a491&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1&check_in=2021-04-05&check_out=2021-04-06")

    print(f"https://www.airbnb.co.kr/rooms/{room_number}/federated_search_id=f9a68ffc-8498-44a6-a0d6"
        f"-e0281b30a491&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1&check_in=2021-04-05&check_out=2021-04-06")

    time.sleep(time_cycle)

    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    title = extract_title(soup)
    # print(title)

    price = extract_price(soup)
    # print(price)

    rating = extract_rating(soup)
    # print(rating)

    review_num = extract_the_number_of_review(soup)
    # print(review_num)

    pictures = extract_pictures(soup)
    # print(pictures)

    # summary = soup.find("div", {"class": "_tqmy57"}).find("div", {"class": "_xcsyj0"}).string
    # print(summary)

    features = extract_features(soup)  # [최대 인원, 침실, 침대, 욕실]
    # print(features)
    capacity = int(features[0])
    bedroom_num = int(features[1])
    bed_num = int(features[2])
    bathroom_num = int(features[3])

    # facilities = extract_facilities(soup)
    # print(facilities)

    # address = extract_address(soup)
    # print(address)

    host_name = extract_host_name(soup)
    # print(host_name)

    host_review_num = extract_host_review_num(soup)
    # print(host_review_num)

    types = extract_type(soup)
    if types[0] == '호스팅하는':
        building_type = types[1]
        accommodation_type = ''
    else:
        building_type = types[0]
        accommodation_type = types[1]
    # print(types)

    host_desc = extract_host_description(soup)
    # print(host_desc)

    descriptions = extract_descriptions(soup)
    # print(descriptions)
    location_description = descriptions[0]
    # print(location_description)

    transportation_description = descriptions[1]
    # print(transportation_description)

    coordinate = extract_coordinate(soup)
    # print(coordinate)
    latitude = float(coordinate[0])
    longitude = float(coordinate[1])

    return \
        [
            {
                "accommodation_id": accommodation_id,
                "city": city,
                "gu": gu,
                "title": rmEmoji_ascii(title),
                "capacity": capacity,
                "bathroom_num": bathroom_num,
                "bedroom_num": bedroom_num,
                "bed_num": bed_num,
                "price": price,
                "contact": "010-1234-5678",
                "latitude": latitude,
                "longitude": longitude,
                "location_desc": rmEmoji_ascii(location_description),
                "transportation_desc": rmEmoji_ascii(transportation_description),
                "accommodation_desc": rmEmoji_ascii(accommodation_description),
                "host_desc": rmEmoji_ascii(host_desc),
                "rating": rating,
                "review_num": review_num,
                "accommodation_type": accommodation_type,
                "building_type": building_type,
                "host_name": host_name,
                "host_review_num": host_review_num,
            }, [
            {
                "url": pictures[0],
                "accommodation_id": number
            }, {
                "url": pictures[1],
                "accommodation_id": number
            }, {
                "url": pictures[2],
                "accommodation_id": number
            }, {
                "url": pictures[3],
                "accommodation_id": number
            }, {
                "url": pictures[4],
                "accommodation_id": number
            }
        ],
            reviews
        ]


def extract_accommodations(last_page, URL, city, gu, start, driver):
    accommodations = []
    accommodations.append({
        "accommodation_id": "",
        "city": "",
        "gu": "",
        "title": "",
        "capacity": "",
        "bathroom_num": "",
        "bedroom_num": "",
        "bed_num": "",
        "price": "",
        "contact": "",
        "latitude": "",
        "longitude": "",
        "location_desc": "",
        "transportation_desc": "",
        "accommodation_desc": "",
        "host_desc": "",
        "rating": "",
        "review_num": "",
        "accommodation_type": "",
        "building_type": "",
        "host_name": "",
        "host_review_num": ""
    })
    pictures = []
    reviews = []
    reviews.append({
        "name": "",
        "created_date": "",
        "content": "",
        "accommodation_id": "",
        "rating": ""
    }, )
    accommodation_count = start

    # for page in range(1):
    for page in range(last_page):
        print(f"Scraping {city} {gu} page: {page}\n")
        result = requests.get(f"{URL}&items_offset={page * OFFSET}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "_8s3ctt"})

        for result in results:
            print(f"{accommodation_count}...")
            try:
                accommodation_info = extract_accommodation(result, city, gu, accommodation_count, driver, accommodation_count)
                accommodation = accommodation_info[0]
                picture = accommodation_info[1]
                review = accommodation_info[2]
                accommodations.append(accommodation)

                # if accommodation_count == start + 2:
                #     break

                for pic in picture:
                    pictures.append(pic)

                for rev in review:
                    reviews.append(rev)

                print(accommodation)
                print(picture)
                print(review)
                accommodation_count += 1

            except Exception as e:
                print(e)
                pass
            print()

    print("\nFinish Scraping !")
    return [accommodations, pictures, reviews, accommodation_count]


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
    price = html.find("div", {"class": "_wgmchy"}).find("span", {"class": "_pgfqnw"}).string.replace(",", "").replace(
        "₩", "")

    return int(price)


# 별점
def extract_rating(html):
    rating = 0
    try:
        rating = html.find("span", {"class": "_1hhxz3f"}).find("span", {"class": "_pgfqnw"}).string
    except:
        pass

    return float(rating)


# 후기 수
def extract_the_number_of_review(html):
    the_number_of_review = html.find("span", {"class": "_bq6krt"})
    if the_number_of_review is not None:
        the_number_of_review = the_number_of_review.string.replace("(", "").replace(")", "")
    else:
        the_number_of_review = 0

    return int(the_number_of_review)


# 특징(?) 최대 인원, 침실, 침대, 욕실
def extract_features(html):
    results = html.find("div", {"class": "_tqmy57"}).find_all("span")
    features = []
    for result in results:
        number = re.findall("\d+", result.string)
        if number:
            features.append(number[0])

    if len(features) == 3:
        features.insert(1, 1)
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
def extract_type(html):
    result = html.find("div", {"class": "_xcsyj0"})

    # print(result)
    # print(result.string.split(" "))
    # print(result.string.split(" ")[-1])
    results = result.string.split(" ")

    if len(results) == 2:
        return results[-1].split(" ")

    results = results[-1].split(" ")
    results[0] = results[0].replace("의", "")
    # print(results)
    return results


# 태그 제거
def remove_tag(content):
    cleaner = re.compile("<.*?>")
    clean_text = re.sub(cleaner, "", content)

    return clean_text


# 위치 상세 설명 & 교통편 설명
def extract_descriptions(html):
    descriptions = html.find("div", {"class": "_8uj869"}).find_all("div", {"class": "_50mnu4"})

    results = []

    for desc in descriptions:
        try:
            if len(descriptions) == 1 and '교통편' == str(desc.find("div", {"class": "_1yocemr"}).find("h2").string):
                results.append("")
            result = desc.find("div", {"class": "_1xib9m0"}).__str__().replace("<br/>", "\n")
            result = remove_tag(result)
            results.append(result)
        except Exception as e:
            pass

    if not results:
        return ["", ""]

    if len(results) == 1:
        results.append("")

    return results


# 숙소 설명
def extract_accommodation_description(html):
    description = ""
    try:
        description = html.find("div", {"class": "_1seuw5go"}).find("div", {"class": "_1xib9m0"}).find("span").__str__() \
            .replace("<br/>", "\n")
        description = remove_tag(description)
    except:
        pass

    # print(description)
    return description


# 호스트의 후기 개수
def extract_host_review_num(html):
    try:
        review_num = html.find("li", {"class": "_1belslp"}).find("span", {"class": "_pog3hg"}).string
        review_num = review_num.split(" ")

        # print(review_num)
        # print(int(review_num[-1].replace("개", "")))
        if len(review_num) != 2:
            return 0
        else:
            return int(review_num[-1].replace("개", ""))
    except:
        return 0
        # pass


# 호스트 소개
def extract_host_description(html):
    desc = ""
    try:
        desc = html.find("div", {"class": "_5zvpp1l"}).find("div", {"class": "_1xib9m0"}).__str__().replace("<br/>",
                                                                                                            "\n")
        return remove_tag(desc)
    except Exception as e:
        pass

    return desc


# 좌표 [위도, 경도]
def extract_coordinate(html):
    coordinate = html.find("div", {"class": "_8uj869"}).find("a")["href"] \
        .replace("https://maps.google.com/maps?ll=", "").replace("&z=14&t=m&hl=ko&gl=KR&mapclient=apiv3", "")

    coordinate = coordinate.split(",")

    if coordinate.__len__() != 2:
        raise Exception('좌표를 찾을 수 없습니다.')

    return coordinate


# 후기 [id, date, content]
def extract_reviews(html, number):
    results = html.find_all("div", {"class": "_50mnu4"})
    # print(results)
    reviews = []
    for result in results:
        review = []
        date = result.find("div", {"class": "_1ixuu7m"}).string
        name = result.find("div", {"class": "_1lc9bb6"}).__str__()
        content = result.find("div", {"class": "_1xib9m0"}).find("span").__str__()
        id = remove_tag(name).replace(date, "")
        date = date.replace("년 ", "-").replace("월", "-1")

        reviews.append(
            {
                "name": id,
                "created_date": date,
                "content": rmEmoji_ascii(remove_tag(content)),
                "accommodation_id": number,
                "rating": 0.0
            }
        )

        # review.append(id)
        # review.append(date)
        # review.append(remove_tag(content))

        # reviews.append(review)
    return reviews


def rmEmoji_ascii(input_string):
    return input_string.encode('euc-kr', 'ignore').decode('euc-kr')
