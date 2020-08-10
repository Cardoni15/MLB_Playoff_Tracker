# handles importing data into the team classes
from retrosheet_tools import extract_all_game_results
from team_class import team_class
from mlb_league_dict import mlb_teams


class mlb_league:
    """
    contains every team in the MLB.
    there will be a list of team class objects
    """
    def __init__(self):
        self.teams = self.initialize_leage()

    def initialize_leage(self):
        """
        function to initialize each team
        """
        all_teams = []
        for league in mlb_teams:
            divisions = mlb_teams[league].keys()
            for division in divisions:
                for team in mlb_teams[league][division]:
                    team_obj = team_class(team, division, league)
                    all_teams.append(team_obj)
        return all_teams

    def import_season_data(self, retro_sheet: str):
        """
        provide a retro sheet to load in game data
        """
        game_results = extract_all_game_results(retro_sheet)
        for game in game_results:
            for team in self.teams:
                if team.team == game[0]:
                    team.add_win_loss(1)

                if team.team == game[1]:
                    team.add_win_loss(0)

    def get_team_record(self, your_team: str):
        """
        return win_loss list for team provided
        """
        for team in self.teams:
            if team.team == your_team:
                return team.win_loss

    def calculate_record_for_window(self, start_game: int, end_game: int):
        """
        update each teams number of wins over the window provided
        """
        for team in self.teams:
            team.return_num_wins(start_game, end_game)

    def calculate_window_over_season(self, window_size: int):
        """
        calculate every teams record over the window size for the entire MLB season
        """
        game_one = 0
        game_final = window_size - 1
        while game_final < 162:
            self.calculate_record_for_window(game_one, game_final)
            game_one = game_one + 1
            game_final = game_final + 1

    def calculate_playoff_teams_for_window(self, windowNum: int):
        """
        calculate 16 team playoffs for each 60 game window
        """
        wild_card_nl = []
        wild_card_al = []
        playoff_teams = []
        for league in mlb_teams:
            divisions = mlb_teams[league].keys()
            for division in divisions:
                tempDivision = []
                for team in mlb_teams[league][division]:
                    for teem in self.teams:
                        if teem.team == team:
                            tempDivision.append(teem)
                sort_by_rec = sorted(tempDivision, key=lambda x: x.window_records[windowNum], reverse=True)
                playoff_teams.append(sort_by_rec[0])
                playoff_teams.append(sort_by_rec[1])
                if league == 'nl':
                    wild_card_nl.append(sort_by_rec[2])
                    wild_card_nl.append(sort_by_rec[3])
                    wild_card_nl.append(sort_by_rec[4])
                if league == 'al':
                    wild_card_al.append(sort_by_rec[2])
                    wild_card_al.append(sort_by_rec[3])
                    wild_card_al.append(sort_by_rec[4])

        wildcard = sorted(wild_card_al, key=lambda x: x.window_records[windowNum], reverse=True)
        playoff_teams.append(wildcard[0])
        playoff_teams.append(wildcard[1])
        wildcard = sorted(wild_card_nl, key=lambda x: x.window_records[windowNum], reverse=True)
        playoff_teams.append(wildcard[0])
        playoff_teams.append(wildcard[1])

        return playoff_teams

    def calculate_playoff_teams_every_window(self, window: int):
        """
        calculate number of windows in a 162 game season.
        return a list of playoff team objects
        """
        all_playoff_teams = []
        for slice_ in range(0, 162-window):
            temp_playoff_teams = self.calculate_playoff_teams_for_window(slice_)
            all_playoff_teams.append(temp_playoff_teams)

        return all_playoff_teams
