from pathlib import Path
import json

from fastmcp import FastMCP

mcp = FastMCP("Connoisseur-Server")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def data_path(filename: str) -> Path:
    path = DATA_DIR / filename
    if path.exists():
        return path
    raise FileNotFoundError(f"No se encontró {filename} en {DATA_DIR}")


def load_json(filename: str) -> list[dict]:
    with data_path(filename).open(encoding="utf-8") as file:
        return json.load(file)


@mcp.tool()
def get_restaurant_info(restaurant_name: str) -> str:
    """Busca un restaurante por nombre y devuelve sus datos estructurados."""
    query = restaurant_name.lower().strip()
    matches = [
        restaurant
        for restaurant in load_json("structured-restaurant-data.json")
        if query in restaurant["name"].lower() or restaurant["name"].lower() in query
    ]
    if not matches:
        return json.dumps({
            "status": "not_found",
            "message": f"No restaurant found matching '{restaurant_name}'.",
        }, indent=2)
    return json.dumps({"status": "found", "count": len(matches), "results": matches}, indent=2)


@mcp.tool()
def recommend_by_vibe(vibe: str) -> str:
    """Encuentra restaurantes por ambiente, etiquetas o descripción."""
    query = vibe.lower().strip()
    matches = []
    for restaurant in load_json("structured-restaurant-data.json"):
        tags = [tag.lower() for tag in restaurant.get("vibes", [])]
        description = restaurant.get("description", "").lower()
        if any(query in tag for tag in tags) or query in description:
            matches.append({
                "name": restaurant["name"],
                "neighborhood": restaurant.get("neighborhood"),
                "cuisine": restaurant.get("cuisine"),
                "rating": restaurant.get("rating"),
                "vibes": restaurant.get("vibes", []),
                "price_range": restaurant.get("price_range"),
            })
    excerpts = [
        paragraph.strip()[:300]
        for paragraph in data_path("California-Culinary-Map.txt").read_text(encoding="utf-8").split("\n\n")
        if query in paragraph.lower() and paragraph.strip()
    ]
    return json.dumps({
        "vibe_searched": vibe,
        "structured_matches": matches,
        "raw_text_excerpts": excerpts[:5],
    }, indent=2)


@mcp.tool()
def get_review(restaurant_name: str) -> str:
    """Devuelve la reseña disponible de un restaurante."""
    query = restaurant_name.lower().strip()
    review = next(
        (item for item in load_json("augmented-user-review.json")
         if query in item["restaurant_name"].lower()),
        None,
    )
    if review is None:
        return json.dumps({
            "status": "not_found",
            "message": f"No review found for '{restaurant_name}'.",
        }, indent=2)
    return json.dumps({
        "status": "found",
        "restaurant": review["restaurant_name"],
        "reviewer": review["reviewer"],
        "rating": review["rating"],
        "review_text": review["review_text"],
        "image_description": review.get("image_description", "N/A"),
        "visit_date": review.get("visit_date", "N/A"),
    }, indent=2)


if __name__ == "__main__":
    mcp.run()
