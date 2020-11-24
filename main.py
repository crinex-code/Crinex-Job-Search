from urllib.parse import quote, unquote
from flask import Flask, render_template, request, redirect, send_file
from so import get_jobs as get_so_jobs
from wwr import get_jobs as get_wwr_jobs
from ro import get_jobs as get_ro_jobs
from export import save_to_file
"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=c%23
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""

db = {}
app = Flask("FINALE")


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/search")
def search():
  term = quote(request.args.get("term"))
  if term:
    existing_term = db.get(term)
    if existing_term:
      jobs = existing_term
    else:
      jobs = get_so_jobs(term) + get_wwr_jobs(term) + get_ro_jobs(term)
      db[term] = jobs
  else:
    return redirect("/")
  return render_template("search.html", term=unquote(term), jobs=jobs, total=len(jobs))

@app.route("/export")
def export():
  term = request.args.get("term")
  if term:
    term = term.lower()
    jobs = db.get(term)
    if jobs:
      save_to_file(jobs, term)
      return send_file(f"./csv/{term}.csv", as_attachment=True)
    else:
      return redirect("/")


# will redirect invalid urls to the 404 page
@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html"), 404


app.run()

