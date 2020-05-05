# TapnSwap - Reinforcement Learning

### Jean-Remy Conti, ENS Paris-Saclay (France), 2020


This a personal project I did during the COVID-19 pandemic. It is based on a game I would often play with friends. An optimal policy is learned via Q-learning and the user may play against the trained agent (difficult level choice).


<p align="center">
  <img src="https://github.com/JRConti/TapnSwap-RL/blob/master/images/preview.png">
</p>

## Requirements

* Python
* Python basic libraries: numpy, os, time, matplotlib.


## Run the game 

Clone this repository and run `main.py`.

```
git clone https://github.com/JRConti/TapnSwap-RL
python TapnSwap-RL/main.py
```

The file `main.py` launches the game only, not the training part.

When playing in 1-player mode, the (very) easy level makes you play against a fully Random Agent while the difficult level makes you play against an agent trained by Q-learning.

The code for the game has been written (and tested) for Linux; there might be some problems with other OS even if the requirements are basic, so let me know if you encounter bugs by submitting an issue.


## Structure of repository

* `tapnswap.py`: back-end
* `interact.py`, `main.py`: front-end
* `agent.py`: defines the agent's behavior
* `train.py`, `validation.py`: training and optimization
* `Models`: saved Q-functions of different models with:
    * `Models/data`: saved counters of state-action pairs for each agent
    * `Models/train`: testing results of agents during training
    * `Models/results`: tournament reports between trained agents
* `doc`: source LaTeX code for `README.pdf`
* `images`: contains 2 sampled images.


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

Now let's consider a more complex example:

`Round of Player 1`

                Player 2                
                   |                    
              ||   |   ||||             
                   |                    
        L -------------------- R        
                   |                    
             |||   |   |                
                   |                    
                Player 1                

It is Player 1's round. Her hands have respectively 3 and 1 fingers while Player 2 has hands with 2 and 4 fingers. Player 1 can then tap with 3 or 1 on a hand of Player 2, that is on 2 or 4.

Player 1 is able to kill the hand of Player 2 with 2 fingers, by tapping with 3 on 2 (3+2 = 5 > 4). The next round is then:

`Round of Player 2`

                Player 1                
                   |                    
             |||   |   |                
                   |                    
        L -------------------- R        
                   |                    
                   |   ||||             
                   |                    
                Player 2                

Now Player 2 has lost a hand. Notice that Player 1 could have killed the hand of Player 2 which has 4 fingers instead, in the same way.

* Swap actions consist in exchanging some fingers of one of your hand to the other one.

To illustrate this process, let's come back to the previous complex example:

`Round of Player 1`

                Player 2                
                   |                    
              ||   |   ||||             
                   |                    
        L -------------------- R        
                   |                    
             |||   |   |                
                   |                    
                Player 1                

Instead of tapping with 1 or 3, Player 1 may swap some fingers from one of her hands to the other. By swapping 1 finger, Player 1 can obtain the configuration of hands 2-2 or 4-0. Let's look at the first possibility:

`Round of Player 1`

                Player 2                
                   |                    
              ||   |   ||||             
                   |                    
        L -------------------- R        
                   |                    
              ||   |   ||               
                   |                    
                Player 1                

By swapping, Player 1 gets the configuration of hands 2-2. Changing the hand that loses 1 finger, Player 1 could have obtained the configuration 4-0.

There is one main restriction to swap actions: swapping to an identical but reversed configuration is NOT allowed. For instance, in this case, Player 1 could not have swapped from 3-1 to 1-3, exchanging 2 fingers.

But it is still possible to exchange 2 fingers. For instance, a swap from 3-2 to 1-4 is a valid swap.

Note that it is also possible to revive a killed hand:

`Round of Player 1`

                Player 2                
                   |                    
              ||   |   |                
                   |                    
        L -------------------- R        
                   |                    
              ||   |                    
                   |                    
                Player 1                

In this case, Player 1 has one hand with 2 fingers and a killed hand. Exchanging 1 finger from the left to the right, Player 1 may revive the killed hand:

`Round of Player 1`

                Player 2                
                   |                    
              ||   |   |                
                   |                    
        L -------------------- R        
                   |                    
               |   |   |                
                   |                    
                Player 1                

That's all for the rules !


The code for the game can be found in:
1. `tapnswap.py`: back-end.
2. `interact.py`: utils functions for front-end.
3. `main.py`: front-end.


## Training and results

For details on the implementation, how the training is modeled, the experiments I have achieved alongside the corresponding results, see `README.pdf` file in this repo.


## Meta

Jean-Rémy Conti – jean-remy.conti@mines-paristech.fr

Distributed under the GNU license. See LICENSE for more information.


## Contributing

1. Fork it (https://github.com/JRConti/TapnSwap-RL/fork)
2. Create your feature branch: `git checkout -b feature/fooBar`
3. Commit your changes: `git commit -am 'Add some fooBar'`
4. Push to the branch: `git push origin feature/fooBar`
5. Create a new Pull Request

