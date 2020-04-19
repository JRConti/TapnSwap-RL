"""
TapnSwap game.
Main script. Launches the navigation menu (rules, number of players, ...).
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU 
# General Public License along with this program.  
# If not, see <https://www.gnu.org/licenses/>.

from tapnswap import TapnSwap
from interact import tap_valid_digits, game_1vs1, game_1vsAgent
from agent import Agent, RandomAgent, RLAgent
import os

def clear_screen(): 
  """ 
  Clear console screen on either windows, mac or linux.
  """

  # for windows 
  if os.name == 'nt': 
    _ = os.system('cls') 
  # for mac and linux(here, os.name is 'posix') 
  else: 
    _ = os.system('clear') 


def header_screen():
  """
  Print the header's game.
  """

  clear_screen()
  print('---------------------------------------')
  print(str('TAP \'N SWAP').center(42))
  print('---------------------------------------\n\n')  
  

def options(option1, option2, choice_sent, comeback = False):
  """
  Display a menu with 2 options, along with a sentence explaining
  what are the choices.

  Parameters
  ----------
  option1, option2: strings
    Names of options.
  choice_sent: string
    Sentence explaining to user the possible choices.
  comeback: boolean
    If set to True, add a 3rd option to go back for instance.

  Return
  ------
  choice: int (1, 2 or 0 if comeback = True)
    Choice of user.
  """

  header_screen()

  # Print options
  print(str('1  ' + str(option1)).center(40))
  print()
  print(str(' 2  ' + str(option2)).center(40))
  print('\n\n')

  # Ask user to choose
  sent = choice_sent + int(comeback) * ' (press 0 to go back)'
  print(sent)
  digits = int(comeback)* [0] + [1,2]
  choice = tap_valid_digits(digits)
  return choice


def input_names(n_players):
  """
  Asks user the names of players.

  Parameter
  ---------
  n_players: int (1 or 2)
    Number of human players.

  Return
  ------
  player or (player1, player2): strings
    Names of players given by user. Return player if n_players = 1.
    Return player1, player2 otherwise.
  """

  header_screen()
  assert n_players in [1,2], 'The number of names must be 1 or 2.'

  # 2 human players
  if n_players == 2:
    player1 = input('Name of 1st player ? \n')
    print()
    print('Name of 2nd player ? ')
    not_valid = True
    while not_valid:
      player2 = input()
      if player2 == player1:
        print('Please choose a different name than 1st player')
      else:
        not_valid = False
        print()
    return player1, player2

  # 1 human player
  else:
    player = input('Name of player ? \n')
    print()
    return player


def display_endgame(scores, name1, name2):
  """
  Print scores at the end of a game and asks user whether to start 
  again.

  Parameters
  ----------
  scores: list of 2 int
    List containing scores of both players.
  name1, name2: strings
    Names of players.

  Return
  ------
  restart: boolean
    Answer of user whether to start again.
  """

  # Print scores
  print('Current scores:\n')
  print(name1 + ': %i' % (scores[0]))
  print(name2 + ': %i' % (scores[1]))
  print('----------------------------')

  # Continue or go back
  print('Another game ? (1 : Yes  |   2 : No)\n')
  restart = tap_valid_digits([1,2])
  restart = int(restart)
  restart = bool(2 - restart)
  return restart


def game_mngr():
  """
  Game manager, used for navigation among different choices 
  offered to user.
  """

  # Options
  command = options('PLAY', 'RULES', 'Tap 1 to play or 2 to read the rules')

  # Rules page
  if int(command) == 2:
    header_screen()
    print(str('This page is empty.').center(40))
    print('\n\n') 
    # Go back
    print('Tap 1 to come back to the main menu\n')
    comeback = tap_valid_digits([1])
    if int(comeback):
      game_mngr()

  # Game page
  if int(command) == 1:
    # Options
    players = options('PLAYER', 'PLAYERS', 'How many players ?', 
                                                comeback = True)
    
    # Go back
    if int(players) == 0:
      game_mngr()

    # 2 players
    if int(players) == 2:

      # Ask players' name
      player1, player2 = input_names(n_players = 2)

      # Init scores
      scores = [0, 0]

      # Games
      tapnswap = TapnSwap()
      over = False
      while not over: 
        game_over, winner = game_1vs1(tapnswap, player1, player2)
        scores[winner] += 1
        if game_over:
          # Display scores
          restart = display_endgame(scores, player1, player2)
          # Go back
          if not restart: 
            over = True
            game_mngr()

    # 1 player
    if int(players) == 1:
      
      # Options
      level = options('EASY', 'DIFFICULT', 'Which level ?', comeback = True)

      # Go back
      if int(level) == 0:
        game_mngr()

      # Define agent
      elif int(level) == 1:
        agent = RandomAgent() # easy
      else:
        # Load agent
        agent = RLAgent()
        agent.load_model('greedy0_2_vsRandomvsSelf') # difficult

      # Ask player's name
      player = input_names(n_players = 1)

      # Init scores
      scores = [0, 0]

      # Games
      tapnswap = TapnSwap()
      over = False
      while not over: 
        game_over, winner = game_1vsAgent(tapnswap, player, agent,
                                                     greedy = False)
        scores[winner] += 1
        if game_over:
          # Display scores
          restart = display_endgame(scores, player, 'Computer')
          # Go back
          if not restart: 
            over = True
            game_mngr()
            

if __name__ == "__main__":

  game_mngr()
