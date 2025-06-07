from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

SPORTS = {
    "College Baseball": "https://site.api.espn.com/apis/site/v2/sports/baseball/college-baseball/scoreboard",
    "College Softball": "https://site.api.espn.com/apis/site/v2/sports/softball/college-softball/scoreboard",
    "Men's Basketball": "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard",
    "Women's Basketball": "https://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/scoreboard",
    "College Football": "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard",
    "Men's Ice Hockey": "https://site.api.espn.com/apis/site/v2/sports/hockey/mens-college-hockey/scoreboard"
}

def fetch_scores(url):
    try:
        response = requests.get(url)
        data = response.json()

        games = []
        for event in data.get("events", []):
            competition = event['competitions'][0]
            teams = competition['competitors']
            home = next(t for t in teams if t['homeAway'] == 'home')
            away = next(t for t in teams if t['homeAway'] == 'away')

            games.append({
                "home_team": home['team']['displayName'],
                "home_score": home['score'],
                "away_team": away['team']['displayName'],
                "away_score": away['score'],
                "status": competition['status']['type']['description']
            })
        return games
    except Exception as e:
        print(f"Error fetching from {url}: {e}")
        return []

@app.route("/")
def index():
    all_scores = {}
    for sport_name, api_url in SPORTS.items():
        all_scores[sport_name] = fetch_scores(api_url)
    return render_template("index.html", all_scores=all_scores)

@app.route("/api/scores")
def api_scores():
    all_scores = {}
    for sport_name, api_url in SPORTS.items():
        all_scores[sport_name] = fetch_scores(api_url)
    return jsonify(all_scores)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # for Render deployment compatibility
    app.run(debug=True, host="0.0.0.0", port=port)
