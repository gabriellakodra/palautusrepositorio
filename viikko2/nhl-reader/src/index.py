from rich.console import Console
from rich.table import Table
from player import PlayerReader, PlayerStats


def get_user_inputs():
    nationality = input("Nationality:").upper()
    season = input("Season:")
    return nationality, season


def get_players(nationality, season):
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    return stats.top_scorers_by_nationality(nationality)


def create_table(nationality, season):
    table = Table(title=f"Players: {nationality}, season {season}")
    table.add_column("Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("Team", justify="right", style="magenta")
    table.add_column("Goals", justify="right", style="green")
    table.add_column("Assists", justify="right", style="green")
    table.add_column("Points", justify="right", style="bold yellow")
    return table


def populate_table(table, players):
    for p in players:
        points = p.goals + p.assists
        table.add_row(p.name, p.team, str(p.goals), str(p.assists), str(points))


def main():
    console = Console()
    nationality, season = get_user_inputs()
    players = get_players(nationality, season)
    table = create_table(nationality, season)
    populate_table(table, players)
    console.print(table)


if __name__ == "__main__":
    main()
