from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

def get_scores():
    url = "https://site.api.espn.com/apis/site/v2/sports/baseball/college-baseball/scoreboard"
    response = requests.get(url)
    data = response.json()

    games = []
    for event in data['events']:
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

@app.route("/")
def index():
    scores = get_scores()
    return render_template("index.html", scores=scores)

@app.route("/api/scores")
def api_scores():
    return jsonify(get_scores())

if __name__ == "__main__":
    app.run(debug=True)
