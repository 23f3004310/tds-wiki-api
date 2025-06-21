from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
def get_country_outline(country: str = Query(...)):
    url = f"https://en.wikipedia.org/wiki/{country}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Could not fetch Wikipedia page for {country}"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})
    headings = content.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    outline = [f"{'#' * int(h.name[1])} {h.get_text().strip()}" for h in headings]
    return {"markdown": "\n".join(outline)}
