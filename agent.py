"""
TapnSwap game.
Module Agent defines the agent's behaviour during games, along with 
their updates in case of training. It is possible to load an already 
trained model. The RL Agent is trained via Q-learning.
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU 
# General Public License along with this program.  
# If not, see <https://www.gnu.org/licenses/>.

import numpy as np

class Agent:
  """
  Class of agent used to play with user and used for training.
  """

  def __init__(self):
    pass

  def random_action(self, actions):
    """
    Gives a random action among a list of possible actions.

    Parameter
    ---------
    actions: list
      List of actions in TapnSwap format.

    Return
    ------
    Random action within the list actions (same format than
    format used by TapnSwap).
    """

    # Fix seed
    np.random.seed()

    return actions[ np.random.randint(0, len(actions)) ]

  def choose_action(self, state, actions, greedy = False):
    pass

  def update_Q(self, raw_state, raw_action, reward, raw_next_state):
    pass


class RandomAgent(Agent):
  """
  Class of random agent.
  """

  def choose_action(self, states, actions, greedy = False):
    """
    Choose a purely random action among possible actions.
    """

    return self.random_action(actions)


class RLAgent(Agent):
  """
  Class of agent trained by Q-learning.
  """

  def __init__(self, epsilon = 0.0, gamma = 1.0):
    """
    Build a coder and decoder of states and actions from 
    TapnSwap format to integers.

    Parameters
    ----------
    epsilon: float (in [0,1])
      Fraction of greedy random decisions.
    gamma: float (in [0,1])
      Factor of significance of first actions over last ones.
    """

    # Get integer coding of each state of original format
    # [ [hand0_p0, hand1_p0], [hand0_p1, hand1_p1] ]
    self.build_state_coder()

    # Get integer coding of each action of original format
    # [0/1, 0/1, 0/1/2]
    self.build_action_coder()

    # Init Q function
    n_states = len(self.state_coder)
    n_actions = len(self.action_coder)
    self.Q = np.zeros( (n_states, n_actions) )
    self.count_state_action = np.zeros( (n_states, n_actions) )

    # Parameters of agent
    self.epsilon = epsilon
    self.gamma = gamma


  def build_state_coder(self):
    """
    Build a dictionary {state: idx} where: 
    * state is a tupled version of the state in format given by 
      TapnSwap instance -> ex: ( (1,1), (1,1) ).
    * idx is its coding integer.
    """

    # First build list of states for 1 pair of hands
    list_states_pair0_diff = [ [i,j] for i in range(5) for j in range(5) 
                                if i != j  ] 
    list_states_pair0_eq = [ [i,j] for i in range(5) for j in range(5) 
                                if (i == j)] 
    list_states_pair0 = list_states_pair0_diff + list_states_pair0_eq 

    # Then build list of states for 2 pairs
    list_states = [ tuple(( tuple(state_pair0), tuple(state_pair1) ))
                    for state_pair0 in list_states_pair0 
                    for state_pair1 in list_states_pair0 ]

    # Build dictionary
    self.state_coder = {state: i for i, state in enumerate(list_states)}


  def build_action_coder(self):
    """
    Build a dictionary {action: idx} where:
    * action is a tupled version of the action in format given by
      TapnSwap instance -> ex: (0,1,0).
    * idx is its coding integer.
    """

    # Build list of all actions
    list_actions_tap = [ tuple([0, i, j]) for i in range(2) 
                          for j in range(2) ]
    list_actions_swap = [ tuple([1, i, j]) for i in range(2) 
                          for j in range(1,3) ]
    list_actions = list_actions_tap + list_actions_swap

    # Build dictionary
    self.action_coder = {action: i for i, action in enumerate(list_actions)}


  def code_state(self, raw_state):
    """
    Code raw state from TapnSwap format to 
    agent state format (integer) using dictionary state_coder.

    Parameter
    ---------
    raw_state: list
      State in TapnSwap format -> ex: [ [1,2], [3,4] ]. 

    Return
    ------
    Corresponding state in agent format (int).
    """

    # Tupled version of raw state
    raw_state_t = tuple(( tuple(raw_state[0]), tuple(raw_state[1])  ))    
    assert raw_state_t in self.state_coder.keys(), \
    'The state {} is not in dictionary of states.'.format(raw_state_t)
    return self.state_coder[ raw_state_t ]


  def code_actions(self, raw_actions):
    """
    Code raw actions from TapnSwap format to 
    agent actions format (integers) using dictionary action_coder.

    Parameter
    ---------
    raw_actions: list
      List of actions to code. Each action in the list 
      is in the TapnSwap format -> ex: [0,1,1].

    Return
    ------
    List of int: Corresponding actions in agent format.
    """

    # If there is only 1 raw_action in raw_actions
    if type( raw_actions[0] ) != list:
      raw_actions = [ raw_actions ]

    # Tupled version of raw_actions
    raw_actions_t = [ tuple( raw_action ) for raw_action in raw_actions ] 
    problem_actions = [raw_action_t for raw_action_t in raw_actions_t 
                        if raw_action_t not in self.action_coder.keys() ]
    assert len(problem_actions) == 0, \
    'The actions {} are not in dictionary of actions.'.format(problem_actions)
    return [ self.action_coder[raw_action_t] 
            for raw_action_t in raw_actions_t ]


  def decode_action(self, action):
    """
    Decode action from agent format to TapnSwap format.

    Parameter
    ---------
    action: int
      Action in agent format (integers found in dictionary
      action_coder).

    Return
    ------
    Corresponding action in TapnSwap format.
    """

    # Tupled version of action, found in dictionary of actions
    action_t = list(self.action_coder.keys())[
              list(self.action_coder.values()).index(action)]
    assert type(action_t) == tuple, \
    'Several actions returned by RL agent: {}'.format(action_t)
    # Decoding into TapnSwap format
    return list(action_t)


  def decode_state(self, state):
    """
    Decode state from agent format to TapnSwap format. 

    Parameter
    ---------
    state: int
      State in agent format (integer found in dictionary 
      state_coder).

    Return
    ------
    Corresponding state in TapnSwap format.
    """

    # Tupled version of state, found in dictionary of states
    state_t = list(self.state_coder.keys())[
              list(self.state_coder.values()).index(state)]
    # Decoding into TapnSwap format
    return list(state_t)


  def choose_action(self, raw_state, raw_actions, greedy = False):
    """
    Choose an epsilon-greedy action at current state among a 
    list of possible actions.

    Parameters
    ----------
    raw_state: list
      Current state in TapnSwap format.
    raw_actions: list
      List of possible current actions in TapnSwap format.
    greedy: boolean
      If set to True, it gives epsilon-greedy decisions
      while, if set to False, it gives optimal decisions.

    Return
    ------
    raw_action: list
      Action chosen by agent in TapnSwap format.
    """

    # Coding of state   
    state = self.code_state(raw_state)

    # Coding of actions
    actions = self.code_actions(raw_actions)

    # greedy = True  -> epsilon-greedy policy
    # greedy = False -> current optimal policy
    epsilon = float(greedy) * self.epsilon
    
    # Exploration   
    np.random.seed()
    if np.random.random() <= epsilon:
      assert greedy == True, \
      'Agent is epsilon greedy while it should not !'
      action = self.random_action(actions)
    
    # Exploitation
    else:
      action_idx = np.argmax( self.Q[state, actions]  )
      action = actions[action_idx]

    # Decoding into TapnSwap format
    raw_action = self.decode_action(action)

    return raw_action


  def update_Q(self, raw_state, raw_action, reward, raw_next_state):
    """
    Update of Q function using Temporal Difference
    on current transition with dynamic learning rate.

    Parameters
    ----------
    raw_state: list
      Current state in TapnSwap format.
    raw_action: list
      Current actions in TapnSwap format.
    reward: float
      Current reward.
    raw_next_state: list
      Next state in TapnSwap format.
    """

    # Decoding into agent format
    state = self.code_state(raw_state)
    action = self.code_actions(raw_action)
    next_state = self.code_state(raw_next_state)

    # Compute Temporal Difference (TD)
    delta_t = (reward + 
              self.gamma * max(self.Q[next_state, :]) - 
              self.Q[state, action])
    # Update learning rate
    self.count_state_action[state, action] += 1
    lr = 1.0/float( self.count_state_action[state, action] )

    #Update Q value
    self.Q[state, action] +=  lr * delta_t


  def load_model(self, filename):
    """
    Load trained model of format CSV in which is stored 
    the trained matrix Q and the counter of state-action pairs
    for future training. Update the variables self.Q and 
    self.count_state_action.

    Parameter
    ---------
    filename : string
      The path to Q matrix CSV file is ./Models/filename.csv 
      while the counter of state-action pairs is located at 
      ./Models/data/filename.csv.
    """

    # Load arrays as numpy arrays
    self.Q = np.loadtxt('Models/' + filename + '.csv', delimiter=',')
    self.count_state_action = np.loadtxt(
      'Models/data/count_' + filename + '.csv', delimiter=',')
