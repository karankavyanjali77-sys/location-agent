from mcp.server.fastmcp import FastMCP
import httpx
from google.cloud import bigquery

mcp = FastMCP("zoo-server")

@mcp.tool()
async def get_animal_info(animal_name: str) -> dict:
    """Fetch animal data from BigQuery zoo dataset."""
    client = bigquery.Client()
    query = f"""
        SELECT name, species, habitat, diet, conservation_status
        FROM `your_project.zoo_dataset.animals`
        WHERE LOWER(name) LIKE LOWER('%{animal_name}%')
        LIMIT 5
    """
    results = client.query(query).result()
    return {"animals": [dict(row) for row in results]}

@mcp.tool()
async def get_wikipedia_summary(topic: str) -> str:
    """Fetch a summary from Wikipedia."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic
        )
        data = resp.json()
        return data.get("extract", "No summary found.")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
