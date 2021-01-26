import csv


def save_to_file(jobs):
    file = open("air.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title", "img", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    file.close()
    return
