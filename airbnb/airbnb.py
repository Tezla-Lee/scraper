import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

OFFSET = 20

# location = input("지역을 입력하세요 : ")
location = "마포"

URL = f"https://www.airbnb.co.kr/s/{location}/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&date_picker_type=calendar&source=structured_search_input_header&search_type=search_query&check_in=2021-02-16&check_out=2021-02-17"


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
    # title = html.find("a")["aria-label"]
    # img = html.find("div", {"class": "_4626ulj"}).find("img")["src"]
    # link = html.find("a")["href"]
    # return {'title': title, 'img': img, 'link': f"https://www.airbnb.co.kr/{link}"}
    # link = "https://www.airbnb.co.kr" + html.find("a")["href"] + "&check_in=2021-02-16&check_out=2021-02-17"

    link = html.find("a")["target"]
    # link = html.find("a")["href"]
    room_number = link[8:]

    # "https://www.airbnb.co.kr/rooms/46093747?federated_search_id=b3e0cc69-a4dd-4fe3-baae-0c28ab94162c&check_in=2021-02-16&check_out=2021-02-17&source_impression_id=p3_1611584741_dve9CIKLNhsuIKBO&guests=1&adults=1&check_in=2021-02-16&check_out=2021-02-17"

    # result = requests.get(f"https://www.airbnb.co.kr{link}")
    # print(f"https://www.airbnb.co.kr{link}")
    result = requests.get(
        f"https://www.airbnb.co.kr/rooms/{room_number}?federated_search_id=f9a68ffc-8498-44a6-a0d6-e0281b30a491&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1")
    # print(f"https://www.airbnb.co.kr/rooms/{room_number}?federated_search_id=f9a68ffc-8498-44a6-a0d6-e0281b30a491&source_impression_id=p3_1611588826_7FLZBGwSxmQjBix%2F&guests=1&adults=1")

    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "_1y6fhhr"})

    for re in results:
        print(re)

    # print(soup)
    # title = soup.find("div", {"class": "_mbmcsn"})
    # print(title)

    return link


def extract_accommodations(last_page):
    accommodations = []
    for page in range(last_page):
        print(f"Scraping AirBnB page: {page}")
        result = requests.get(f"{URL}&items_offset={page * OFFSET}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "_8s3ctt"})

        for result in results:
            accommodation = extract_accommodation(result)
            accommodations.append(accommodation)

    print("\nFinish Scraping !")
    return accommodations


def get_accommodations():
    last_page = extract_pages()
    accommodations = extract_accommodations(last_page)
    return accommodations
