import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()


def fetch_and_format_players():
    # 1. Fetch official FPL API data
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    response = requests.get(
        url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502, detail="Failed to fetch from FPL API"
        )

    data = response.json()

    # 2. Map Team IDs and Element Types (Positions)
    teams = {t["id"]: t["name"] for t in data["teams"]}
    positions = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}

    # 3. Construct formatted JSON array matching your screenshot
    players_data = []
    for p in data["elements"]:
        player_obj = {
            "id": p["id"],
            "name": f"{p['first_name']} {p['second_name']}",
            "team": teams.get(p["team"], ""),
            "position": positions.get(p["element_type"], ""),
            "currentPrice": p["now_cost"] / 10,
            "chanceOfPlayingThisGW": (
                p["chance_of_playing_this_round"]
                if p["chance_of_playing_this_round"] is not None
                else 100
            ),
            "injuryStatus": p["status"],
            "injuryNews": p["news"] if p["news"] else "Fully Fit",
            "appearances": p.get("starts", 0),
            "minutesPlayed": p.get("minutes", 0),
            "defensiveContributions": (
                p.get("clearances", 0)
                + p.get("blocks", 0)
                + p.get("interceptions", 0)
                + p.get("tackles", 0)
            ),
            "goals": p.get("goals_scored", 0),
            "xG": str(p.get("expected_goals", "0.00")),
            "assists": p.get("assists", 0),
            "xA": str(p.get("expected_assists", "0.00")),
            "cleanSheets": p.get("clean_sheets", 0),
            "saves": p.get("saves", 0),
            "yellowCards": p.get("yellow_cards", 0),
            "redCards": p.get("red_cards", 0),
            "bonusPoints": p.get("bonus", 0),
            "penOrder": p.get("penalties_order", 0),
            "clearances": p.get("clearances", 0),
            "blocks": p.get("blocks", 0),
            "interceptions": p.get("interceptions", 0),
            "tackles": p.get("tackles", 0),
        }
        players_data.append(player_obj)

    return players_data


@app.get("/")
def home():
    return {"status": "online", "endpoint": "/players"}


@app.get("/players")
def get_players():
    return fetch_and_format_players()
