# TapnSwap - Reinforcement Learning

### Jean-Remy Conti, ENS Paris-Saclay (France), 2020


This a personal project I did during the COVID-19 pandemic. It is based on a game I would often play with friends. An optimal policy is learned via Q-learning and the user may play against the trained agent (difficult level choice).


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


## Structure of repository





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

Tap actions are coded as `[0, tapping_hand, tapped_hand]` where `tapping_hand` is the hand of the agent involved in tap action (0: left hand, 1: right hand) and `tapped_hand` is the hand of the agent's opponent that receives the tap action from the agent (same binary coding).

Swap actions are coded as `[1, giving_hand, exchange_nbr]` where `giving_hand` is the hand of the agent that gives some of its fingers to the other hand (same binary coding as before) and `exchange_nbr` is the amount of such fingers.

In file `agent.py`, the agent initializes itself by creating an integer coding for all the actions in the previous format. At each time step, the agent gets the list of possible actions, code them in integers, chooses between them and send the decoded chosen action to back-end.

#### Next state $s_{t+1}$

The next state of the agent is given by the environment after that the agent chooses the action $a_t$. It is the configuration of hands obtained after the round of the agent's opponent which follows action $a_t$.

#### Reward $r_t$

The most difficult task in Reinforcement Learning is often determining the rewards corresponding to each transition ($s_t$, $a_t$, $s_{t+1}$). In this game, it is difficult to find such rewards without adding bias to the learning process (which may not be optimal). Indeed, the sole purpose of killing 1 hand might not even be an optimal strategy at all ... Thus, I chose to give non-zero rewards to the agent if and only if the game came to an end (positive reward if game is won, negative reward if game is lost). 

#### RL

The agent's actions are determined by its policy $\pi$ (such that $a_t = \pi(s_t)$) which depends only on the current state. For 1 game ending at $t = T$ and starting at state $s_0$, the goal of the agent is to maximize the following quantity w.r.t. $\pi$:

$V^\pi(s_0) = \mathbb{E}[\sum_{t=0}^T \ \gamma^t \ r_t \ | \ \pi, \ s_0]$

It is the expected sum of rewards the agent gets starting at $s_0$, following policy \pi. In this case, the expectation is on the new states $s_{t+1}$ given by the environment. The factor gamma gives the significance of first actions over last ones. The optimal policy $\pi^\star$ has value $V^\star = \underset{\pi}{\text{max}} V^\pi$ for all initial states.

#### Q-learning

The Q-function is defined similarly:

$Q^\pi(s_t, a_t) = \mathbb{E}[\sum_{t'=t}^T \ gamma^(t'-t) \ r_{t'} \ | \ \pi, \ s_t, \ a_t]$

This algorithm approximates the optimal Q-function $Q^\star = \underset{\pi}{\text{max}} Q^\pi$. Note that the optimal policy is then given by $\pi^\star(s_t) = \underset{a \in \mathcal{A_t}}{\text{argmax}} Q^\star(s_t, a)$ where $\mathcal{A_t}$ is the set of possible actions at time $t$.

The main idea of Q-learning is to build an estimator $\hat{Q}$ of the optimal Q-function $Q^\star$. At the beginning, the agent is initialized with a full-zero matrix $\hat{Q}(s, a)$ for all states $s$ and all actions $a$. Note that, in our case, we are in tabular setting (the number of distinct state-action pairs can be stored in the memory of a computer) so there is no need of Deep Learning. As one can observe from the definitions of states and actions for TapnSwap, there are 5^4 - 1 = 624 distinct states (the -1 is because the state `[[0,0], [0,0]]` is not possible) and 2^2 (tap) + 2 * 2 (all swap actions can be described with 1 or 2 exchanged fingers only) = 8 distinct actions. Thus, the estimator $\hat{Q}$ is a matrix of size 624 * 8.

The training consists in the agent playing $N$ games. For each game, the agent starts at state $s_0$ and, while the game is not over, it takes action $a_t$ at state $s_t$ with $\epsilon$-greedy policy (probability $\epsilon$ of taking action randomly and $1-\epsilon$ of taking current optimal actions $\hat{\pi}^\star (s_t) = \underset{a \in \mathcal{A_t}}{\text{argmax}} \hat{Q}(s_t, a)$), observes next state $s_{t+1}$ and reward $r_t$. It then computes the Temporal Difference (TD(0)):

$\delta_t = r_t + \gamma \underset{a \in \mathcal{A_t}}{\text{max}} \hat{Q}(s_t, a) - \hat{Q}(s_t, a_t)$

$\delta_t$ is an unbiased estimator of the Bellman error, which quantifies how far the estimator $\hat{Q}$ is from the optimal Q-function $Q^\star$. Thus, a simple way to minimize this error is to update the estimator $\hat{Q}$ at each time step in the following way:

$\hat{Q}(s_t, a_t) = \hat{Q}(s_t, a_t) + \alpha(s_t, a_t)  \delta_t$.

$\alpha(s_t, a_t)$ is the learning rate and should depend on the current state-action pair. Q-learning converges a.s. to the optimal Q-function if all state-action pairs are tried infinitely often with the learning rate satisfying Robbins-Monro conditions: I chose in this case $\alpha(s_t, a_t) = \frac{1}{#(s_t, a_t)}$ where $#(s_t, a_t)$ is the number of visits of the state-action pair ($s_t$, $a_t$) from the agent. The decisions of the agent and the updates of the estimator $\hat{Q}$ are coded in file `agent.py`.

The whole process is repeated until the game is over, and for $N$ games. At the end, the near-optimal policy is $\hat{\pi}^\star(s_t) = \underset{a \in \mathcal{A_t}}{\text{argmax}} \ \hat{Q}(s_t, a)$.

An agent is thus fully determined by the pair ($\epsilon$, $\gamma$) used during training. Note that $\epsilon$ controls the trade-off between exploitation and exploration. 

#### The agent's opponent

The opponent is a significant feature for training as it is the environment in which the agent evolves. In file `train.py`, I implemented 2 different ways of training for an agent: playing against a fully Random Agent or playing against another version of itself. 

Note that usually, Q-learning is an off-policy method, meaning that the agent should adopt an $\epsilon = 1$-greedy policy. However, firstly because of flexibility and secondly because of the influence of $\epsilon$ on the environment (when an agent plays against another version of itself), I chose to allow training for any value of $\epsilon$.

#### Training in practice

In file `train.py`, I implemented a training function that allows to train any agent (determined by $\epsilon$ and $\gamma$) during the number of games (or epochs) you want, either vsRandom (fully Random Agent opponent) or vsSelf (playing against another version of itself). At the end of training, the function saves the learned Q-function in a CSV format located at `Models/filename.csv`. The typo for `filename` I used can be illustrated with an example: the file `Models/greedy_0_1_vsRandom.csv` stores the Q-function of an agent with $\epsilon = 0.1$ training against a Random Agent while the file `Models/greedy_0_4_vsSelf.csv` stores the Q-function of an agent with $\epsilon = 0.4$ training against another version of itself. 

Note that $\gamma$ is not specified in the name of the CSV file because it is not a relevant parameter in our case. Indeed, since the only reward is at the end of the game, there is no need to weight some rewards compared to others.

The previous training function also stores the counter of state-action pairs encountered by an agent during training. For the latter example, the counter is stored at `Models/data/count_greedy_0_4_vsSelf.csv`.

Thus, I allowed the possibility of training an already trained model, importing the learned Q-function and the counter of encountered state-action pairs. It is also possible for the user to play on the shell with the learning agent DURING training as often as you want. In the same way, I allowed the possibility for a learning agent to play any number of games (without training on those) against a fully Random Agent during training, as a kind of evaluation of current training.


## Optimizer




  #### vsRandomvsSelf








