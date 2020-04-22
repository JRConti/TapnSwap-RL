"""
TapnSwap game.
Functions used to manage games between 2 agents, with possibility of 
training, of watching the games, of playing with an agent during 
training, of testing an agent during training by making it play 
against another agent and of saving the learned Q-function in 
CSV format. It is possible to train an already trained model.
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU 
# General Public License along with this program.  
# If not, see <https://www.gnu.org/licenses/>.

from tapnswap import TapnSwap
from interact import game_1vsAgent, show_score
from agent import Agent, RandomAgent, RLAgent
import numpy as np
import time

def game_2Agents(agent1, agent2, start_idx = -1, train = True, 
        time_limit = None, n_games_test = 0,
        play_checkpoint_usr = False, verbose = False):
  """
  Manages a game between 2 agents (agent1, agent2) potentially 
  time-limited, with possibility to train them, to confront 1 of 
  them through a game with user before the game between the 2 agents 
  (agent1, agent2) and to test 1 of them through several games 
  against a Random Agent after the game between the 2 agents 
  (agent1, agent2).

  Parameters
  ----------
  agent1, agent2: instances of Agent
    Agents involved in the game.
  start_idx: -1, 0 or 1
    Index of the agent that starts the game 
    (0: agent1, 1: agent2, -1: random).
  train: boolean
    Set to True to train both agents.
  time_limit: int
    Maximum number of rounds between the 2 agents 
    (possibility of loops with optimal actions).
    Avoid to set it to 0 in case of identical agents.
  n_games_test: int
    Number of games between agent1 and a Random Agent following
    the game between agent1 and agent2.
  play_checkpoint_usr: boolean
    Set to True for a game between the user and agent1 
    preceding the game between agent1 and agent2.
  verbose: boolean
    Set to True for a written explanation of each round.

  Return
  ------
  game_over: boolean.
  winner: index of winner agent (0: agent1, 1: agent2, -1: tie).
  test_results: list of int
    Only working if n_games_test > 0 (otherwise empty list 
    by default). If n_games_test > 0:
    * test_results[0]: number of finished games.
    * test_results[1]: number of games = n_games_test.
    * test_results[2]: score of agent1.
    * test_results[3]: score of Random Agent.
  """

  tapnswap = TapnSwap()
  tapnswap.reset()

  # Time of pause between several actions (if verbose)
  delay = 2

  # Preliminary game with the user 
  if play_checkpoint_usr:
    game_1vsAgent(tapnswap, 'test player', agent1, greedy = False)
    tapnswap.reset()
  
  # Select starting player
  if start_idx == -1:
    np.random.seed()
    player_idx = np.random.randint(0,2)
  else:
    assert start_idx == 0 or start_idx == 1, \
    'The starting agent index must be 0, 1 or -1.'
    player_idx = start_idx

  agents = [agent1, agent2]
  names = ['Agent1', 'Agent2']

  count_rounds = 0
  prev_state = []
  prev_action = []

  # Start game
  game_over = False
  while not game_over:
    if verbose:
      # Print current configuration
      show_score(tapnswap, names, 1 - player_idx, invert = False)
      time.sleep(delay)

    # Get current state
    hands = tapnswap.show_hands().copy()
    state = [ hands[player_idx], hands[1 - player_idx] ]
    # Choose action
    actions = tapnswap.list_actions(player_idx)
    action = agents[player_idx].choose_action(state, actions, 
                                              greedy = train)
    # Take action and get reward
    reward = tapnswap.take_action(player_idx, action)

    if verbose:
      # Print chosen action
      seq = str(names[player_idx])
      if action[0] == 0:
        seq = seq + str(' tapped with ' + 
                str(hands[player_idx, action[1]]) + ' on ' + 
                str(hands[1 - player_idx, action[2]]))
      else:
        new_hands = tapnswap.show_hands().copy()
        seq = seq + str(' swapped ' + str(hands[player_idx][0]) + 
                '-' + str(hands[player_idx][1]) + ' for ' + 
                str(new_hands[player_idx][0]) + '-' + 
                str(new_hands[player_idx][1]))
      print(seq)
      time.sleep(delay)
      print()
      # Print new configuration
      show_score(tapnswap, names, player_idx)
      time.sleep(delay)
      # Print corresponding reward
      print('Reward of ', names[player_idx], ' : ', reward)
      time.sleep(delay)
      print('----------------------------')

    game_over, winner = tapnswap.game_over()

    # Training
    if train:
      # Get new state
      next_hands = tapnswap.show_hands().copy()
      next_state = [ next_hands[player_idx], next_hands[1 - player_idx] ]
      # Train playing agent for a winning move
      if game_over:
        agents[player_idx].update_Q(state, action, reward, next_state)
      # Train waiting agent (response of the environment)
      if count_rounds:
        # New state in other's agent point of view
        inv_next_state = [ next_hands[1 - player_idx], 
                    next_hands[player_idx] ]
        # Each waiting agent receives the transition with the 
        # response of the environment for the new state
        agents[1 - player_idx].update_Q(prev_state, prev_action, 
                                        - reward, inv_next_state)
      # Keep in memory previous state and action
      prev_state = state
      prev_action = action

    # Avoid loops
    if time_limit is not None:
      if count_rounds > time_limit and not game_over:
        game_over = True
        winner = -1

    # Next round
    player_idx = 1 - player_idx
    count_rounds += 1

  # Test of agent1
  test_results = []
  if bool(n_games_test):
    random_agent = RandomAgent()
    test_results = compare_agents(agent1, random_agent, 
                                  n_games = n_games_test, 
                                  time_limit = None, verbose = False)

  return game_over, winner, test_results


def compare_agents(agent1, agent2, n_games, time_limit = None, verbose = True):
  """
  Manages competitive games between 2 agents and return final scores.

  Parameters
  ----------
  agent1, agent2: instances of Agent.
  n_games: int
    Number of games used to compare both agents.
  time_limit: int (or None)
    Maximum number of rounds between the 2 agents (possibility of 
    loops with optimal actions).
  verbose: boolean
    Set to True to know which of the n_games is currently played.

  Return
  ------
  results: list of int
    results[0]: number of finished games.
    results[1]: number of games = n_games.
    results[2]: score of agent1.
    results[3]: score of agent2.
  """

  start_idx = 0
  scores = [0,0]

  # Start games
  if verbose:
    print('Number of games:')

  for game in range(1, n_games + 1):
    if game % (n_games // 10) == 0 and verbose:
      print(game, '/', n_games)

    game_over, winner, _ = game_2Agents(agent1, agent2, 
                                        start_idx = start_idx, 
                                        train = False, 
                                        time_limit = time_limit, 
                                        n_games_test = 0, 
                                        play_checkpoint_usr = False, 
                                        verbose = False)
    # Update scores
    if winner in [0,1]:
      scores[winner] += 1

    start_idx = 1 - start_idx

  # Output results
  results = [scores[0]+scores[1], n_games, scores[0], scores[1]]

  return results


def train(n_epochs, epsilon, gamma, load_model, filename, random_opponent, 
      n_games_test, freq_test, n_skip_games = int(0), verbose = False):
  """
  Train 2 agents by making them play and learn together. Save the
  learned Q-function into CSV file. It is possible to confront 1 of 
  the agents (against either the user or a Random Agent) during 
  training, as often as one wants. It is also possible to train an already 
  trained model.

  Parameters
  ----------
  n_epochs: int
    Number of games used for training.
  epsilon: float (in [0,1])
    Fraction of greedy decisions during training of the 2 RL Agents.
  gamma: float (in [0,1])
    Factor of significance of first actions over last ones for the 
    2 RL Agents.
  load_model: string
    CSV filename in which is stored the learned Q-function of an 
    agent. If load_model = 'model', the function loads the model 
    './Models/model.csv'. If load_model is not None, the previous 
    parameters epsilon and gamma are used for a second training.
  filename: string
    Name of the CSV file that will store the learned Q-function 
    of one of the agents. The path to CSV file is 
    then ./Models/filename.csv. The counter of state-action
    pairs is also stored at ./Models/data/count_filename.csv for
    future training.
  random_opponent: boolean
    If set to true, the function trains 1 RL Agent by making it 
    play against a Random Agent. Otherwise, the RL agent is
    trained by playing against another version of itself.
  n_games_test: int
    Number of games one of the RL Agent plays against a Random Agent
    for testing. If set to 0, the RL Agents will not be tested by a 
    Random Agent. 
  freq_test: int
    Number of epochs after which one of the RL Agents plays n_games_test
    games against a Random Agent. If set to 1000, each 1000 epochs of
    training, one of the RL Agents is tested against a Random Agent.
    If set to 0, test occurs at the last epoch of training only.
    If set to -1, none of the agents is tested during training.
  n_skip_games: int 
    Number of epochs after which the user can choose to play 
    against one of the learning agents. If set to 1000, 
    each 1000 games, the user can choose to play against 
    one agent. If set to 0, the user can choose to play against one 
    agent at the last epoch only. If set to -1, no choice is offered 
    and the user cannot test any agent.
  verbose: boolean
    If set to True, each game action during training has a 
    written explanation.

  Return
  ------
  learning_results: list
    Only significant with n_games_test > 0 (otherwise, empty list 
    by default). List of each n_epochs // freq_test epoch test results 
    against a Random Agent. Each test result is a list: 
    [current epoch, score of RL Agent, number of finished games, 
    n_games test].
  """

  # Learning agent
  agent1 = RLAgent(epsilon, gamma)
  if load_model is not None:
    agent1.load_model(load_model)
  
  # Choose opponent 
  if random_opponent:
    agent2 = RandomAgent()
    time_limit = None
    print('Training vs Random')
  else:
    agent2 = RLAgent(epsilon, gamma)
    if load_model is not None:
      agent2.load_model(load_model)
    time_limit = None
    print('Training vs Self')
  
  start_idx = 0
  scores = [0,0]

  # If the user only confronts the agent at the last epoch 
  # or if no confrontation
  if n_skip_games in [-1,0]:
    n_skip_games = n_epochs - n_skip_games

  # Boolean for game between the user and agent1 preceding a game 
  # between agent1 and agent2
  play_checkpoint_usr = False

  # If there is a test of agent1 at the last epoch only or no test 
  if freq_test in [-1,0]:
    freq_test = n_epochs - freq_test

  # Number of games between agent1 and a Random Agent for testing
  n_games_test_mem = n_games_test
  learning_results = []

  # Start training
  print('Training epoch:')
  for epoch in range(1, n_epochs + 1): 
    
    if epoch % (n_epochs // 10) == 0:
      print(epoch, '/', n_epochs)

    #Update boolean for playing with user
    play_checkpoint_usr = bool(epoch % n_skip_games == 0)
    if play_checkpoint_usr:
      # Print training status
      print('Number of games: ', epoch)
      print('Scores: ', scores)
      # Ask user to play
      play = int(input('Play ? (1 Yes | 0 No)\n'))
      play_checkpoint_usr = bool(play)

    # Update boolean for test
    n_games_test = int(epoch % freq_test == 0) * n_games_test_mem

    # Start game
    game_over, winner, test_results = game_2Agents(agent1, agent2, 
                  start_idx = start_idx, train = True, 
                  time_limit = time_limit, 
                  n_games_test = n_games_test,
                  play_checkpoint_usr = play_checkpoint_usr,
                  verbose = verbose)
    
    assert game_over, str('Game not over but new game' +
                          ' beginning during training')

    if winner in [0,1]:
      scores[winner] += 1

    # Save test games of agent1 against a Random Agent
    if bool(n_games_test):
      assert len(test_results) != 0, \
      'Agent1 has been tested but there is no result of that.'
      learning_results.append([
                  epoch, test_results[2], test_results[0], test_results[1]])

    # Next round
    start_idx = 1 - start_idx

  # Save Q-function of agent1
  np.savetxt(str('Models/' + filename + '.csv'), agent1.Q, delimiter=',')
  # Save stats for learning rate of agent1
  np.savetxt(str('Models/data/count_' + filename + '.csv'), 
              agent1.count_state_action, delimiter=',')

  return learning_results


if __name__ == "__main__":
  
  train(n_epochs = 5000, epsilon = 0.6, gamma = 1.0, load_model = None, 
    filename = 'greedy0_6_vsSelf_test', random_opponent = False, 
    n_games_test = 0, freq_test = -1, n_skip_games = -1, verbose = False)


  agent1 = RLAgent()
  agent1.load_model('greedy0_2_vsRandomvsSelf')
  agent2 = RLAgent()
  agent2.load_model('greedy0_6_vsSelf_test')
  results = compare_agents(agent1, agent2, n_games = 10, 
              time_limit = None, verbose = False)
  print(results)


