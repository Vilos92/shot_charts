#!/usr/bin/env python
import os
import logging
import argparse
from collections import namedtuple
import matplotlib.pyplot as plt
#import seaborn as sns
import pandas as pd
import nbashots as nba

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--static', required=True, help='static path')

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

class Player(object):
    def __init__(self, person_id, full_name, first_name, last_name):
        self.person_id = person_id
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name

    def get_formatted_name(self):
        '''Format the name based on the presence of a last name'''
        return self.first_name + ' ' + self.last_name if self.last_name else self.first_name

    def get_save_name(self):
        '''Format a string for the file containing this player's shot chart'''
        save_name = self.first_name + ' ' + self.last_name if self.last_name else self.first_name
        save_name = save_name.replace(' ', '_')
        return save_name 

class ShotChartGenerator(object):
    '''Class for generating and saving shot charts for all NBA players'''
    def __init__(self, save_path):
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        self.save_path = save_path

        plt.rcParams['figure.figsize'] = (12, 11)

    def get_all_players(self):
        '''Return a list of all players of the NBA'''
        logger.info('Loading list of all players')
        all_players_pd = nba.get_all_player_ids('all_data')
        all_players = []
        for index, row in all_players_pd.iterrows():
            person_id = row['PERSON_ID']
            full_name = row['DISPLAY_LAST_COMMA_FIRST']
            first_and_last_name = row['DISPLAY_LAST_COMMA_FIRST'].split(', ')
            first_name = first_and_last_name[1] if len(first_and_last_name) > 1 else first_and_last_name[0]
            last_name = first_and_last_name[0] if len(first_and_last_name) > 1 else ''
            player = Player(person_id=person_id, full_name=full_name,
                            first_name=first_name, last_name=last_name)
            all_players.append(player)
        return all_players

    def save_shot_charts(self, players):
        '''Save a shot chart for every player'''
        for player in players:
            player_shots_df = nba.Shots(player.person_id).get_shots()
            if not player_shots_df.empty:
                print 'Creating shot chart for: {0}'.format(player.full_name)
                chart_title = '{0} FGA 2015-16 Season'.format(player.get_formatted_name())
                nba.shot_chart(player_shots_df.LOC_X, player_shots_df.LOC_Y,
                                title=chart_title)
                player_save_name = player.get_save_name()
                save_path = os.path.join(self.save_path, player_save_name + '.png')
                plt.savefig(save_path, bbox='tight')

def main():
    args = parser.parse_args()
    save_path = args.static

    shg = ShotChartGenerator(save_path)
    all_players = shg.get_all_players()
    shg.save_shot_charts(all_players)

if __name__ == '__main__':
    main()
