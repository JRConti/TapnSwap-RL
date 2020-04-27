# TapnSwap - Reinforcement Learning

### Jean-Remy Conti, ENS Paris-Saclay (France), 2020


This a personal project I did during the COVID-19 pandemic. It is based on a game I would often play with friends. An optimal policy is learned via Q-learning and the user may play against the trained agent (difficult level choice).


## Requirements

* Python
* Python basic libraries: numpy, os, time, matplotlib


## Run the game 

Clone this repository and run `main.py`.

```
git clone https://github.com/JRConti/TapnSwap-RL
python TapnSwap-RL/main.py
```

The file `main.py` launches the game only, not the training part.


## Description of the game

You may skip this part if you want to play: the rules of the game are explained to you when launching the game.

TapnSwap is a 2-player game. Both players have a variable number of fingers on both of their hands. If one player has a hand composed of more than 4 fingers, this hand is "killed". The goal of the game is to kill both hands of the opponent player.

#### First round

Each player starts with 1 finger on each hand and one of them has to make the first move. The configuration of hands is then:

` Round of Player 1 `

                Player 2                
                   |                    
               |   |   |                
                   |                    
        L -------------------- R        
                   |                    
               |   |   |                
                   |                    
                Player 1  

Both players are separated from each other by the horizontal line. The main vertical line separates the hands of both players (L: left hands, R: right hands). There is currently 1 finger on each hand of each player.

#### Actions

At each round of the game, each player has to choose an action among the list of possible actions. There are 2 main kinds of actions: tap and swap.

* Tap actions involve adding the number of fingers on one of your hands to one of your opponent's hands.

For instance, with the previous initial configuration, Player 1 may tap only with 1 (both of Player 1's hands have 1 finger) on 1 (both of Player 2's hands have 1 finger). If it happens, the configuration of hands at the next round is then:

`Round of Player 2`

                Player 1                
                   |                    
               |   |   |                
                   |                    
        L -------------------- R        
                   |                    
              ||   |   |                
                   |                    
                Player 2                

Player 2 had 1 finger on each hand but Player 1 tapped with 1 so now Player 2 has one hand with 1+1 = 2 fingers.



The code for the game can be found in:
1. `tapnswap.py`: back-end.
2. `interact.py`: util functions for front-end.
3. `main.py`: front-end.


## Training




