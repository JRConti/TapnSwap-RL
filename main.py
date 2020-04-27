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


def print_rules():
  """
  Display the rules of TapnSwap game on screen.
  """

  header_screen()

  names = ['Player 1', 'Player 2']

  print('TapnSwap is a 2-player game. Both players have a ' +
        'variable number of fingers on both of their hands. ' + 
        'If one player has a hand composed of more than 4 fingers, this ' +
        'hand is "killed". The goal of the game is to kill both hands of ' +
        'the opponent player.\n')
  
  print('--------------')
  print(' First round ')
  print('--------------\n')

  print('Each player starts with 1 finger on each hand and one of them ' +
        'has to make the first move. The configuration of hands is then:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[0])
  print('----------------------------')
  print()
  print(str(names[1]).center(40))
  print('  |  '.center(40))
  print(str(4 * ' ' + \
            1 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(4 * ' ' + \
            1 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[0].center(40))
  print()

  print('Both players are separated from each other by the horizontal line. ' +
        'The main vertical line separates the hands of both players ' +
        '(L: left hands, R: right hands). There is currently 1 finger ' +
        'on each hand of each player.\n')

  print('-> Press Enter to continue')
  input()

  print('----------')
  print(' Actions ')
  print('----------\n')

  print('At each round of the game, each player has to choose an action ' +
        'among the list of possible actions. There are 2 main kinds of ' +
        'actions: tap and swap.\n')

  print('* Tap actions involve adding the number of fingers on one of ' +
        'your hands to one of your opponent\'s hands.\n')

  print('For instance, with the previous initial configuration, Player 1 ' +
        'may tap only with 1 (both of Player 1\'s hands have 1 finger) ' +
        'on 1 (both of Player 2\'s hands have 1 finger). If it happens, ' +
        'the configuration of hands at the next round is then:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[1])
  print('----------------------------')
  print()
  print(str(names[0]).center(40))
  print('  |  '.center(40))
  print(str(4 * ' ' + \
            1 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[1].center(40))
  print()

  print('Player 2 had 1 finger on each hand but Player 1 tapped with 1 ' +
        'so now Player 2 has one hand with 1+1 = 2 fingers.\n')

  print('-> Press Enter to continue')
  input()

  print('Now let\'s consider a more complex example:\n')

  # Example
  print('Round of', names[0])
  print('----------------------------')
  print()
  print(str(names[1]).center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            4 *'|' + \
            1 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(2 * ' ' + \
            3 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[0].center(40))
  print()

  print('It is Player 1\'s round. Her hands have respectively 3 and 1 ' +
        'fingers while Player 2 has hands with 2 and 4 fingers. Player 1 ' +
        'can then tap with 3 or 1 on a hand of Player 2, that is on 2 or 4.\n')

  print('Player 1 is able to kill the hand of Player 2 with 2 fingers, ' +
        'by tapping with 3 on 2 (3+2 = 5 > 4). The next round is then:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[1])
  print('----------------------------')
  print()
  print(str(names[0]).center(40))
  print('  |  '.center(40))
  print(str(2 * ' ' + \
            3 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(5 * ' ' + \
            0 *'|' + \
            '   |   ' + \
            4 *'|' + \
            1 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[1].center(40))
  print()

  print('Now Player 2 has lost a hand. Notice that Player 1 could have ' +
        'killed the hand of Player 2 which has 4 fingers instead, in the ' +
        'same way.\n')
  
  print('* Swap actions consist in exchanging some fingers of one of your ' +
        'hand to the other one.\n')

  print('To illustrate this process, let\'s come back to the previous ' +
        'complex example:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[0])
  print('----------------------------')
  print()
  print(str(names[1]).center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            4 *'|' + \
            1 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(2 * ' ' + \
            3 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[0].center(40))
  print()

  print('Instead of tapping with 1 or 3, Player 1 may swap some fingers ' +
        'from one of her hands to the other. By swapping 1 finger, ' +
        'Player 1 can obtain the configuration of hands 2-2 or 4-0. ' + 
        'Let\'s look at the first possibility:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[0])
  print('----------------------------')
  print()
  print(str(names[1]).center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            4 *'|' + \
            1 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            2 *'|' + \
            3 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[0].center(40))
  print()

  print('By swapping, Player 1 gets the configuration of hands 2-2. ' +
        'Changing the hand that loses 1 finger, Player 1 could have ' +
        'obtained the configuration 4-0.\n')

  print('-> Press Enter to continue')
  input()

  print('There is one main restriction to swap actions: swapping to an ' +
        'identical but reversed configuration is NOT allowed. For ' +
        'instance, in this case, Player 1 could not have swapped from ' +
        '3-1 to 1-3, exchanging 2 fingers.\n')

  print('But it is still possible to exchange 2 fingers. For instance, ' +
        'a swap from 3-2 to 1-4 is a valid swap.\n')

  print('Note that it is also possible to revive a killed hand:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[0])
  print('----------------------------')
  print()
  print(str(names[1]).center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            0 *'|' + \
            5 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[0].center(40))
  print()

  print('In this case, Player 1 has one hand with 2 fingers and a ' +
        'killed hand. Exchanging 1 finger from the left to the right, ' +
        'Player 1 may revive the killed hand:\n')

  print('-> Press Enter to continue')
  input()

  # Example
  print('Round of', names[0])
  print('----------------------------')
  print()
  print(str(names[1]).center(40))
  print('  |  '.center(40))
  print(str(3 * ' ' + \
            2 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print('L -------------------- R'.center(40))
  print('  |  '.center(40))
  print(str(4 * ' ' + \
            1 *'|' + \
            '   |   ' + \
            1 *'|' + \
            4 * ' ' ).center(40))
  print('  |  '.center(40))
  print(names[0].center(40))
  print()

  print('That\'s all for the rules, thanks !\n')


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
    print_rules()
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
