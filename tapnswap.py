"""
TapnSwap game.
Module TapnSwap is the back-end of the game. It manages hands of 
players and their actions.
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU 
# General Public License along with this program. 
# If not, see <https://www.gnu.org/licenses/>.

import numpy as np

class TapnSwap:
    """
    Class which manages the hands of each player and 
    their possible actions.
    """

    def __init__(self):
        """
        Initialize 4 hands (2 for each player).
        """

        # 2 pairs of hands (1 finger on each hand)
        self.hands = np.array([[1, 1], [1, 1]]) 


    def tap(self, pair0, hand0, hand1):
        """
        Tap with hand0 of pair0 on hand1 of other pair: add number of 
        fingers found on hand0 of pair0 to the hand1 of other pair.

        Parameters
        ----------
        pair0: int (0 or 1)
        	Index of pair of hands involved in tapping the other pair.
        hand0: int (0 or 1)
            Hand's index giving tap action (hand of pair0).
        hand1 : int (0 or 1)
            Hand's index receiving tap action (hand of other pair 
            than pair0).
        """

        if (0 < self.hands[pair0, hand0] < 5
            and 0 < self.hands[1 - pair0, hand1] < 5):
            self.hands[1 - pair0, hand1] += self.hands[pair0, hand0]

            # Kill hand with more than 4 fingers
            if self.hands[1 - pair0, hand1] >= 5:
              self.hands[1 - pair0, hand1] = 0
        else: raise ValueError

    
    def swap(self, pair0, hand0, exchange_nbr):
        """
        Swap exchange_nbr from hand0 to other hand (same pair pair0).

        Parameters
        ----------
        pair0: int (0 or 1)
            Index of pair of hands involved in swap action.
        hand0: int (0 or 1)
            Hand's index involved in giving some of its fingers 
            to the other hand (both are hands of pair0).
        exchange_nbr: int
            Number of fingers to take from hand0 of pair0 and
            to give to hand1 of pair0.
        """

        if ( 0 < exchange_nbr < 5
            and self.hands[pair0, hand0] >= exchange_nbr
            and (self.hands[pair0, hand0] - exchange_nbr != 
                  self.hands[pair0, 1 - hand0])
            ):
          self.hands[pair0, hand0] -= exchange_nbr
          self.hands[pair0, 1 - hand0] += exchange_nbr

          # Kill hand with more than 4 fingers
          if self.hands[pair0, 1 - hand0] >= 5:
            self.hands[pair0, 1 - hand0] = 0
        else: raise ValueError


    def list_actions_tap(self, pair0):
      """
      Gives the list of possible tap actions for pair0.

      Parameter
      ---------
      pair0: int (0 or 1)
      	Index of pair of hands for which one wants to know 
        the list of possible tap actions.

      Return
      ------
      list_actions: list of possible tap actions.
      	Each tap action has the form [0, tapping_hand, tapped_hand] 
      	where:
      	* tapping_hand: int (0 or 1)
            Hand of pair0 involved in tap action.
      	* tapped_hand: int (0 or 1)
            Hand of the other pair that receives the 
            tap action of pair0.
      """

      list_actions = []
      for i in range(2):
        if 0 < self.hands[pair0, i] < 5:
          for j in range(2):
            if 0 < self.hands[1 - pair0, j] < 5:
              list_actions.append([0, i, j])
      return list_actions

    
    def list_actions_swap(self, pair0):
      """
      Gives the list of possible swap actions for pair0.

      Parameter
      ---------
      pair0: int (0 or 1)
        Index of pair of hands for which one wants to know 
        the list of possible swap actions.

      Return
      ------
      list_actions: list of possible swap actions.
      	Each swap action has the form [1, giving_hand, exchange_nbr] 
      	where:
      	* giving_hand: int (0 or 1) 
            Hand of pair 0 that gives some of its fingers 
            to the other hand.
      * exchange_nbr: int
            Amount of such fingers.
      """

      list_actions = []
      sum_hands = self.hands[pair0, 0] + self.hands[pair0, 1]

      if 1 < sum_hands < 7: # Valid swap

        # Index of maximum hand of pair0
        hand_max = np.argmax( self.hands[pair0, :] )
        diff_hands = (self.hands[pair0, hand_max] - 
                      self.hands[pair0, 1 - hand_max])
        
        if diff_hands == 0: # (1|1, 2|2 or 3|3)
          list_actions.append( [1, hand_max, 1])
          if sum_hands == 4:
            list_actions.append( [1, hand_max, 2] )
        
        elif diff_hands == 1: # (2|1 or 3|2)
          list_actions.append( [1, 1 - hand_max, 1] )
        
        elif diff_hands == 2: # (2|0, 3|1 or 4|2)
          list_actions.append( [1, hand_max, 1])
          if sum_hands == 4:
            list_actions.append( [1, 1 - hand_max, 1] )
        
        elif diff_hands == 3: # (3|0 or 4|1)
          list_actions.append( [1, hand_max, 1] )

        elif diff_hands == 4: # (4|0)
          list_actions.append( [1, hand_max, 1] )
          list_actions.append( [1, hand_max, 2] )
      return list_actions


    def list_actions_h(self, pair0):
      """
      Gives the possible actions for pair0 in text format 
      (non uniques -> might observe repetitions). 
      
      Parameter
      ---------
      pair0: int (0 or 1)
        Index of pair of hands for which one wants to know 
        the list of possible actions.

      Return
      ------
      actions_h: list of possible actions in text format.
      	Each action has the form 'Tap with fingers_on_tapping_hand on 
      	fingers_on_tapped_hand' or 'Swap fingers_on_hand0_pair0 -
      	fingers_on_hand1_pair0 for fingers_on_new_hand0_pair0 -
      	fingers_on_new_hand1_pair0' where:
      	* fingers_on_tapping_hand: int
            Amount of fingers found on tapping hand before tap action.
      	* fingers_on_tapped_hand: int
            Amount of fingers on tapped hand before tap action.
      	* fingers_on_hand[i]_pair0: int
            Amount of fingers found on hand [i] of pair 0 before swap.
      	* fingers_on_new_hand[i]_pair0: int
            Amount of fingers found on hand[i] of pair0 after swap.
      """

      actions = self.list_actions_tap(pair0) + self.list_actions_swap(pair0)
      actions_h = []

      for i in range(len(actions)):
        new_action = ''
        # Tap action
        if actions[i][0] == 0:
          new_action = 'Tap with %i on %i' % (
          self.hands[pair0, actions[i][1]],
          self.hands[1 - pair0, actions[i][2]])
        # Swap action
        else:
          new_action = 'Swap %i-%i for %i-%i' % (
              self.hands[pair0, 0], self.hands[pair0, 1],
              self.hands[pair0, actions[i][1]] - actions[i][2],
              self.hands[pair0, 1 - actions[i][1]] + actions[i][2])
        actions_h.append(new_action)
      
      return actions_h


    def list_actions_hu(self, pair0):
      """
      Gives the possible actions for pair0 in text format (uniques).

      Parameter
      ---------
      pair0: int (0 or 1)
        Index of pair of hands for which one wants to know 
        the list of possible actions.

      Return
      ------
      list of (unique) possible actions in text format.
      	Each action has the same format than the output of 
      	list_actions_h method.
      """

      actions_h = self.list_actions_h(pair0) 
      seen = set()
      return [action for action in actions_h 
              if not (action in seen or seen.add(action))]


    def list_actions(self, pair0):
        """
        Gives the list of unique possible actions for pair0.

        Parameter
        ---------
        pair0: int (0 or 1)
        	Index of pair of hands for which one wants to know 
            the list of possible actions.

        Return
        ------
        actions: list of unique possible actions.
        	Each action has the same format than the output of 
        	list_actions_tap and list_actions_swap methods.
        """

        # List of non-unique actions
        actions = self.list_actions_tap(pair0) + self.list_actions_swap(pair0)
        
        # Corresponding actions in text format
        actions_h = self.list_actions_h(pair0)    # non-uniques
        actions_hu = self.list_actions_hu(pair0)  # uniques

        # Keep unique actions
        indices_to_del = []
        if len(actions_hu) != len(actions_h):
          for action in range(len(actions_hu)):
            indices = [i for i, x in enumerate(actions_h) 
                        if x == actions_hu[action]]
            if len(indices) > 1:
              indices_to_del += indices[1:]
        actions = [action for idx, action in enumerate(actions) 
                    if idx not in indices_to_del]

        return actions


    def show_hands(self):
        return self.hands


    def game_over(self):
      """
      Check if game over.

      Return
      ------
      game_over: boolean
      winner: 
      * winner = -1 if not game_over
      * winner = 0 if self.hands[1] = [0,0]
      * winner = 1 if self.hands[0] = [0,0]. 
      """

      game_over = not bool( (self.hands[0][0] + 
                              self.hands[0][1]) * (self.hands[1][0] + 
                                                    self.hands[1][1]) )

      winner = -1 * int(not game_over) + (int(game_over) * ( 
                  int(not bool( self.hands[0][0] + self.hands[0][1] )) + 
                  int(    bool( self.hands[1][0] + self.hands[1][1] ))  
                                                            ) // 2)

      return game_over, winner


    def take_action(self, pair0, action):
        """
        Take action for pair0.

        Parameters
        ----------
        pair0: int (0 or 1)
            Index of pair of hands which takes action.
        action: list 
            Action taken by pair0 (same format than the output of 
            list_actions method).

        Return
        ------
        reward: float
            Reward given to pair0. For now, a non 0 reward is
            returned only if the game is over just after the action.
        """

        # Take action
        if action[0] == 0: # tap
          self.tap(pair0, action[1], action[2])
        elif action[0] == 1: # swap
          self.swap(pair0, action[1], action[2])
        else: raise ValueError  

        reward = 0.0

        # Check if game is over
        game_over, winner = self.game_over()
        if game_over:
          reward = 10.0
          if winner != pair0:
            reward = - reward
        return reward


    def reset(self):
        """
        Reset the count of fingers on each hand.
        """     

        self.hands = np.array([[1, 1], [1, 1]])

