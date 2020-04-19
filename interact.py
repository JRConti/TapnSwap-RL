"""
TapnSwap game.
Functions for interaction with the user on command line.
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU 
# General Public License along with this program.  
# If not, see <https://www.gnu.org/licenses/>.

import time

def tap_valid_digits(list_numbers):
  """
  Ask a valid number to user among those found in list_numbers.

  Parameter
  ---------
  list_numbers: list [1,2,3,...] of valid numbers.

  Return
  ------
  result: string
    Valid input of user. 
  """

  # Loop until the user gives an element of list_numbers
  not_valid = True
  while not_valid:
    # Loop until the user gives an integer
    while True:
      try:
        result = input()
        result = int(result)
        break
      except ValueError:
        if len(list_numbers) == 1:
          seq = 'Tap ' + str(list_numbers[0]) + ' to continue'
        else:
          seq = 'Please tap one number ('
          for i in range(len(list_numbers) - 1):
            seq = seq + str(list_numbers[i]) + ', '
          seq = seq[:-2] + ' or ' + str(list_numbers[-1]) + ')'
        print(seq)
    # Check that the number belongs to list_numbers
    if result not in list_numbers:
      if len(list_numbers) == 1:
        seq = 'Tap ' + str(list_numbers[0]) + ' to continue'
      else:
        seq = 'Please tap ' 
        for i in range(len(list_numbers) - 1):
          seq = seq + str(list_numbers[i]) + ', '
        seq = seq[:-2] + ' or ' + str(list_numbers[-1]) 
      print(seq)
    else:
      not_valid = False
  return result


def show_score(tapnswap, names, player_idx, invert = False):
  """
  Show scores stored in tapnswap at player_idx's round.

  Parameters
  ----------
  tapnswap: instance of TapnSwap.
  names: list of 2 strings
    List containing the names of the 2 current players.
  player_idx: int (0 or 1)
    Index of player which has currently to play.
  invert: boolean
    If set to False, the player whose name is names[player_idx]
    is placed below its opponent. If True, the player below is
    names[1-player_idx].
  """

  # Name of player's round
  round_name = names[player_idx]
  if invert:
    round_name = names[1 - player_idx]
  print('Round of', round_name)
  print('----------------------------')

  # Print scores
  hands = tapnswap.show_hands()
  print()
  print(str(names[1 - player_idx]).center(40))
  print('  |  '.center(40))
  print(str((5 - hands[1 - player_idx][0]) * ' ' + \
            hands[1 - player_idx][0]*'|' + \
            '   |   ' + \
            hands[1 - player_idx][1]*'|' + \
            (5 - hands[1 - player_idx][1]) * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str((5 - hands[player_idx][0]) * ' ' + \
            hands[player_idx][0]*'|' + \
            '   |   ' + \
            hands[player_idx][1]*'|' + \
            (5 - hands[player_idx][1]) * ' ' ).center(40))
  print('  |  '.center(40))
  print(str(names[player_idx]).center(40))
  print()


def user_choose_action(tapnswap, player_idx):
  """
  Ask the user indexed by player_idx an action among all 
  the possibilities and take this action.

  Parameters
  ----------
  tapnswap: instance of TapnSwap.
  player_idx: int (0 or 1)
    Index of player to choose action.
  """
  
  print('Choose an action')
  
  # Print available actions
  list_actions = tapnswap.list_actions_hu(player_idx)
  for idx, action in enumerate(list_actions):
    print(idx, ': ', action)
  
  # Input action
  action_idx = tap_valid_digits(range(len(list_actions)))

  # Take action
  actions = tapnswap.list_actions(player_idx)
  tapnswap.take_action(player_idx, actions[action_idx])


def check_game_over(tapnswap, names, player_idx):
  """
  Check if the game is over at player_idx's round and display the 
  end of the game.

  Parameters
  ----------
  tapnswap: instance of TapnSwap.
  names: list of 2 strings
    List containing the names of the 2 current players.
  player_idx: int (0 or 1)
    Index of player who has just finished its round.

  Return
  ------
  game_over: boolean.
  winner: 
  * winner = -1 if not game_over.
  * winner = 0 if names[0] has won.
  * winner = 1 if names[1] has won. 
  """

  # Check
  game_over, winner = tapnswap.game_over()

  # Print
  if winner == player_idx:
    print('----------------------------')
    print(names[player_idx], 'won !')
  elif winner == 1 - player_idx:
    print('----------------------------')
    print(names[1 - player_idx], 'won !')
  
  return game_over, winner


def game_1vs1(tapnswap, player1, player2):
  """
  Display the game for 1 human vs 1 other human.

  Parameters
  ----------
  tapnswap: instance of TapnSwap.
  player1, player2: strings
    Names of the 2 players.

  Return
  ------
  game_over: boolean.
  winner: 
  * winner = -1 if not game_over.
  * winner = 0 if player1 has won.
  * winner = 1 if player2 has won. 
  """

  tapnswap.reset()

  game_over = False

  # Ask for starting player
  print('Which player start first ? (tap 1 for %s or 2 for %s) ' 
                                            % (player1, player2))
  player_idx = tap_valid_digits([1,2])
  player_idx = int(player_idx)
  player_idx -= 1
  names = [player1, player2]
  print()

  # Start game
  print('----------------------------')
  while not game_over:
    # Print scores
    show_score(tapnswap, names, player_idx)

    # Choose and take action
    user_choose_action(tapnswap, player_idx)
  
    # Check if game is over
    game_over, winner = check_game_over(tapnswap, names, player_idx)
    print('----------------------------')

    player_idx = 1 - player_idx

  return game_over, winner


def game_1vsAgent(tapnswap, player, agent, greedy = False):
  """
  Display the game for 1 human vs 1 agent.

  Parameters
  ----------
  tapnswap: instance of TapnSwap.
  player: string
    Name of player.
  agent: instance of Agent to play against user.
  greedy: boolean. 
    Not used for training here but, if set to True, allows to use 
    greedy policy (with epsilon) to add some randomness in agent 
    choices while setting it to False leads to optimal choices.

  Return
  ------
  game_over: boolean.
  winner: 
  * winner = -1 if not game_over.
  * winner = 0 if player has won.
  * winner = 1 if agent has won. 
  """

  tapnswap.reset()

  # Ask for starting player
  print('Which player start first ? (tap 1 for you or 2 for computer) ')
  player_idx = tap_valid_digits([1,2])
  player_idx = int(player_idx)
  player_idx -= 1
  names = [player, 'Computer']
  print()

  # Start game
  print('----------------------------')
  game_over = False
  while not game_over:
    
    # Player's round
    if player_idx == 0:
      # Print scores
      show_score(tapnswap, names, player_idx)

      # Choose and take action
      user_choose_action(tapnswap, player_idx)


    # Computer's round
    else:
      # Print scores before action of agent
      show_score(tapnswap, names, 1 - player_idx, invert = True)
      time.sleep(2)

      # Get current state and possible actions
      hands = tapnswap.show_hands().copy()
      state = [ hands[player_idx], hands[1 - player_idx]  ]
      actions = tapnswap.list_actions(player_idx)
      # Choose action
      action = agent.choose_action(state, actions, greedy = greedy)
      # Take action
      reward = tapnswap.take_action(player_idx, action)

      # Print chosen action
      seq = 'Computer '
      if action[0] == 0:
        seq = seq + str('tapped with ' + str(hands[player_idx, action[1]]) + 
                        ' on ' + str(hands[1 - player_idx, action[2]]) )
      else:
        new_hands = tapnswap.show_hands()
        seq = seq + str( 'swapped ' + str(hands[player_idx][0]) + '-' + 
                          str(hands[player_idx][1]) + ' for ' + 
                          str(new_hands[player_idx][0]) + '-' + 
                          str(new_hands[player_idx][1]) )
      print(seq)
      time.sleep(2)

    # Check if game is over
    game_over, winner = check_game_over(tapnswap, names, player_idx)
    print('----------------------------')

    player_idx = 1 - player_idx

  return game_over, winner
