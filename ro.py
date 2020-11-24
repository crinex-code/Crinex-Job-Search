import requests
import re
from bs4 import BeautifulSoup

# search for remote jobs from remoteok

BASE_URL = "https://remoteok.io"


def get_soup(term):
  url = f"{BASE_URL}/remote-dev+{term}-jobs"
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
  jobs_board = soup.find("table", id="jobsboard")
  job_listings = jobs_board.find_all("tr")
  for job in job_listings:
    job = extract_job(job)
    if job != None:
      jobs.append(job)
  return jobs



def extract_job(data):
  try:
    link = data.find("a", itemprop="url")['href']
    company = data.find("h3", itemprop="name").text
    title = data.find("h2", itemprop="title").text
    location = data.find("div", class_="location").text
    # try:
    #   logo = data.find("td", class_="has-logo")["src"]
    # except:
    #   logo = "None"
    return {
      'title': title,
      'company': company,
      'location': deEmojify(location).strip(),
      'link': f"{BASE_URL}{link}",
      # 'logo': logo
    }
  except:
    return None



# https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python
def deEmojify(text):
  regrex_pattern = re.compile(pattern = "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags = re.UNICODE)
  return regrex_pattern.sub(r'',text)




def get_jobs(term):
  print("Scraping Remote Jobs from RemoteOk....\n")
  jobs = extract_jobs(term)
  return jobs