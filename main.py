from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS for all origins
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
    
    # Find all headings inside the content area
    content_div = soup.find("div", {"class": "mw-parser-output"})
    if not content_div:
        return {"error": "Could not find content block on Wikipedia page."}

    headings = content_div.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])

    markdown = f"## Contents\n\n# {country.capitalize()}\n"

    for heading in headings:
        level = int(heading.name[1])
        title = heading.get_text(strip=True).replace('[edit]', '')
        markdown += f"{'#' * level} {title}\n"

    return {"outline": markdown}
