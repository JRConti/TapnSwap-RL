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


## Training

The training of the agent is done via Q-learning, which is a specific kind of Reinforcement Learning algorithm. In classical Reinforcement Learning, an agent evolves in an environment in the following way: starting from an intial state $s_0$, the agent chooses an action $a_0$, the environment responds to the agent by giving its new state $s_1$ and a reward $r_0$. The same process keeps going for next time steps. At time step $t$, the agent is in state $s_t$, chooses action $a_t$ and gets its next state $s_{t+1}$ and the corresponding reward $r_t$ by the environment.

#### The agent and the environment

In a 2-player game like TapnSwap, the agent is one player that should learn the optimal policy (or strategy). The environment is the entity that is impacted by the agent's actions and that responds to the agent by giving its new states and rewards. One trivial choice for the environment is the agent's opponent.

#### Current state $s_t$

The current state of the agent is a list of 2-sized lists containing the number of fingers of each hand. For instance, if the current configuration is:

`Round of Agent`

            Agent's opponent                
                   |                    
              ||   |   ||||             
                   |                    
        L -------------------- R        
                   |                    
             |||   |   |                
                   |                    
                 Agent                

the current state of the agent is `[[3,1], [2,4]]`. Note that the lists are firstly (agent then opponent) and secondly ordered (left hand then right hand). The initial state $s_0$ is `[[1,1], [1,1]]`.

#### Action $a_t$

Actions in back-end (file `tapnswap.py`) are represented differently depending on whether they are tap or swap actions.

Tap actions are coded as `[0, tapping_hand, tapped_hand]` where `tapping_hand` is the hand of the agent involved in tap action (0: left hand, 1: right hand) and `tapped_hand`: is the hand of the agent's opponent that receives the tap action from the agent (same binary coding).

Swap actions are coded as `[1, giving_hand, exchange_nbr]` where `giving_hand` is the hand of the agent that gives some of its fingers to the other hand (same binary coding as before) and `exchange_nbr` is the amount of such fingers.

In file `agent.py`, the agent initializes itself by creating an integer coding for all the actions in the previous format. At each time step, the agent gets the list of possible actions, code them in integers, chooses between them and send the decoded chosen action to back-end.

#### Next state $s_{t+1}$

The next state of the agent is given by the environment after that the agent chooses the action $a_t$. It is the configuration of hands obtained after the round of the agent's opponent which follows $a_t$.

#### Reward $r_t$

The most difficult task in Reinforcement Learning is often determining the rewards corresponding to each transition ($s_t$, $a_t$, $s_{t+1}$). In this game, it is difficult to find such rewards without adding bias to the learning process (which may not be optimal). Indeed, the sole purpose of killing 1 hand might not even be an optimal strategy at all ... Thus, I chose to give rewards to the agent if and only if the game came to an end (positive reward if game is won, negative reward if game is lost).






