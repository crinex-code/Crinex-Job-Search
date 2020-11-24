import requests
from bs4 import BeautifulSoup


# search for remote jobs from stack overflow


def get_soup(term, page=0):
    URL = f"https://stackoverflow.com/jobs?r=true&q={term}&pg={page + 1}"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def is_remote(job_cell):
    captions = []
    caption_soups = job_cell.find("div", class_="fs-caption").find_all("div", class_="grid--cell")
    for caption in caption_soups:
        text = caption.text
        if text:
            captions.append(text)
    if "Remote" in captions:
        return True
    return False


def get_last_page(term):
    soup = get_soup(term)
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(data):
    job_cell = data.find("div", {"class": "fl1"})
    if is_remote(job_cell):
        title = job_cell.find("h2").find("a")["title"]
        company, location = job_cell.find("h3").find_all("span", recursive=False)
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        job_id = data["data-jobid"]
        # logo = data.find("img")
        # try:
        #   logo = logo['src']
        # except:
        #   logo = "None"
        return {
            'title': title,
            'company': company,
            'location': location,
            'link': f"https://stackoverflow.com/jobs/{job_id}",
            # 'logo': logo
        }


def extract_jobs(last_page, term):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO page: {page}")
        soup = get_soup(term, page)
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            if job:
                jobs.append(job)
    return jobs


def get_jobs(term):
    print("Scraping Remote Jobs from Stack Overflow....\n")
    last_page = get_last_page(term)
    print(f"Total SO page: {last_page}")
    jobs = extract_jobs(last_page, term)
    return jobs
