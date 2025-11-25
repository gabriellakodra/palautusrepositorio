class TennisGame:
    LOVE = 0
    FIFTEEN = 1
    THIRTY = 2
    FORTY = 3
    GAME_POINT = 4

    ADVANTAGE_THRESHOLD = 1
    WIN_THRESHOLD = 2


    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_score = self.LOVE
        self.player2_score = self.LOVE

    def won_point(self, player_name):
        if player_name == "player1":
            self.player1_score = self.player1_score + 1
        else:
            self.player2_score = self.player2_score + 1

    def _scores_tied(self):
        return self.player1_score == self.player2_score

    def _end_game_scenario(self):
        return (
            self.player1_score >= self.GAME_POINT
            or self.player2_score >= self.GAME_POINT
        )

    def _tied_score_display(self):
        if self.player1_score == self.LOVE:
            return "Love-All"
        elif self.player1_score == self.FIFTEEN:
            return "Fifteen-All"
        elif self.player1_score == self.THIRTY:
            return "Thirty-All"
        else:
            return "Deuce"

    def _end_game_score_display(self):
        score_difference = self.player1_score - self.player2_score

        if score_difference == self.ADVANTAGE_THRESHOLD:
            return "Advantage player1"
        elif score_difference == -self.ADVANTAGE_THRESHOLD:
            return "Advantage player2"
        elif score_difference >= self.WIN_THRESHOLD:
            return "Win for player1"
        else:
            return "Win for player2"

    def _convert_score_to_tennis_term(self, score):
        if score == self.LOVE:
            return "Love"
        elif score == self.FIFTEEN:
            return "Fifteen"
        elif score == self.THIRTY:
            return "Thirty"
        elif score == self.FORTY:
            return "Forty"

    def _regular_score_display(self):
        player1_term = self._convert_score_to_tennis_term(self.player1_score)
        player2_term = self._convert_score_to_tennis_term(self.player2_score)
        return f"{player1_term}-{player2_term}"

    def get_score(self):
        if self._scores_tied():
            return self._tied_score_display()
        elif self._end_game_scenario():
            return self._end_game_score_display()
        else:
            return self._regular_score_display()
