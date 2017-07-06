import pickle
import dota2api
import json
import time
import csv

def get_list_of_steamid():
    with open ('steamids', 'r') as fp:
        return pickle.load(fp)

def read_json_file(filepath):
    json_data=open(filepath).read()
    return json.loads(json_data)

def fetch_games_data(api,csv_file,steamids):
    for steamid in steamids:
        try:
             result = api.get_match_history(account_id=steamid)
             matches = result['matches']
             for match in matches:
                 match_details = api.get_match_details(match['match_id'])
                 add_game_to_csv(match_details,csv_file,steamid)
        except Exception as exp:
            print(exp)

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
    radiant_win = False
    if match['radiant_win'] == 'true':
        radiant_win = True
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


    
def openfile(mode="wb"):
    date = time.strftime("%d-%m-%Y")
    filename = './data/'+date + '_dota_games.csv'
    fo = open(filename,mode)
    return fo

if __name__=='__main__':
    steamids = get_list_of_steamid()
    csv_file = openfile()
    api = dota2api.Initialise(read_json_file('./api-key.json')['key'])
    fetch_games_data(api,csv_file,steamids)
