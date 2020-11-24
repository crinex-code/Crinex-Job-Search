import requests
# import re
from bs4 import BeautifulSoup

# search for remote jobs from weworkremotely

BASE_URL = "https://weworkremotely.com"

def get_soup(term):
  url = f"{BASE_URL}/remote-jobs/search?term={term}"
  try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
  except Exception as e:
    print(f"ERROR: get_soup({term})\n{e}")
    return ''



def extract_jobs(term):
  jobs = []
  soup = get_soup(term)
  jobs_container = soup.find("div", class_="jobs-container")
  job_listings = jobs_container.find_all("li")
  for job in job_listings:
    job = extract_job(job)
    if job != None:
      jobs.append(job)
  return jobs



def extract_job(data):
  try:
    link = data.find("a", recursive=False)['href']
    company = data.find("span", class_="company").text
    title = data.find("span", class_="title").text
    location = data.find("span", class_="region").text
    # logo = data.find("div", class_="flag-logo")
    # try:
    #   # find url btw round brackets()
    #   logo = re.search("\(([^)]*)\)", logo["style"]).group(1)
    # except:
    #   logo = "None"
    return {
      'title': title,
      'company': company,
      'location': location,
      'link': f"{BASE_URL}{link}",
      # 'logo': logo
    }
  except:
    return None



def get_jobs(term):
  print("\nScraping Remote Jobs from We Work Remotely....\n")
  jobs = extract_jobs(term)
  return jobs
