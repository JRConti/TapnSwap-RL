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

<<<<<<< HEAD
For details on the implementation, how the training is modeled, the experiments I have achieved alongside the corresponding results, see `README.pdf` file in this repo.
=======
The training of the agent is done via Q-learning, which is a specific kind of Reinforcement Learning algorithm. In classical Reinforcement Learning, an agent evolves in an environment in the following way: starting from an intial state <img src="/tex/ac3148a5746b81298cb0c456b661f197.svg?invert_in_darkmode&sanitize=true" align=middle width=14.25802619999999pt height=14.15524440000002pt/>, the agent chooses an action <img src="/tex/007094eee0f16d09ce121fc2ba8e7107.svg?invert_in_darkmode&sanitize=true" align=middle width=15.24170009999999pt height=14.15524440000002pt/>, the environment responds to the agent by giving its new state <img src="/tex/286f7d4815c0996530bda7973b1ec5ea.svg?invert_in_darkmode&sanitize=true" align=middle width=14.25802619999999pt height=14.15524440000002pt/> and a reward <img src="/tex/1db75c795ab2c794f72bbe79b8113be1.svg?invert_in_darkmode&sanitize=true" align=middle width=13.96886699999999pt height=14.15524440000002pt/>. The same process keeps going for next time steps. At time step <img src="/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/>, the agent is in state <img src="/tex/1f1c28e0a1b1708c6889fb006c886784.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/>, chooses action <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/> and gets its next state <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/> and the corresponding reward <img src="/tex/39522195af502cac4f9d3a41f3e0f2ca.svg?invert_in_darkmode&sanitize=true" align=middle width=12.38211314999999pt height=14.15524440000002pt/> by the environment. 

#### The agent and the environment

In a 2-player game like TapnSwap, the agent is one player that should learn the optimal policy (or strategy). The environment is the entity that is impacted by the agent's actions and that responds to the agent by giving its new states and rewards. One trivial choice for the environment is the agent's opponent.

#### Current state <img src="/tex/1f1c28e0a1b1708c6889fb006c886784.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/>

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

the current state of the agent is `[[3,1], [2,4]]`. Note that the lists are firstly (agent then opponent) and secondly ordered (left hand then right hand). The initial state <img src="/tex/ac3148a5746b81298cb0c456b661f197.svg?invert_in_darkmode&sanitize=true" align=middle width=14.25802619999999pt height=14.15524440000002pt/> is `[[1,1], [1,1]]`.

#### Action <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/>

Actions in back-end (file `tapnswap.py`) are represented differently depending on whether they are tap or swap actions.

Tap actions are coded as `[0, tapping_hand, tapped_hand]` where `tapping_hand` is the hand of the agent involved in tap action (0: left hand, 1: right hand) and `tapped_hand` is the hand of the agent's opponent that receives the tap action from the agent (same binary coding).

Swap actions are coded as `[1, giving_hand, exchange_nbr]` where `giving_hand` is the hand of the agent that gives some of its fingers to the other hand (same binary coding as before) and `exchange_nbr` is the amount of such fingers.

In file `agent.py`, the agent initializes itself by creating an integer coding for all the actions in the previous format. At each time step, the agent gets the list of possible actions, code them in integers, chooses between them and send the decoded chosen action to back-end.

#### Next state <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/>

The next state of the agent is given by the environment after that the agent chooses the action <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/>. It is the configuration of hands obtained after the round of the agent's opponent which follows action <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/>.

#### Reward <img src="/tex/39522195af502cac4f9d3a41f3e0f2ca.svg?invert_in_darkmode&sanitize=true" align=middle width=12.38211314999999pt height=14.15524440000002pt/>

The most difficult task in Reinforcement Learning is often determining the rewards corresponding to each transition (<img src="/tex/1f1c28e0a1b1708c6889fb006c886784.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/>, <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/>, <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/>). In this game, it is difficult to find such rewards without adding bias to the learning process (which may not be optimal). Indeed, the sole purpose of killing 1 hand might not even be an optimal strategy at all ... Thus, I chose to give non-zero rewards to the agent if and only if the game came to an end (positive reward if game is won, negative reward if game is lost). 

#### RL

The agent's actions are determined by its policy <img src="/tex/f30fdded685c83b0e7b446aa9c9aa120.svg?invert_in_darkmode&sanitize=true" align=middle width=9.96010619999999pt height=14.15524440000002pt/> (such that <img src="/tex/287f09cd1f1159f393421ba5bfd52a99.svg?invert_in_darkmode&sanitize=true" align=middle width=72.63316169999999pt height=24.65753399999998pt/>) which depends only on the current state. For 1 game ending at <img src="/tex/6d49ffa8001d8d6e5f271531236ff434.svg?invert_in_darkmode&sanitize=true" align=middle width=39.74304179999999pt height=22.465723500000017pt/> and starting at state <img src="/tex/ac3148a5746b81298cb0c456b661f197.svg?invert_in_darkmode&sanitize=true" align=middle width=14.25802619999999pt height=14.15524440000002pt/>, the goal of the agent is to maximize the following quantity w.r.t. <img src="/tex/f30fdded685c83b0e7b446aa9c9aa120.svg?invert_in_darkmode&sanitize=true" align=middle width=9.96010619999999pt height=14.15524440000002pt/>:

<img src="/tex/36aa7b72a642b14006616d7dffcff10e.svg?invert_in_darkmode&sanitize=true" align=middle width=227.28611895pt height=32.256008400000006pt/>

It is the expected sum of rewards the agent gets starting at <img src="/tex/ac3148a5746b81298cb0c456b661f197.svg?invert_in_darkmode&sanitize=true" align=middle width=14.25802619999999pt height=14.15524440000002pt/>, following policy \pi. In this case, the expectation is on the new states <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/> given by the environment. The factor gamma gives the significance of first actions over last ones. The optimal policy <img src="/tex/4b9e818fb2bd9e00a29de1201046856b.svg?invert_in_darkmode&sanitize=true" align=middle width=16.69528244999999pt height=22.63846199999998pt/> has value <img src="/tex/1035b5e023eb4835c150ab0ae9c8073c.svg?invert_in_darkmode&sanitize=true" align=middle width=94.65245459999998pt height=22.63846199999998pt/> for all initial states.

#### Q-learning

The Q-function is defined similarly:

<img src="/tex/398d5bae28dff657fce0da8fef225a1f.svg?invert_in_darkmode&sanitize=true" align=middle width=368.60706959999993pt height=32.256008400000006pt/>

This algorithm approximates the optimal Q-function <img src="/tex/16fc7a524924fbd8f462b98c62e03ca7.svg?invert_in_darkmode&sanitize=true" align=middle width=94.15924319999999pt height=22.63846199999998pt/>. Note that the optimal policy is then given by <img src="/tex/299809f1cb41b9c203c7c02fe79b3713.svg?invert_in_darkmode&sanitize=true" align=middle width=182.01004304999998pt height=30.885828600000014pt/> where <img src="/tex/dc3b4885c72b12e5355875739438a2e0.svg?invert_in_darkmode&sanitize=true" align=middle width=21.98404889999999pt height=22.465723500000017pt/> is the set of possible actions at time <img src="/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/>.

The main idea of Q-learning is to build an estimator <img src="/tex/391f97230acf153493653a43407302bf.svg?invert_in_darkmode&sanitize=true" align=middle width=12.99542474999999pt height=31.141535699999984pt/> of the optimal Q-function <img src="/tex/27db7880334fb2af2631380f9a2a86f4.svg?invert_in_darkmode&sanitize=true" align=middle width=19.73061914999999pt height=22.63846199999998pt/>. At the beginning, the agent is initialized with a full-zero matrix <img src="/tex/b335455a748e1ce06e0f344013af6f9f.svg?invert_in_darkmode&sanitize=true" align=middle width=49.481371499999995pt height=31.141535699999984pt/> for all states <img src="/tex/6f9bad7347b91ceebebd3ad7e6f6f2d1.svg?invert_in_darkmode&sanitize=true" align=middle width=7.7054801999999905pt height=14.15524440000002pt/> and all actions <img src="/tex/44bc9d542a92714cac84e01cbbb7fd61.svg?invert_in_darkmode&sanitize=true" align=middle width=8.68915409999999pt height=14.15524440000002pt/>. Note that, in our case, we are in tabular setting (the number of distinct state-action pairs can be stored in the memory of a computer) so there is no need of Deep Learning. As one can observe from the definitions of states and actions for TapnSwap, there are 5^4 - 1 = 624 distinct states (the -1 is because the state `[[0,0], [0,0]]` is not possible) and 2^2 (tap) + 2 * 2 (all swap actions can be described with 1 or 2 exchanged fingers only) = 8 distinct actions. Thus, the estimator <img src="/tex/391f97230acf153493653a43407302bf.svg?invert_in_darkmode&sanitize=true" align=middle width=12.99542474999999pt height=31.141535699999984pt/> is a matrix of size 624 * 8.

The training consists in the agent playing <img src="/tex/f9c4988898e7f532b9f826a75014ed3c.svg?invert_in_darkmode&sanitize=true" align=middle width=14.99998994999999pt height=22.465723500000017pt/> games. For each game, the agent starts at state <img src="/tex/ac3148a5746b81298cb0c456b661f197.svg?invert_in_darkmode&sanitize=true" align=middle width=14.25802619999999pt height=14.15524440000002pt/> and, while the game is not over, it takes action <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/> at state <img src="/tex/1f1c28e0a1b1708c6889fb006c886784.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/> with <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/>-greedy policy (probability <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> of taking action randomly and <img src="/tex/bdb8f1d1c8fbdfe5abfdafd09a2b6227.svg?invert_in_darkmode&sanitize=true" align=middle width=34.98279179999999pt height=21.18721440000001pt/> of taking current optimal actions <img src="/tex/ee40176c047cddc88bed926f72ab837f.svg?invert_in_darkmode&sanitize=true" align=middle width=174.45294899999996pt height=31.141535699999984pt/>), observes next state <img src="/tex/b02dd36b8a10566f2a0ad9cbb2e74858.svg?invert_in_darkmode&sanitize=true" align=middle width=29.31519194999999pt height=14.15524440000002pt/> and reward <img src="/tex/39522195af502cac4f9d3a41f3e0f2ca.svg?invert_in_darkmode&sanitize=true" align=middle width=12.38211314999999pt height=14.15524440000002pt/>. It then computes the Temporal Difference (TD(0)):

<img src="/tex/c6c2700a7d419d8542f52c1b7cdf3159.svg?invert_in_darkmode&sanitize=true" align=middle width=249.27946229999998pt height=31.141535699999984pt/>

<img src="/tex/10ea9eec57d7dd8109d5e58e9baf6620.svg?invert_in_darkmode&sanitize=true" align=middle width=12.27173144999999pt height=22.831056599999986pt/> is an unbiased estimator of the Bellman error, which quantifies how far the estimator <img src="/tex/391f97230acf153493653a43407302bf.svg?invert_in_darkmode&sanitize=true" align=middle width=12.99542474999999pt height=31.141535699999984pt/> is from the optimal Q-function <img src="/tex/27db7880334fb2af2631380f9a2a86f4.svg?invert_in_darkmode&sanitize=true" align=middle width=19.73061914999999pt height=22.63846199999998pt/>. Thus, a simple way to minimize this error is to update the estimator <img src="/tex/391f97230acf153493653a43407302bf.svg?invert_in_darkmode&sanitize=true" align=middle width=12.99542474999999pt height=31.141535699999984pt/> at each time step in the following way:

<img src="/tex/7025c902cb087af97133123f761e498a.svg?invert_in_darkmode&sanitize=true" align=middle width=235.03187235pt height=31.141535699999984pt/>.

<img src="/tex/fad359da84968b88fe12f5c25aad557a.svg?invert_in_darkmode&sanitize=true" align=middle width=58.63782374999998pt height=24.65753399999998pt/> is the learning rate and should depend on the current state-action pair. Q-learning converges a.s. to the optimal Q-function if all state-action pairs are tried infinitely often with the learning rate satisfying Robbins-Monro conditions: I chose in this case <img src="/tex/cc17e057ec00474942c4dec1f59c75d3.svg?invert_in_darkmode&sanitize=true" align=middle width=120.95049449999998pt height=27.77565449999998pt/> where <img src="/tex/28482ad0cb6376e3f84dcd12260e6fe9.svg?invert_in_darkmode&sanitize=true" align=middle width=48.06132539999999pt height=24.65753399999998pt/> is the number of visits of the state-action pair (<img src="/tex/1f1c28e0a1b1708c6889fb006c886784.svg?invert_in_darkmode&sanitize=true" align=middle width=12.67127234999999pt height=14.15524440000002pt/>, <img src="/tex/9789555e5d8fa5de21171cc40c86d2cd.svg?invert_in_darkmode&sanitize=true" align=middle width=13.65494624999999pt height=14.15524440000002pt/>) from the agent. The decisions of the agent and the updates of the estimator <img src="/tex/391f97230acf153493653a43407302bf.svg?invert_in_darkmode&sanitize=true" align=middle width=12.99542474999999pt height=31.141535699999984pt/> are coded in file `agent.py`.

The whole process is repeated until the game is over, and for <img src="/tex/f9c4988898e7f532b9f826a75014ed3c.svg?invert_in_darkmode&sanitize=true" align=middle width=14.99998994999999pt height=22.465723500000017pt/> games. At the end, the near-optimal policy is <img src="/tex/60400de2b62cc30bc1ccca31ec74b309.svg?invert_in_darkmode&sanitize=true" align=middle width=179.93239274999996pt height=31.141535699999984pt/>.

An agent is thus fully determined by the pair (<img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/>, <img src="/tex/11c596de17c342edeed29f489aa4b274.svg?invert_in_darkmode&sanitize=true" align=middle width=9.423880949999988pt height=14.15524440000002pt/>) used during training. Note that <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> controls the trade-off between exploitation and exploration. 

#### The agent's opponent

The opponent is a significant feature for training as it is the environment in which the agent evolves. In file `train.py`, I implemented 2 different ways of training for an agent: playing against a fully Random Agent or playing against another version of itself. 

Note that usually, Q-learning is an off-policy method, meaning that the agent should adopt an <img src="/tex/7d064005e144808707a773a44d3d0529.svg?invert_in_darkmode&sanitize=true" align=middle width=36.80923124999999pt height=21.18721440000001pt/>-greedy policy. However, firstly because of flexibility and secondly because of the influence of <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> on the environment (when an agent plays against another version of itself), I chose to allow training for any value of <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/>.

#### Training in practice

In file `train.py`, I implemented a training function that allows to train any agent (determined by <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> and <img src="/tex/11c596de17c342edeed29f489aa4b274.svg?invert_in_darkmode&sanitize=true" align=middle width=9.423880949999988pt height=14.15524440000002pt/>) during the number of games (or epochs) you want, either vsRandom (fully Random Agent opponent) or vsSelf (playing against another version of itself). At the end of training, the function saves the learned Q-function in a CSV format located at `Models/filename.csv`. The typo for `filename` I used can be illustrated with an example: the file `Models/greedy_0_1_vsRandom.csv` stores the Q-function of an agent with <img src="/tex/436d9a3fbe125b99e3afb8e2aaa85347.svg?invert_in_darkmode&sanitize=true" align=middle width=49.59466544999998pt height=21.18721440000001pt/> training against a Random Agent while the file `Models/greedy_0_4_vsSelf.csv` stores the Q-function of an agent with <img src="/tex/209289d32e886caab81e1aed3c0b26b1.svg?invert_in_darkmode&sanitize=true" align=middle width=49.59466544999998pt height=21.18721440000001pt/> training against another version of itself. 

Note that <img src="/tex/11c596de17c342edeed29f489aa4b274.svg?invert_in_darkmode&sanitize=true" align=middle width=9.423880949999988pt height=14.15524440000002pt/> is not specified in the name of the CSV file because it is not a relevant parameter in our case. Indeed, since the only reward is at the end of the game, there is no need to weight some rewards compared to others.

The previous training function also stores the counter of state-action pairs encountered by an agent during training. For the latter example, the counter is stored at `Models/data/count_greedy_0_4_vsSelf.csv`.

Thus, I allowed the possibility of training an already trained model, importing the learned Q-function and the counter of encountered state-action pairs. It is also possible for the user to play on the shell with the learning agent DURING training as often as you want. In the same way, I allowed for a learning agent the possibility to play any number of games (without training on those) against a fully Random Agent during training, as a kind of evaluation of current training.


## Optimizer

The module Optimizer found in file `validation.py` is used as validation step for training agents via Q-learning. Training can be done for many values of <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> and for different opponents (Random Agent, Self and all sequences using those two). Indeed, it is possible to initialize the optimizer by setting `change_opp = True`, meaning that after 1 session of training of any agent vsRandom or vsSelf, the agents change their type of opponent for the following session of training. In this way, it is possible to alternate the 2 types of opponents during the whole training. For instance, an agent initialized with <img src="/tex/436d9a3fbe125b99e3afb8e2aaa85347.svg?invert_in_darkmode&sanitize=true" align=middle width=49.59466544999998pt height=21.18721440000001pt/> firstly trained vsRandom, then vsSelf, stores its learned Q-function in `Models/greedy_0_1_vsRandomvsSelf.csv`.

#### `grid_search`

The method `grid_search` of module Optimizer computes the fraction of an agent's wins over a given number of games against a Random Agent. This fraction is computed as a function of the number of games used for training the agent. It then provides a way of visualizing the progress made by all trained agents (different values of <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> and different opponents). 

For instance, here is what you can get by training an agent with <img src="/tex/93f08c4276891415d2a8149283706f4a.svg?invert_in_darkmode&sanitize=true" align=middle width=49.59466544999998pt height=21.18721440000001pt/> vs Self during 100 games:

![Training evolution](images/training.png)

At each epoch, the training agent has played 10000 games against a Random Agent and the fraction of wins is represented on the y-axis. One can observe that the agent reaches local maxima (different branch - perhaps still a good strategy - than the optimal policy) which may last 20 epochs forming a 'plateau', then performs worse followed by a great progress. Note that at each time that an agent is tested (here and in what follows), it chooses its actions with its version of optimal policy (that is <img src="/tex/3aebae27082f9d15d701d7068659dcb0.svg?invert_in_darkmode&sanitize=true" align=middle width=36.80923124999999pt height=21.18721440000001pt/>) so that the parameter <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> is only significant during training.

Those testing results obtained during training are stored in a txt file. For the previous example, the results of training are stored in `Models/train/GS_epsilon_0_8_vsSelf.txt`. In those txt files, each line corresponds to an epoch result in the format: epoch, score of training agent, number of finished games, number of played games. Note that, if the new trained agent loses against its old version (before the training), the method `grid_search` cancels the training and keeps the past version of the training agent. This may be useful in case of several sessions of training.
      
At the end of all trainings, the method `grid_search` simulates a tournament between all trained agents. Each agent plays 10 games against all others and the scores of each model against another 
are stored in a CSV file located at `Models/results/tournamentK.csv` where K is the number of tournaments the module Optimizer has simulated. A txt file is also generated using the previous CSV file: it displays rankings of each model, alongside its total score against all other models. Those files are located at `Models/results/tournamentK.txt`.

The method `grid_search` has an option `retrain` which, if set to True, does the previous process for already trained models. If the option `change_opp` is also set to True at the initialization of the module Optimizer, the already trained agents are retrained normally (first output) and retrained with a different opponent than before (second output) which may be useful to compare agents among which some alternate the type of their opponent. In this way, if you want to compare trained agents among which some alternate their type of opponent, it is necessary to initialize the Optimizer with `change_opp = True` and then firstly run the method `grid_search` with `retrain = False` (no model already trained for now) and secondly to run it another time but with `retrain = True`. 

#### `retrain_best_models`

Looking at the results of the tournaments output by the `grid_search` method, it is then possible to retrain some of the trained agents, according to their total score during the previous tournament.

The method `retrain_best_models` looks at the previous tournament ranking txt file and selects some of the best current models according to their total score. The selection is made by keeping the models that have a total score above a given fraction of the best total score.

It is worth noting that the values of <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> not represented by the corresponding selected best models are definitely discarded by the Optimizer. Once selected, those models are retrained for a given number of epochs, without playing against a Random Agent during training (as opposed to `grid_search` method), and eventually participate to a tournament, in the same way than before. Note that only the values of <img src="/tex/7ccca27b5ccc533a2dd72dc6fa28ed84.svg?invert_in_darkmode&sanitize=true" align=middle width=6.672392099999992pt height=14.15524440000002pt/> matter in the participation of agents in the next tournament and not their type of opponent. For instance, if an agent with <img src="/tex/436d9a3fbe125b99e3afb8e2aaa85347.svg?invert_in_darkmode&sanitize=true" align=middle width=49.59466544999998pt height=21.18721440000001pt/> previously trained vsRandom has performed very poorly in the previous tournament while, with the same value of <img src="/tex/18587b7e997ba95d733290f835ecc7ce.svg?invert_in_darkmode&sanitize=true" align=middle width=1544.49387345pt height=284.3835621pt/>\epsilon<img src="/tex/b79dc589a55d8afc77fe6cd6909cfa01.svg?invert_in_darkmode&sanitize=true" align=middle width=352.6124151pt height=22.831056599999986pt/>\epsilon = 0<img src="/tex/1906c292d3cd884865a87f4bf973cc80.svg?invert_in_darkmode&sanitize=true" align=middle width=709.2521039999999pt height=45.84475500000001pt/>\epsilon<img src="/tex/213811e74621ee6c676894da3dec00a7.svg?invert_in_darkmode&sanitize=true" align=middle width=2221.2019186499997pt height=47.67123240000001pt/>\epsilon$ vsRandom, vsSelf, vsRandomvsSelf and vsSelfvsRandom, each of them with a total number of training epochs equal to 10000. At the end, the method creates a tournament (`Models/results/tournament2.txt` in this repo) which compares all of current agents. The resulting rankings are strongly stochastic and depend a lot on the chance of having exploring and exploiting enough the trained agents got. This is not a problem since the purpose here is to approach the optimal policy as soon as possible.

After having trained the agents with 4 combinations of opponents (vsRandom, vsSelf, vsRandomvsSelf, vsSelfvsRandom) for 10000 epochs, I have runned the method `retrain_best_models` keeping all agents with a total score above 30% of the max total score in the previous tournament (`Models/results/tournament2.txt` in this repo) and training them for 40000 more epochs. The output is the file `Models/results/tournament3.txt`. 

Finally, I have runned this method 4 more times, each time training the best models during 50000 epochs and reducing the number of best models kept. The last output in this repo is `Models/results/tournament7.txt`. In order to look for the optimal policy, I kept going on my local machine but the total scores of the top 3 best models did not change so I decided to stop. Indeed, playing against the best models at this time showed me that it was enough.

#### Results

In fact, when playing against the previous best agents, I was not able to win if I was the player to make the first move. I think I have tried all possibilities when playing against my top agent (which I chose to be the difficult level on the game menu), without being able to win a single time (if I was the player to make the first move).

This project showed me that this game can be 'cracked', meaning that **there exists a strategy you could always win with, if you don't start**. This was one of my main interrogation about this game and, before this implementation, I was pretty close to the optimal policy since I have played this game a lot. For the sole purpose of discovering this strategy, this project was worth it.

As a consequence, if you let the trained agent start and that you apply the optimal policy, you are sure to win, meaning that all depends on who starts. However, this has led to an unforeseen negative point: in practice, all good performing agents were trained against another version of themselves (vsSelf) at some point (which is not surprising once the exploration is in the good direction) so that, without having found the full optimal policy (meaning that you always win in any configuration), they were able to win if they did not start. Thus, the trained agents that started during the training were sure to lose and did not explore other configurations than the ones explored in their current optimal policy. That's why it may be possible to win if you let the trained agent start, without applying the optimal policy (but not so easy !).

A way of improvement that I did not try is to forbid the optimal strategy (at some point or at the last move) to train agents in other configurations than the ones encountered in the optimal policy.
>>>>>>> d35276166d3ece0b1c0b3ba50eac3149b922b910


## Meta

Jean-Rémy Conti – jean-remy.conti@mines-paristech.fr

Distributed under the GNU license. See LICENSE for more information.


## Contributing

1. Fork it (https://github.com/JRConti/TapnSwap-RL/fork)
2. Create your feature branch: `git checkout -b feature/fooBar`
3. Commit your changes: `git commit -am 'Add some fooBar'`
4. Push to the branch: `git push origin feature/fooBar`
5. Create a new Pull Request

