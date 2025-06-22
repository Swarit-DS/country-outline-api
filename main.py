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
    content = soup.find("div", {"class": "mw-parser-output"})

    headings = content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    markdown = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])  # Extract number from h1, h2, etc.
        text = heading.get_text(strip=True)
        markdown += f"{'#' * level} {text}\n"

    return {"outline": markdown}
