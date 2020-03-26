from os import system, name 
from time import sleep 
from tapnswap import *
from interact import *


def clear_screen(): 
  """ 
  Clear console screen on either windows, mac or linux
  """

  # for windows 
  if name == 'nt': 
    _ = system('cls') 
  # for mac and linux(here, os.name is 'posix') 
  else: 
    _ = system('clear') 


def header_screen():
  """
  Print the header's game
  """
  clear_screen()
  print('---------------------------------------')
  print(str('TAP \'N SWAP').center(40))
  print('---------------------------------------\n\n')  
  


def game_mngr(tapnswap):
  """

  """

  header_screen()

  # Options
  print(str('1 : PLAY').center(40))
  print()
  print(str(' 2 : RULES').center(40))
  print('\n\n')

  # Choice
  print('Tap 1 to play or 2 to read the rules')
  command = tap_valid_digits([1,2])

  # Rules page
  if int(command) == 2:
    header_screen()
    print(str('This page is empty.').center(40))
    print('\n\n') 
    # Go back
    print('Tap 1 to come back to the main menu\n')
    comeback = tap_valid_digits([1])
    if int(comeback):
      game_mngr(tapnswap)

  # Game page
  if int(command) == 1:
    header_screen()
    # Options
    print(str('1 PLAYER').center(40))
    print()
    print(str(' 2 PLAYERS').center(40))
    print('\n\n')
    # Choice
    print('How many players ? (press 0 to go back)')
    players = tap_valid_digits([0,1,2])
    
    # Go back
    if int(players) == 0:
      game_mngr(tapnswap)

    # 2 players
    if int(players) == 2:
      header_screen()
      # Names of players
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

      # Init scores
      scores = [0, 0]

      # Games
      over = False
      while not over: 
        game_over, winner = game_1vs1(tapnswap, player1, player2)
        scores[winner] += 1
        if game_over:
          # Display scores
          print('Current scores:\n')
          print(player1 + ': %i' % (scores[0]))
          print(player2 + ': %i' % (scores[1]))
          print('----------------------------')
          # Continue or go back
          tapnswap.reset()
          print('Another game ? (1 : Yes  |   2: No)\n')
          restart = tap_valid_digits([1,2])
          # Go back
          if int(restart) == 2: 
            over = True
            game_mngr(tapnswap)

    # 1 player
    if int(players) == 1:
      header_screen()
      print(str('This page is empty.').center(40))
      print('\n\n') 
      # Go back
      print(str('Tap 1 to come back to the main menu\n').center(40))
      comeback = tap_valid_digits([1])
      if int(comeback):
        game_mngr(tapnswap)






tapnswap = TapnSwap()
game_mngr(tapnswap)
