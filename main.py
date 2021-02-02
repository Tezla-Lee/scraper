from airbnb.save import save_to_file_json
from airbnb.airbnb_selenium import get_accommodations

city = "서울특별시"
gu = "마포구"

accommodations_info = get_accommodations(city, gu, 1)
accommodations = accommodations_info[0]
pictures = accommodations_info[1]
save_to_file_json(accommodations, pictures, city, gu)
