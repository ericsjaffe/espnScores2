import requests

url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
response = requests.get(url)
data = response.json()

# Extract and display game information
for event in data['events']:
    competition = event['competitions'][0]
    teams = competition['competitors']
    home_team = next(team for team in teams if team['homeAway'] == 'home')
    away_team = next(team for team in teams if team['homeAway'] == 'away')
    print(f"{away_team['team']['displayName']} vs {home_team['team']['displayName']}")
    print(f"Score: {away_team['score']} - {home_team['score']}")
    print(f"Status: {competition['status']['type']['description']}\n")
