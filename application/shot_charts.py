#!/usr/bin/env python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import nbashots as nba

def main():
    all_players = nba.get_all_player_ids('all_data')

    player_data = {}
    for index, row in all_players.iterrows():
        print index, row['PERSON_ID']

        person_id = row['PERSON_ID']
        player_data[person_id] = {}
        player_data[person_id]['games'] = nba.PlayerLog(person_id).get_game_logs()
        print player_data[person_id]['games']
        break

if __name__ == '__main__':
    main()
