# main interface for reporting out on playoff teams
from statistics import mean, mode
import pprint as p

from league_data import mlb_league
from team_class import team_class
from mlb_league_dict import mlb_teams


def calculate_win_stats(playoff_teams: list):
    """
    calculate the average amount of wins based on every 16 team playoff bracket.
    """
    i = 0
    wins_list = []
    for slice_ in playoff_teams:
        for team in slice_:
            wins_list.append(team.window_records[i])
        i = i + 1

    avg_wins = int(mean(wins_list))
    mode_wins = mode(wins_list)
    min_wins = min(wins_list)
    max_wins = max(wins_list)

    print([avg_wins, mode_wins, min_wins, max_wins])


def calculate_unique_teams(playoff_teams: list):
    """
    returns number of unique playoff teams over every 60 game window last season.
    """
    team_list = []
    for slice_ in playoff_teams:
        for team in slice_:
            team_list.append(team.team)
    unique_teams = set(team_list)
    print(len(unique_teams))
    return unique_teams


def calculate_playoff_team_frequency(playoff_teams: list):
    """
    calculate frequency of playoff appearance for each team.
    """
    playoff_dict = {}
    print(len(playoff_teams))
    for slice_ in playoff_teams:
        print(len(slice_))
        for team in slice_:
            if team.team in playoff_dict:
                playoff_dict[team.team] += 1

            else:
                playoff_dict[team.team] = 1
    playoff_dict = sorted(playoff_dict.items(), key=lambda x: x[1], reverse=True)

    return playoff_dict


def calculate_losers(playoff_teams: set):
    """
    uses the MLB league dict to see who is missing.
    """
    all_teams = []
    for league in mlb_teams:
        divisions = mlb_teams[league].keys()
        for division in divisions:
            for team in mlb_teams[league][division]:
                all_teams.append(team)
    print(len(all_teams))
    for team in all_teams:
        if team not in playoff_teams:
            print(team)


# initialize the league, import retro sheet data, calculate 60 game playoff window, generate stats

mlb_2019 = mlb_league()
mlb_2019.import_season_data('GL2019.TXT')
mlb_2019.calculate_window_over_season(60)
playoff_teams = mlb_2019.calculate_playoff_teams_every_window(60)

calculate_win_stats(playoff_teams)
unique_teams = calculate_unique_teams(playoff_teams)
calculate_losers(unique_teams)
p.pprint(calculate_playoff_team_frequency(playoff_teams))
