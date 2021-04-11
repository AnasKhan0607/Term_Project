import requests
# API address we can fill the parameters: platform, region and battle tag of a player to get their profile
url = 'https://ow-api.com/v1/stats/{}/{}/{}/complete'


class Overwatch:
    def __init__(self, platform, region, battle_tag):
        self.information = [platform, region, battle_tag]
        # Send a request to the api to get information about the user profile
        self.result = requests.get(url.format(platform, region, battle_tag))
        # Convert to JSON (basically dictionary formatted info)
        self.result_json = self.result.json()
        # List of all filters for player to select
        self.displayed_filters = []
        self.api_filters = []
        self.sub_stats = []


    def get_filters(self):
        """
        Get the main filters(stats) available for a user to select to compare with another player.
        We don't really care about icon, level icon, etc. for this since they aren't stats used for comparision.

        :return: list of possible filters
        """

        # The primary filters
        self.displayed_filters = ['Name', 'Level', 'Prestige', 'Rating', 'Endorsement Level', 'In-Game Stats', 'Best In-Game Stats', 'Game Outcomes', 'Awards']
        self.api_filters.extend(['name', 'level', 'prestige', 'rating','Endorsement Level', 'In-Game Stats', 'Best In-Game Stats', 'Game Outcomes', 'Awards'])

        filter_dict = {}


        for x, stat in enumerate(self.displayed_filters):
            filter_dict[stat] = self.api_filters[x]

        #
        # for match_filter in ['quickPlayStats', 'competitiveStats']:
        #     qp_game_filters = []
        #     qp_award_filters = []
        #     qp_total_filters = []
        #     for qp_filter in self.result_json[match_filter]:
        #         if qp_filter == 'games':
        #             for game_filter in self.result_json[match_filter]['games']:
        #                 qp_game_filters.extend(([game_filter]))
        #             qp_total_filters.extend([qp_filter, qp_game_filters])
        #         elif qp_filter == 'awards':
        #
        #             for award_filter in self.result_json[match_filter]['awards']:
        #                 qp_award_filters.extend(([award_filter]))
        #
        #             qp_total_filters.extend([qp_filter, qp_award_filters])
        #     self.filters.extend([[match_filter, qp_total_filters]])
        return filter_dict

    # self.displayed_filters = ['Name', 'Level', 'Prestige', 'Rating', 'Endorsement Level', 'In-Game Stats',
    #                           'Best In-Game Stats', 'Game Outcomes', 'Awards']
    # self.api_filters.extend(
    #     ['name', 'level', 'prestige', 'rating', 'Endorsement Level', 'In-Game Stats', 'Best In-Game Stats',
    #      'Game Outcomes', 'Awards'])

    def get_stat(self, stat, game_mode):
        try:
            if stat == 'Name':
                return self.result_json['name']
            elif stat == 'Level':
                return self.result_json['level']
            elif stat == 'Endorsement Level':
                return self.result_json['endorsement']
            elif stat == 'Rating':
                return self.result_json['rating']
            elif stat == 'Prestige':
                return self.result_json['prestige']
            elif stat in ['cards', 'medals', 'medalsBronze', 'medalsSilver','medalsGold']:
                return self.result_json[game_mode]['awards'][stat]
            elif stat in ['gameWon', 'gamesLost', 'gamesPlayed']:
                return self.result_json[game_mode]['careerStats']['allHeroes']['game'][stat]
            elif stat in ['allDamageDoneMostInGame', 'barrierDamageDoneMostInGame', 'eliminationsMostInGame', 'healingDoneMostInGame', 'killsStreakBest', 'multikillsBest']:
                return self.result_json[game_mode]['careerStats']['allHeroes']['best'][stat]
            elif stat in ['barrierDamageDone', 'damageDone', 'deaths','eliminations','soloKills','objectiveKills']:
                return self.result_json[game_mode]['careerStats']['allHeroes']['combat'][stat]
            else:
                return self.result_json[stat]
        except TypeError:
            # If the api does not have the information associated with a profile
            return 'N/A'
        except KeyError:
            return 'N/A'





    # def analyze_stats(self, player):
        # """
        # analyze the stats of a player and return an integer value representing its final
        # score after evaluation
        #
        # :param player: Battle Tag of player
        # :return: evaluation score
        # """
        # if player == self.test_get_player_info()[0]:
        #     player_stats = self.test_get_player_info()
        #     return 0.6 * player_stats[1] + 0.8 * player_stats[2] + 0.8 * player_stats[3]  # example calculations
        # return "Invalid player"

    # def compare_2players(self, player1, player2):
    #     """
    #     compares stats of 2 players, and returns the winning player
    #
    #     :param player1: Battle Tag of player1
    #     :param player2: Battle Tag of player 2
    #     :return: player with higher stats, else return a message saying players are equal
    #     """
    #     if self.analyze_stats(player1) > self.analyze_stats(player2):
    #         return player1
    #     elif self.analyze_stats(player1) < self.analyze_stats(player2):
    #         return player2
    #     return "Players are equal in comparison"

# Example of a user who uses platform is pc, region us, and battle tag of player of cats-11481 in Overwatch


ov = Overwatch('pc', 'us', 'cats-11481')


