from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Allow all origins for CORS (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="Name of the country")):
    # Format Wikipedia URL
    wiki_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    
    # Fetch the page
    response = requests.get(wiki_url)
    if response.status_code != 200:
        return {"error": f"Could not fetch page for '{country}'."}

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract H1 to H6 headings
    headings = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(tag.name[1])
        text = tag.get_text().strip()
        if text:
            headings.append("#" * level + " " + text)

    # Construct Markdown outline
    markdown_outline = "## Contents\n\n" + "\n".join(headings)

    return {
        "country": country,
        "markdown_outline": markdown_outline
    }
