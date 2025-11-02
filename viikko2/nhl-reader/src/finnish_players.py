import requests
from player import Player

def get_finnish_players():
    """Returns a list of Finnish NHL players."""
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()
    
    players = []
    for player_dict in response:
        player = Player(player_dict)
        players.append(player)
    
    # Filter for Finnish players
    finnish_players = []
    for player in players:
        if player.nationality == "FIN":
            finnish_players.append(player)
    
    return finnish_players

def show_finnish_players():
    """Prints all Finnish NHL players."""
    finnish_players = get_finnish_players()
    
    print("Finnish players:")
    for player in finnish_players:
        print(player)
    
    print(f"\nTotal Finnish players: {len(finnish_players)}")

if __name__ == "__main__":
    show_finnish_players()
