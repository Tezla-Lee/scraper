import requests
from bs4 import BeautifulSoup
import csv

link = "https://www.airbnb.co.kr/rooms/47788267?federated_search_id=624e3893-9a41-4502-8cc8-ad5913e14f66&source_impression_id=p3_1611590091_7vY2f1JosD8kVadT&guests=1&adults=1"
result = requests.get(link)
soup = BeautifulSoup(result.text, "html.parser")
file = open("abc.csv", mode="w")
writer = csv.writer(file)
writer.writerow(soup)
