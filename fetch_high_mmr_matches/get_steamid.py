import json
import dota2api
import pickle
import time

def import_json(filepath):
    json_data=open(filepath).read()
    return json.loads(json_data)

def write_list_to_file(filename,list_to_write):
    with open(filename, 'a') as fp:
        pickle.dump(list_to_write, fp)

def read_list_from_file(filename):
    with open(filename, 'r') as fp:
        return pickle.load(fp)

if __name__=="__main__":
    api_details = import_json('./api-key.json')
    api = dota2api.Initialise(api_details['key'])
    players_steamid = read_list_from_file('players_steamid')
    steamids = read_list_from_file('steamids')
    while True:
        matches = api.get_top_live_games()
        for match in matches['game_list']:
            print(match['average_mmr'])
            for player in match['players']:
                if player['account_id'] not in players_steamid:
                    players_steamid.append(player['account_id'])
                    try:
                        api.get_match_history(account_id=player['account_id'])
                        steamids.append(player['account_id'])
                    except Exception as exp:
                        print exp
        write_list_to_file('steamids',steamids)
        write_list_to_file('players_steamid',players_steamid)
        time.sleep(1800)
