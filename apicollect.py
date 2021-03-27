import requests
# API address we can fill the parameters: platform, region and battle tag of a player to get their profile
url = 'https://ow-api.com/v1/stats/{}/{}/{}/profile'


class Overwatch:
    def __init__(self, platform, region, battle_tag):
        # Send a request to the api to get information about the user profile
        self.result = requests.get(url.format(platform, region, battle_tag))
        # Convert to JSON (basically dictionary formatted info)
        self.result_json = self.result.json()
        # List of all filters for player to select
        self.filters = []

    def get_filers(self):
        """
        Get the main filters(stats) available for a user to select to compare with another player.
        We don't really care about icon, level icon, etc. for this since they aren't stats used for comparision.

        :return: list of possible filters
        """

        # The primary filters
        self.filters.extend(['name', 'level', 'prestige', 'rating', 'gamesWon'])

        #
        for match_filter in ['quickPlayStats', 'competitiveStats']:
            qp_game_filters = []
            qp_award_filters = []
            qp_total_filters = []
            for qp_filter in self.result_json[match_filter]:
                if qp_filter == 'games':
                    for game_filter in self.result_json[match_filter]['games']:
                        qp_game_filters.extend(([game_filter]))
                    qp_total_filters.extend([qp_filter, qp_game_filters])
                elif qp_filter == 'awards':

                    for award_filter in self.result_json[match_filter]['awards']:
                        qp_award_filters.extend(([award_filter]))

                    qp_total_filters.extend([qp_filter, qp_award_filters])
            self.filters.extend([[match_filter, qp_total_filters]])
        return self.filters

    def test_get_player_info(self):
        """
        This is just a simple example of how to make API requests for demonstration purposes.
        :return:
        """
        if self.result:
            name = self.result_json['name']
            games_won = self.result_json['gamesWon']
            level = self.result_json['level']
            rating = self.result_json['rating']
            return [name, games_won, level, rating]
        return None

    def analyze_stats(self, player):
        """
        analyze the stats of a player and return an integer value representing its final
        score after evaluation

        :param player: Battle Tag of player
        :return: evaluation score
        """
        if player == self.test_get_player_info()[0]:
            player_stats = self.test_get_player_info()
            return 0.6 * player_stats[1] + 0.8 * player_stats[2] + 0.8 * player_stats[3]  # example calculations
        return "Invalid player"

    def compare_2players(self, player1, player2):
        """
        compares stats of 2 players, and returns the winning player

        :param player1: Battle Tag of player1
        :param player2: Battle Tag of player 2
        :return: player with higher stats, else return a message saying players are equal
        """
        if self.analyze_stats(player1) > self.analyze_stats(player2):
            return player1
        elif self.analyze_stats(player1) < self.analyze_stats(player2):
            return player2
        return "Players are equal in comparison"

# Example of a user who uses platform is pc, region us, and battle tag of player of cats-11481 in Overwatch


ov = Overwatch('pc', 'us', 'cats-11481')
ov.get_filers()
print("hey")
print("testing push")
