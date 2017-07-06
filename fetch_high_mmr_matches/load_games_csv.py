import pickle
import dota2api
import json
import time
import csv
import argparse

def get_list_of_steamid():
    with open ('steamids', 'r') as fp:
        return pickle.load(fp)

def read_json_file(filepath):
    json_data=open(filepath).read()
    return json.loads(json_data)

def fetch_games_data(api,file_dict,steamids,datatype):
    steamids = [steamids[0]]
    for steamid in steamids:
        try:
             result = api.get_match_history(account_id=steamid)
             matches = result['matches']
             for match in matches:
                 match_details = api.get_match_details(match['match_id'])
                 if 'csv' in datatype:
                     add_game_to_csv(match_details,file_dict['csv'],steamid)
                 if 'detailed' in datatype:
                     add_game_to_detailed_file(match_details,file_dict['detailed'],steamid)
                 if 'raw' in datatype:
                     add_game_to_raw_file(match_details,file_dict['raw'],steamid)
        except Exception as exp:
            print(exp)


def add_game_to_detailed_file(match,csv_file,steamid):
    players_team = None
    players_hero = None
    if match_filter(match) == False:
        return
    radiant_win = match['radiant_win']
    radiant_team = []
    dire_team = []
    for player in match['players']:
        if player['player_slot'] < 100:
            if player['account_id'] == steamid:
                players_team = True
                players_hero = player['hero_id']
            radiant_team.append(player)
        else:
            if player['account_id'] == steamid:
                players_team = False
                players_hero = player['hero_id']
            dire_team.append(player)
    write_array = []
    for player in radiant_team:
        write_array.append(int(player['hero_id']))
    for player in dire_team:
        write_array.append(int(player['hero_id']))
    write_array.append(match['match_id'])
    write_array.append(match['start_time'])
    write_array.append(radiant_win)
    write_array.append(players_hero)
    write_array.append(players_team==radiant_win)
    writer = csv.writer(csv_file)
    writer.writerow(write_array)

def add_game_to_raw_file(match,raw_file,steamid):
    if match_filter(match) == False:
        return
    match['steam-id'] = steamid
    json.dump(match, raw_file)
    



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


def add_game_to_csv(match,csv_file,steamid):
    '''
    function to add dota game to CSV file. CSV file consist of coloums 1-118
    '''
    players_team = None
    if match_filter(match) == False:
        return
    radiant_win = match['radiant_win']
    radiant_team = []
    dire_team = []
    for player in match['players']:
        if player['player_slot'] < 100:
            if player['account_id'] == steamid:
                players_team = True
            radiant_team.append(player)
        else:
            if player['account_id'] == steamid:
                players_team = False
            dire_team.append(player)
    write_array = [0]*115
    write_array[0] = int(radiant_win == players_team)
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


    
def openfile(data_type,mode="wb"):
    date = time.strftime("%d-%m-%Y")
    file_dict = {}
    for data in data_type:
        filename = './data/'+date + '_dota_games.'+data
        fo = open(filename,mode)
        file_dict[data] = fo
    return file_dict

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_type",
        default=['csv'],
        nargs='+',
        help="Valid model types: {'csv', 'detailed' ,'raw'}. \n usage: \n python load_games_csv.py --data_type detailed csv raw"
    )
    data_type = parser.parse_args().data_type
    steamids = get_list_of_steamid()
    file_dict = openfile(data_type)
    api = dota2api.Initialise(read_json_file('./api-key.json')['key'])
    fetch_games_data(api,file_dict,steamids,data_type)
