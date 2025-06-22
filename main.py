from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route to show info
@app.get("/")
def read_root():
    return {"message": "Welcome to Country Outline API. Use /api/outline?country=India"}

# Main API endpoint
@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="Name of the country")):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "Wikipedia page not found"}

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.find("div", {"class": "mw-parser-output"})
    if not content:
        return {"error": "Content not found on Wikipedia page"}

    headings = content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    outline = ["## Contents", f"# {country}"]

    for tag in headings:
        level = int(tag.name[1])
        text = tag.get_text().strip()
        outline.append(f"{'#' * level} {text}")

    return {"outline": "\n".join(outline)}
