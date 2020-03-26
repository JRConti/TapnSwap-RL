import numpy as np

class TapnSwap:
    """
    Class which manages the hands of each player and their possible actions.
    """

    def __init__(self):
        """
        Initialize 4 hands (2 for each player).
        """

        self.hands = np.array([[1, 1], [1, 1]]) # 2 pairs of hands (1 finger on each hand)

    def tap(self, pair0, hand0, hand1):
        """
        Tap with hand0 of pair0 on hand1 of other pair.
        """

        if (self.hands[pair0, hand0] < 5
            and self.hands[1 - pair0, hand1] < 5
            and self.hands[pair0, hand0] > 0
            and self.hands[1 - pair0, hand1] > 0):
            self.hands[1 - pair0, hand1] += self.hands[pair0, hand0]

            if self.hands[1 - pair0, hand1] >= 5:
              self.hands[1 - pair0, hand1] = 0
        else: raise ValueError
    
    def swap(self, pair0, hand0, exchange_nbr):
        """
        Swap exchange_nbr from hand0 to hand1 (same pair pair0).
        """

        if ( 0 < exchange_nbr < 5
            and self.hands[pair0, hand0] >= exchange_nbr
            and self.hands[pair0, hand0] - exchange_nbr != self.hands[pair0, 1 - hand0]):
          self.hands[pair0, hand0] -= exchange_nbr
          self.hands[pair0, 1 - hand0] += exchange_nbr

          if self.hands[pair0, 1 - hand0] >= 5:
            self.hands[pair0, 1 - hand0] = 0
        else: raise ValueError

    def list_actions_tap(self, pair0):
      """
      Return the list of possible tap actions for pair0.
      Each 'tap' action has the form [0, tapping_hand, tapped_hand] where:
      
      * tapping hand is the hand of pair0 involved in tap action
      * tapped_hand is the hand of the other pair that receives the tap action of pair0.
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
      Return the list of possible swap actions for pair0.
      Each 'swap' action has the form [1, giving_hand, exchange_nbr] where:

      * giving_hand is the hand of pair 0 that gives some of its fingers to the other hand
      * exchange_nbr is the amount of those fingers.
      """

      list_actions = []
      sum_hands = self.hands[pair0, 0] + self.hands[pair0, 1]

      if 1 < sum_hands < 7: # Valid swap
        hand_max = np.argmax( self.hands[pair0, :] )
        diff_hands = self.hands[pair0, hand_max] - \
        self.hands[pair0, 1 - hand_max]
        
        if diff_hands == 0: # sum_hands = 2, 4 or 6  (1|1, 2|2 or 3|3)
          list_actions.append( [1, hand_max, 1])
          if sum_hands == 4:
            list_actions.append( [1, hand_max, 2] )
        
        elif diff_hands == 1: # sum_hands = 3 or 5  (2|1 or 3|2)
          list_actions.append( [1, 1 - hand_max, 1] )
        
        elif diff_hands == 2: # sum_hands = 2, 4 or 6  (2|0, 3|1 or 4|2)
          list_actions.append( [1, hand_max, 1])
          if sum_hands == 4:
            list_actions.append( [1, 1 - hand_max, 1] )
        
        elif diff_hands == 3: # sum_hands = 3 or 5  (3|0 or 4|1)
          list_actions.append( [1, hand_max, 1] )

        elif diff_hands == 4: # sum_hands = 4  (4|0)
          list_actions.append( [1, hand_max, 1] )
          list_actions.append( [1, hand_max, 2] )
      return list_actions

    def list_actions(self, pair0):
        """
        Return the unique list of possible actions for pair0.
        Each action has the same form than the output of list_actions_tap and list_actions_swap methods.
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
            indices = [i for i, x in enumerate(actions_h) if x == actions_hu[action]]
            if len(indices) > 1:
              indices_to_del += indices[1:]
        actions = [action for idx, action in enumerate(actions) if idx not in indices_to_del]

        return actions

    def list_actions_h(self, pair0):
      """
      Return the possible actions for pair0 in text format (non uniques).
      Each action has the form 'Tap with tapping_hand on tapped_hand' or 'Swap hands_pair0 for new_hands_pair0'.
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
      Return the possible actions for pair0 in text format (uniques).
      Each action has the form 'Tap with tapping_hand on tapped_hand' or 'Swap hands_pair0 for new_hands_pair0'.
      """

      actions_h = self.list_actions_h(pair0) 
      seen = set()
      return [action for action in actions_h if not (action in seen or seen.add(action))]

    def show_hands(self):
        return self.hands

    def take_action(self, pair0, action):
        """
        Take the action 'action' for pair0
        """

        if action[0] == 0: # tap
          self.tap(pair0, action[1], action[2])
        elif action[0] == 1: # swap
          self.swap(pair0, action[1], action[2])
        else: raise ValueError  

    def reset(self):
        """
        Reset the count of fingers on each hand.
        """     

        self.hands = np.array([[1, 1], [1, 1]])