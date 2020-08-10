# Handle the parsing of game log data from retrosheet.org
# use this decoder: https://www.retrosheet.org/gamelogs/glfields.txt

import csv


def load_in_retrosheet(sheet_file: str) -> list:
    """
    import a file from retrosheet
    """
    game_list = []
    with open(sheet_file) as game_logs:
        game_data = csv.reader(game_logs)
        for game in game_data:
            game_list.append(game)
    return game_list


def result_parser(game_data: list) -> list:
    """
    return the teams and scores and game number for a game
    [away_team, away_score, game_number, home_team, home_score, home_game_number]
    """
    return [game_data[3], game_data[9], game_data[5], game_data[6], game_data[10], game_data[8]]


def extract_all_game_results(sheet_file: str) -> list:
    """
    function takes in a retrosheet for an entire season
    returns a list of every game in this format:
    [winning]
    """
    game_logs = load_in_retrosheet(sheet_file)
    results_list = []
    for log in game_logs:
        results_list.append(calculate_game_winner(result_parser(log)))
    return results_list


def calculate_game_winner(game_log):
    """
    Uses score to calculate game winner
    """
    if game_log[1] > game_log[-2]:
        return [game_log[0], game_log[-3]]
    else:
        return [game_log[-3], game_log[0]]
