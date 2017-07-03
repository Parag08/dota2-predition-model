import dota2
import json
import dota2api
import time
import csv
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

allowed_game_modes = [1,2,5,22]

csv_file = open("output.csv", "wb")

def add_game_to_csv(match):
    '''
    function to add dota game to CSV file. CSV file consist of coloums 1-118
    '''
    if match['game_mode'] not in allowed_game_modes:
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





json_data=open('./api-key.json').read()
api_details=json.loads(json_data) 
api = dota2api.Initialise(api_details['key'])
matches = api.get_match_history_by_seq_num(start_at_match_seq_num=2484255385)
if matches['status']==1:
    matches =  matches['matches']
#print json.dumps(matches[0])
#print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(matches[0]['start_time']))

for match in matches:
    add_game_to_csv(match)
