import pandas as pd

import os

total_colums = 115
heros_game_played = [0 for x in range(total_colums)]
heros_win_rate = [0.0 for x in range(total_colums)]
heros_sum = [0 for x in range(total_colums)]


def get_files_list(folder='./data/'):
    fileslist = os.listdir(folder)
    csv_list = []
    for csv in fileslist:
        if csv[-3:-1]+csv[-1] == 'csv':
            csv_list.append(folder+csv)
    return csv_list

def calculate_win_rate(df):
    win_rate = []
    win = 0
    lose = 0
    for value,summation in df.sum().iteritems():
        total = 0
        for index,count in df[value].value_counts().iteritems():
            if index == 1:
                win = count + 0.0 
            if index == -1:
                lose = count + 0.0
        try:
            win_rate.append(win/(lose+win))
        except Exception as exp:
            win_rate.append(0)
    return win_rate

def read_file(filename):
    return pd.read_csv(filename)
      

if __name__ == "__main__":
    file_list = get_files_list()
    df = read_file(file_list[0])
    win_rate = calculate_win_rate(df)
