import requests

# API address we can fill the parameters: platform, region and battle tag of a player to get their profile
url = 'https://ow-api.com/v1/stats/{}/{}/{}/complete'


class Overwatch:
    def __init__(self, platform, region, battle_tag):
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
        self.displayed_filters = ['Name', 'Level', 'Prestige', 'Rating', 'Endorsement Level', 'In-Game Stats',
                                  'Best In-Game Stats', 'Game Outcomes', 'Awards']
        self.api_filters.extend(
            ['name', 'level', 'prestige', 'rating', 'Endorsement Level', 'In-Game Stats', 'Best In-Game Stats',
             'Game Outcomes', 'Awards'])

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
        elif stat in ['cards', 'medals', 'medalsBronze', 'medalsSilver', 'medalsGold']:
            return self.result_json[game_mode]['awards'][stat]
        elif stat in ['gameWon', 'gamesLost', 'gamesPlayed']:
            return self.result_json[game_mode]['careerStats']['allHeroes']['game'][stat]
        elif stat in ['allDamageDoneMostInGame', 'barrierDamageDoneMostInGame', 'eliminationsMostInGame',
                      'healingDoneMostInGame', 'killsStreakBest', 'multikillsBest']:
            return self.result_json[game_mode]['careerStats']['allHeroes']['best'][stat]
        elif stat in ['barrierDamageDone', 'damageDone', 'deaths', 'eliminations', 'soloKills', 'objectiveKills']:
            return self.result_json[game_mode]['careerStats']['allHeroes']['combat'][stat]
        return self.result_json[stat]


ov = Overwatch('pc', 'us', 'cats-11481')
