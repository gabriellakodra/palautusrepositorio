from player import PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table 

def main():
    console = Console()

    nationality = input("Nationality:").upper()
    season = input("Season:")

    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    players = stats.top_scorers_by_nationality(nationality)

    table = Table(title=f"Players: {nationality}, season {season}")

    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Team", justify="right", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="green")
    table.add_column("Points", justify="right", style="bold yellow")

    for p in players:
        points = p.goals + p.assists
        table.add_row(p.name, p.team, str(p.goals), str(p.assists), str(points))

    console.print(table)    
    

if __name__ == "__main__":
    main()
