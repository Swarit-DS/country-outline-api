from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="Country name")):
    url = f"https://en.wikipedia.org/wiki/{country}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Could not fetch Wikipedia page for {country}"}

    soup = BeautifulSoup(response.content, "html.parser")
    headings = soup.select(".mw-parser-output h2, .mw-parser-output h3, .mw-parser-output h4, .mw-parser-output h5, .mw-parser-output h6")

    markdown = f"## Contents\n\n# {country.capitalize()}\n"
    for heading in headings:
        level = int(heading.name[1])
        title = heading.get_text(strip=True).replace('[edit]', '')
        markdown += f"{'#' * level} {title}\n"

    return {"outline": markdown}
