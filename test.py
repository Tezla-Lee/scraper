import json
import os


def add_data(accomms, num, city, start_id):
    file_path = f"json/{city}/통합/숙박/{str(num)}_{city}_{str(start_id)}.json"
    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)
    except:
        with open(file_path, 'w') as file:
            try:
                json_data = json.load(file)
            except:
                json_data = []

    print(json_data)
    for accomm in accomms:
        json_data.append(accomm)

    with open(file_path, 'w') as outfile:
        json.dump(json_data, outfile, ensure_ascii=False, indent='\t')

    file.close()
    outfile.close()


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


make_directory("대구")
add_data([{"name": "이재복"},{"name": "ㅁㄴㅇ"}], 1, "대구", 135)