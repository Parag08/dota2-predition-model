<b>someone else beat me to it so I am no longer continuing this please go to following link https://github.com/andreiapostoae/dota2-predictor </b>
this project it dicontinued as of 10-07-2017

sudo pip install dota2api
sudo pip install requests

chapter: data collection

step-1:- get steam-id of 100 top MMR players

step-2:- get games played by following players in last 7.00 patch

step-3:- enter them into the csv-files

[ to do:-                                                                      ]
[things to look at load_data should always load data whenever list is updated  ]
[force process termination should be garcefully handled                        ]
[how should the data be loaded into the model?                                 ]
chapter: data loading

step-1:- read all csv files

step-2:- select features

chapter: training the graph

step-1:- train the model with linear regression

step-2:- save the model

chapter: prediction

step-1:- get steam-id(optional)

step-2:- get games of player(optional)

step-3:- train model with player history(optional)

step-4:- let user input the 10 heros in the game

step-5:- based on 10 heros predict win probability
