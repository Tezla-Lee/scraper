import csv
import json


def save_to_file_json(jobs, photos, city, gu):
    toJson(jobs, city, gu)
    toJson_photo(photos, city, gu)
    return


def toJson(lists, city, gu):
    with open(f"{city}_{gu}.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')


def toJson_photo(lists, city, gu):
    with open(f"{city}_{gu}_photo.json", 'w', encoding='utf-8') as file:
        json.dump(lists, file, ensure_ascii=False, indent='\t')


def save_to_file_csv(jobs, city, gu):
    file = open(f"{city}_{gu}.csv", mode="w")
    writer = csv.writer(file)
    # writer.writerow(
    #     ["city", "gu", "longitude", "latitude", "title", "capacity", "bathroomNum", "bedroomNum", "bedNum", "rating",
    #      "reviewNum", "buildingType", "accommodationType"])
    writer.writerow(
        ["city",
         "gu",
         "title",
         "bathroomNum",
         "bedroomNum",
         "bedNum",
         "price",
         "capacity",
         "contact",
         "latitude",
         "longitude",
         "locationDesc",
         "transportationDesc",
         "accommodationDesc",
         "hostDesc",
         "rating",
         "reviewNum",
         "accommodationType",
         "buildingType",
         "hostName",
         "hostReviewNum"])

    for job in jobs:
        writer.writerow(list(job.values()))

    file.close()
    return
