# team_class holds all of the win loss data for each team

class team_class:
    """
    team_class holds team, wins and losses list, team division, team league
    """
    def __init__(self, team: str, division: str, league: str):
        self.team = team
        self.division = division
        self.league = league
        self.win_loss = []
        self.window_records = []

    
    def import_win_loss_list(self, w_l_list: list):
        """
        import a win loss list sorted by game number (1-162)
        """
        self.win_loss = w_l_list


    def return_num_wins(self, start_game, end_game):
        """
        return number of wins between a start and end game number
        """
        num_wins = 0
        try:
            game_window = self.win_loss[(start_game - 1):(end_game - 1)]
            for game in game_window:
                num_wins = game + num_wins

        except IndexError:
            return False

        self.window_records.append(num_wins)
        return num_wins


    def add_win_loss(self, result):
        """
        Append a game to the win lost list
        """
        self.win_loss.append(result)


    def return_num_wins_for_window(self, window: int):
        """
        return num wins per window
        """
        self.window_records[window]