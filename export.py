import csv

def save_to_file(jobs, term):
  print(f"save_to_file:   {len(jobs)}")
  file = open(f"./csv/{term}.csv", mode='w')
  writer = csv.writer(file)
  writer.writerow(["title", "company", "location", "link"])
  for job in jobs:
    writer.writerow(list(job.values()))
  return