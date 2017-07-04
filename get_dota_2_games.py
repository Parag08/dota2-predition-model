import dota2
import json
import dota2api
import time
import csv
import warnings
'''
0	Unknown
1	All Pick
2	Captains Mode
3	Random Draft
4	Single Draft
5	All Random
6	Intro
7	Diretide
8	Reverse Captains Mode
9	The Greeviling
10	Tutorial
11	Mid Only
12	Least Played
13	New Player Pool
14	Compendium Matchmaking
15	Custom
16	Captains Draft
17	Balanced Draft
18	Ability Draft
19	Event 
20	All Random Death Match
21	Solo Mid 1 vs 1
22	Ranked All Pick
'''


csv_file = open("output.csv", "wb")
#csv_file = open("output.csv", "a")

def match_filter(match,min_duration=600,human_player=10):
    allowed_game_modes = [1,2,5,22]
    allowed_lobby_types = [0,2,5,6,7]
    if match['game_mode'] not in allowed_game_modes:
        return False
    if match['duration'] < min_duration:
        return False
    if match['lobby_type'] not in allowed_lobby_types:
        return False
    if match['human_players'] != human_player:
        return False
    for player in match['players']:
        if player['leaver_status'] != 0:
            return False
    return True



def add_game_to_csv(match):
    '''
    function to add dota game to CSV file. CSV file consist of coloums 1-118
    '''
    if match_filter(match) == False:
        return
    radiant_win = False
    if match['radiant_win'] == 'true':
        radiant_win = True
    radiant_team = []
    dire_team = []
    for player in match['players']:
        if player['player_slot'] < 100:
            radiant_team.append(player)
        else:
            dire_team.append(player)
    write_array = [0]*115
    for player in radiant_team:
        if radiant_win:
            write_array[int(player['hero_id'])] = 1
        else:
            write_array[int(player['hero_id'])] = -1
    for player in dire_team:
        if radiant_win:
            write_array[int(player['hero_id'])] = -1
        else:
            write_array[int(player['hero_id'])] = 1
    writer = csv.writer(csv_file)
    writer.writerow(write_array)

def get_matches(api,number_of_matches,start_at_match=2484255386):
    i = 0
    j = 0
    while i < number_of_matches:
         print(start_at_match,i,j)
         try:
            response_from_api = api.get_match_history_by_seq_num(start_at_match_seq_num=start_at_match)
            if response_from_api['status']==1 and response_from_api != None:
                start_at_match = response_from_api['matches'][99]['match_seq_num']
                i = i + len(response_from_api['matches'])
                for match in response_from_api['matches']:
                    add_game_to_csv(match)
            else:
                warnings.warn("response returned with wrong status code:",response_from_api['status'])
                break
         except Exception as exception:
            print exception
            start_at_match = start_at_match + j
            j = j + 1

json_data=open('./api-key.json').read()
api_details=json.loads(json_data) 
api = dota2api.Initialise(api_details['key'])
matches = get_matches(api,2000)
