
def tap_valid_digits(list_numbers):
  """
  Ask a valid number to user among those in list_numbers
  Return the valid input by user 
  """
  not_valid = True
  while not_valid:
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


def game_1vs1(tapnswap, player1, player2):
  """
  Display the game for 1 human vs 1 other human
  tapnswap: instance of class TapnSwap
  player1, player2: names of 2 players

  return boolean game_over and the identity of the winner
  """

  game_over = False

  # Ask for starting player
  print('Which player start first ? (tap 1 for %s or 2 for %s) ' % (player1, player2))
  player_idx = tap_valid_digits([1,2])
  player_idx = int(player_idx)
  player_idx -= 1
  names = [player1, player2]
  print()

  # Start game
  print('----------------------------')
  while not game_over:
    print('Round of', names[player_idx])
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

    print('Choose an action')
  
    # Print available actions
    list_actions = tapnswap.list_actions_hu(player_idx)
    for idx, action in enumerate(list_actions):
      print(idx, ': ', action)
  
    # Input action
    valid_input = False
    while not valid_input:
      action_idx = int(input())
      if action_idx in range( len(list_actions) ):
        valid_input = True
      else:
        print('Please select a valid action')

    # Take action
    tapnswap.take_action(player_idx, tapnswap.list_actions(player_idx)[action_idx])
  
    # Check if game is over
    hands = tapnswap.show_hands()
    if hands[player_idx][0] == 0 and hands[player_idx][1] == 0:
      game_over = True
      print('----------------------------')
      print(names[1 - player_idx], 'won !')
      winner = 1 - player_idx
    elif hands[1-player_idx][0] == 0 and hands[1-player_idx][1] == 0:
      game_over = True
      print('----------------------------')
      print(names[player_idx], 'won !')
      winner = player_idx
    print('----------------------------')

    player_idx = 1 - player_idx

  return game_over, winner