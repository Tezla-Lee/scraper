import csv
import json
import os


def make_directory(city):
    current_path = os.getcwd()
    path2 = current_path + "/json/" + city
    if not os.path.isdir(path2):
        os.mkdir(path2)

    path3 = path2 + "/리뷰"
    if not os.path.isdir(path3):
        os.mkdir(path3)

    path3 = path2 + "/사진"
    if not os.path.isdir(path3):
        os.mkdir(path3)

    path3 = path2 + "/숙박"
    if not os.path.isdir(path3):
        os.mkdir(path3)

    path4 = path2 + "/통합"
    if not os.path.isdir(path4):
        os.mkdir(path4)

    path5 = path4 + "/리뷰"
    if not os.path.isdir(path5):
        os.mkdir(path5)

    path5 = path4 + "/사진"
    if not os.path.isdir(path5):
        os.mkdir(path5)

    path5 = path4 + "/숙박"
    if not os.path.isdir(path5):
        os.mkdir(path5)
    return


def save_all_json(accommodations, photos, reviews, city, gu, num, start_id):
    toJson_accomm_all(accommodations, city, gu, num, start_id)
    toJson_photo_all(photos, city, gu, num, start_id)
    toJson_review_all(reviews, city, gu, num, start_id)
    return


def save_to_file_json(accommodations, photos, reviews, city, gu, num, start_id):
    toJson_accomm(accommodations, city, gu, num, start_id)
    toJson_photo(photos, city, gu, num, start_id)
    toJson_review(reviews, city, gu, num, start_id)
    return


def save_to_file_csv(accommodations, photos, city, gu):
    save_to_ac_csv(accommodations, city, gu)
    save_to_file_photo_csv(photos, city, gu)
    return


def toJson_accomm(lists, city, gu, num, start_id):
    with open(f"json/{city}/숙박/{str(num)}_{gu}_{str(start_id)}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')
    return


def toJson_photo(lists, city, gu, num, start_id):
    with open(f"json/{city}/사진/{str(num)}_{gu}_{str(start_id)}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')
    return


def toJson_review(lists, city, gu, num, start_id):
    with open(f"json/{city}/리뷰/{str(num)}_{gu}_{str(start_id)}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')
    return


def toJson_accomm_all(lists, city, gu, num, start_id):
    with open(f"json/{city}/통합/숙박/{str(num)}_{gu}_{str(start_id)}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')
    return


def toJson_photo_all(lists, city, gu, num, start_id):
    with open(f"json/{city}/통합/사진/{str(num)}_{gu}_{str(start_id)}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')
    return


def toJson_review_all(lists, city, gu, num, start_id):
    with open(f"json/{city}/통합/리뷰/{str(num)}_{gu}_{str(start_id)}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')
    return


def save_ac_id(num):
    f = open("ac_id.txt", 'w')
    f.write(str(num))
    f.close()
    return


def read_ac_id():
    f = open("ac_id.txt", 'r')
    num = int(f.readline())
    f.close()
    return num


def save_cr_index(num):
    f = open("cr_id.txt", 'w')
    f.write(str(num))
    f.close()


def read_cr_index():
    f = open("cr_id.txt", 'r')
    num = int(f.readline())
    f.close()

    return num


def save_all_id(num):
    f = open("all_id.txt", 'w')
    f.write(str(num))
    f.close()


def read_all_id():
    f = open("all_id.txt", 'r')
    num = int(f.readline())
    f.close()

    return num


def save_to_ac_csv(accommodations, city, gu):
    file = open(f"csv/{city}/{gu}.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(
        [
            "city",
            "gu",
            "title",
            "capacity",
            "bathroom_num",
            "bedroom_num",
            "bed_num",
            "price",
            "contact",
            "latitude",
            "longitude",
            "location_desc",
            "transportation_desc",
            "accommodation_desc",
            "host_desc",
            "rating",
            "review_num",
            "accommodation_type",
            "building_type",
            "host_name",
            "host_review_num",
        ])

    for accommodation in accommodations:
        writer.writerow(list(accommodation.values()))

    file.close()


def save_to_file_photo_csv(photos, city, gu):
    file = open(f"csv/{city}/{gu}_photo.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(
        [
            "url",
            "accommodation_id"
        ])

    for photo in photos:
        writer.writerow(list(photo.values()))

    file.close()


def add_data(accomms, photos, reviews, num, city, start_id):
    file_path = f"json/{city}/통합/숙박/{str(num)}_{city}_{str(start_id)}.json"
    with open(file_path, 'w') as file:
        try:
            json_data = json.load(file)
        except:
            json_data = []

    for accomm in accomms:
        json_data.append(accomm)

    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent='\t')

    file.close()
    outfile.close()

    file_path = f"json/{city}/통합/사진/{str(num)}_{city}_{str(start_id)}.json"
    with open(file_path, 'w') as file:
        try:
            json_data = json.load(file)
        except:
            json_data = []

    for photo in photos:
        json_data.append(photo)

    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent='\t')

    file.close()
    outfile.close()

    file_path = f"json/{city}/통합/리뷰/{str(num)}_{city}_{str(start_id)}.json"
    with open(file_path, 'w') as file:
        try:
            json_data = json.load(file)
        except:
            json_data = []

    for review in reviews:
        json_data.append(review)

    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent='\t')
    file.close()
    outfile.close()
