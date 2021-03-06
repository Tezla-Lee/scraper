import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"


def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all('a')
    # print(links)
    pages = []
    for link in links[0:-1]:
        print(link)
        # pages.append(int(link.string))
    # max_page = pages[-1]
    # print(max_page)
    return links


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    # print(title)
    company = html.find("span", {"class": "company"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
    else:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {'title': title, 'company': company, 'location': location, 'link': f"https://kr.indeed.com/viewjob?jk={job_id}"}


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed page: {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    # print(results)
    # for result in results:
    #     title = result.find("div", {"class": "title"})
    #     print(title.find("a").string)
    return jobs


def get_jobs():
    last_page = extract_pages()
    jobs = extract_jobs(last_page)
    return jobs