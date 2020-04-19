"""
TapnSwap game.
Module Optimizer is used as validation step for training agents via 
Q-learning. Training can be done for many values of epsilon (parameter 
of RL Agent) and for different opponents (Random Agent, Self and all 
sequences using those two). All the resulting trained agents can then 
play against each other in a tournament. Looking at the results of 
those tournaments, it is then possible to retrain some of the trained 
agents, according to their total score during the tournament.
"""

# Copyright (C) 2020, Jean-Rémy Conti, ENS Paris-Saclay (France).
# All rights reserved. You should have received a copy of the GNU 
# General Public License along with this program.  
# If not, see <https://www.gnu.org/licenses/>.

from agent import Agent, RandomAgent, RLAgent
from train import compare_agents, train
import numpy as np
import os

class Optimizer:
	"""
	This optimizer can be initialized for different values of epsilon 
	(parameter of RL Agent) and different ways of training (i.e.
	identity of opponent). Once initialized, it allows for some 
	methods as grid-search which evaluates agent performance during
	training or retrain_best_models which retrains a part of the
	current best models.
	"""

	def __init__(self, epsilon_values, random_training = True, 
						self_training = True, change_opp = True):
		"""
		Specifies which epsilon values and which kind of opponents
		are considered to optimize the learning agent strategy.

		Parameters
		----------
		epsilon_values: list of float (in [0,1])
			List of values of epsilon considered.
		random_training: boolean
			Set to True to consider agents training against Random 
			Agents.
		self_training: boolean
			Set to True to consider agents training against themselves.
		change_opp: boolean
			Set to True to achieve the optimization by changing the 
			opponents of already trained models. For instance, if a 
			previous model was trained against a Random Agent, this 
			option allows to train it against itself.
		"""

		self.epsilon_values = epsilon_values
		
		self.random_training = random_training
		self.self_training = self_training
		assert self.random_training or self.self_training, \
									'Please select at least one training way.'
		
		self.change_opp = change_opp

		# Base name to store results of various tournaments 
		self.tournament_name = 'tournament0'


	def grid_search(self, n_epochs, n_games_test = 100, freq_test = 0,
														retrain = False):
		"""
		Compute the fraction of an agent's wins over a given number of 
		games against a Random Agent. This fraction is computed as a
		function of the number of games used for training the agent.
		At the end of all trainings, a tournament between all trained
		agents occurs. 

		Parameters
		----------
		n_epochs: int
			Number of epochs to train each model.
		n_games_test: int
			Number of games to test the training agent against a 
			Random Agent.
		freq_test: int
			Number of epochs after which the training agent plays n_games_test
			games against a Random Agent. If set to 1000, each 1000 epochs of
			training, the training agent is tested against a Random Agent.
			If set to 0, test occurs at the last epoch of training only.
			If set to -1, there is no test during training.
		retrain: boolean
			Set to True to do the grid-search via training of already
			trained models.

		Outputs
		-------
		For each value of epsilon and each kind of opponent:
		* GS file path: TXT file
			Located at: 
			'Models/train/GS_epsilon_(epsilon_value)_vs(Random/Self).txt'.
			File in which each line corresponds to an epoch test result:
			'epoch, score of RL agent, number of finished games, 
			n_games_test'.
		* CSV model: CSV file
			Located at:
			'Models/greedy_(epsilon_value)_vs(Random/Self).csv'
			File storing the Q-function of the model trained after 
			n_epochs. The counter of state-action pairs is also stored at:
			'Models/data/count_greedy_(epsilon_value)_vs_(Random/self).csv'.
		Only once:
		* Tournament report: CSV file
			Located at: 'Models/results/(self.tournament_name).csv'.
			File storing the results of each confrontation between 
			any 2 of the trained agents.
		* Tournament ranking: TXT file
			Located at: 'Models/results/(self.tournament_name).txt'.
			File ranking the agents using the results of the tournament,
			with total score of each agent displayed.
		"""

		print('-----------')
		print('Grid-Search')
		print('-----------')

		# List of training ways (against random or against themselves)
		random_choices = []
		if self.random_training:
			random_choices.append(True)
		if self.self_training:
			random_choices.append(False)

		# Changing the opponent of already trained models
		invert_choices = [False]
		if self.change_opp and retrain:
			# True must be the 1st element 
			invert_choices = [True, False]

		problems = []

		for random_opponent in random_choices:
			# Effective opponent
			random_opp = random_opponent
			opp = ('Random' * int(random_opponent) + 
					'Self' * (1 - int(random_opponent)))
		
			for invert_opp in invert_choices:
				new_opp = ''
				if invert_opp:
					# Change opponent
					random_opp = not random_opp
					new_opp = ('vsSelf' * int(random_opponent) + 
								'vsRandom' * (1 - int(random_opponent)))

				for epsilon in self.epsilon_values:
					print('epsilon = ', epsilon)
					if retrain:
						print('Previously trained vs ' + str(opp))

					# Output GS filename
					output_path = ('Models/train/GS_epsilon_' + 
									str(epsilon)[0] + '_' + 
									str(epsilon)[2:] + '_vs' + 
									opp + '.txt')

					# Name of CSV model
					model_filename = ('greedy' + str(epsilon)[0] + '_' + 
										str(epsilon)[2:] + '_vs' + opp)

					# Previous number of epochs used for training
					prev_epochs = 0
				
					# Prepare output file
					if not retrain:
						load_model = None

						# Initialize output file
						with open(output_path, "w") as f:
							f.write('Grid-Search\nrandom opponent: ' + 
									str(random_opponent) + '\nepsilon= ' + 
									str(epsilon) + 
									'\n------------------------------\n')
					else:
						load_model = model_filename

						# Update prev_epochs
						prev_epochs = self.find_prev_epochs(epsilon, opp)

						if invert_opp:
							# Prepare output file: copy original results 
							# to add results of future training by 
							# changing the opponent
							output_path2 = ('Models/train/GS_epsilon_' + 
											str(epsilon)[0] + '_' + 
											str(epsilon)[2:] + '_vs' + 
											opp + new_opp + '.txt')
							with open(output_path, 'r') as file_1:
								with open(output_path2, 'w') as file_2:
									for line in file_1:
										if 'random' in line:
											line = line[:-1] + str(' then ' + 
															str(random_opp) + 
																		'\n')
										file_2.write(line)
									file_2.write('---------------'+
												'---------------\n')

							output_path = output_path2
							model_filename = model_filename + new_opp 

					# Create temp file if model already exists
					if os.path.exists('Models/' + model_filename + '.csv'):
						model_filename = model_filename + '_temp'
			
					learning_results = train(n_epochs = n_epochs, 
										epsilon = epsilon, gamma = 1.0, 
										load_model = load_model, 
										filename = model_filename,
										random_opponent = random_opp, 
										n_games_test = n_games_test,
										freq_test = freq_test, 
										n_skip_games = -1, verbose = False)

					assert len(learning_results) != 0, 'Problem here'
			
					# Keep best model and delete temp files
					use_training = self.delete_temp(load_model, model_filename)

					# Store results if trained model is better / before
					if use_training:
						with open(output_path, "a") as f:
							for result in learning_results:
								f.write(str(result[0] + prev_epochs) + ',' +
										 str(result[1]) + ',' + 
										 str(result[2]) + ',' + 
										 str(result[3]) + '\n')

					# Just expectations of results
					if not retrain:
						rate_success = 0.95
					else:
						rate_success = 0.99
					if (not (result[2] == result[3]) or 
						not (result[1] >= rate_success * result[2])):
						print('At the end of training, the RL Agent has won' +
								'only {}/{} games.'.format(result[1], result[3]))
						problems.append([epsilon, random_opp])

					# Display the ineffectiveness of training
					if not use_training:
						print('Trained agent is worse than before training.')
			
					print('\n-----------\n')

		if len(problems) > 0:
			print('Problem with training of the following agents: ', problems, 
										'\nIncrease the number of epochs.')
			print('\n-----------\n')

		# The change of opponent is not available if no model has been 
		# trained before
		change_opp = False
		if retrain:
			change_opp = self.change_opp

		# Start tournament with trained models
		self.tournament(change_opp = change_opp)


	def find_prev_epochs(self, epsilon, training_way):
		"""
		Find number of epochs previously used to train a given model. 
		This function looks at the GS txt file corresponding to the 
		model.

		Parameters
		----------
		epsilon: float
			Parameter of agent during training.
		training_way: string
			Opponent of agent during training (Random, Self, ...).

		Return
		------
		n_epochs: int
			Number of epochs previously used to train the model.
		"""

		n_epochs = 0
		
		# Look at Grid-Search txt file
		filename = ('GS_epsilon_' + str(epsilon)[0] + '_' + str(epsilon)[2:] +
					'_vs' + str(training_way))
		file_path = 'Models/train/' + filename + '.txt' 
		with open(file_path, "r") as f:
			data_player = f.readlines()
		data_player = data_player[4:]
		data_player = [line[:-1] for line in data_player]
		data_player =[ line.split(',') for line in data_player ]
		n_epochs += int(data_player[-1][0])

		return n_epochs


	def delete_temp(self, old_model, temp_model):
		"""
		Delete temporary files in case of 2 versions of same model 
		(but different times of training). Keep the best model and 
		delete the rest.

		Parameters
		----------
		old_model: string
			Model filename before training.
		temp_model: string
			Temporary model filename (after training).

		Return
		------
		use_training: boolean
			False only if old model wins against new temp model.
			True otherwise.
		"""

		use_training = True
		# Several versions of same model
		if (old_model is not None) and (temp_model == old_model + '_temp'):
			# Confront them
			agent1 = RLAgent()
			agent1.load_model(old_model)
			agent2 = RLAgent()
			agent2.load_model(temp_model)
			results = compare_agents(agent1, agent2, n_games = 10, 
									time_limit = 100, verbose = False)

			# Keep best
			if results[3] >= results[2]:
				# More trained agent is the best
				os.remove('Models/' + old_model + '.csv')
				os.remove('Models/data/count_' + old_model + '.csv')
				os.rename(r'Models/' + temp_model + '.csv', 
							r'Models/' + old_model + '.csv')
				os.rename(r'Models/data/count_' + temp_model + '.csv', 
							r'Models/data/count_' + old_model + '.csv')
			else:
				# Less trained agent is the best
				os.remove('Models/' + temp_model + '.csv')
				os.remove('Models/data/count_' + temp_model + '.csv')
				use_training = False
		return use_training


	def tournament(self, change_opp = False):
		"""
		Method to rank the different models obtained after any training. 
		For the values of the factor epsilon of an RL Agent, declared 
		in init method, this method creates a tournament for the 
		corresponding different models. Each model plays 10 games 
		against all others and the scores of each model against another 
		are stored in a CSV file. A TXT file is also generated using
		the CSV file: it displays rankings of each model, alongside
		its total score against all other models.

		Parameter
		---------
		change_opp: boolean
			Set to True to consider agents trained with mixed opponents
			participating to the tournament.

		Outputs
		-------
		Tournament report: CSV file
			Located at: 'Models/results/(self.tournament_name).csv'.
			File storing the results of each confrontation between 2 
			agents.
		Tournament ranking: TXT file
			Located at: 'Models/results/(self.tournament_name).txt'.
			File ranking the agents using the results of the tournament,
			with total score of each agent displayed.
		"""

		n_players = len(self.epsilon_values) * (( int(self.random_training) + 
						int(self.self_training) ) * (1 + int(change_opp) ))

		print('-----------------------------')
		print('TOURNAMENT with {} agents'.format(n_players))
		print('-----------------------------\n')

		# Initialization of scores: some rows and columns are
		# only used for saving configurations of models
		# (epsilon, opponents, change of opponent).
		scores = - np.ones( (n_players + 3, n_players + 3) )

		# List of opponent kinds
		training_ways = []
		if self.random_training:
			training_ways.append('Random')
			if change_opp:
				training_ways.append('RandomvsSelf')
		if self.self_training:
			training_ways.append('Self')	
			if change_opp:
				training_ways.append('SelfvsRandom')

		# List of players
		players = [ [epsilon, training_way] for epsilon in self.epsilon_values 
											for training_way in training_ways]

		for idx1, player1 in enumerate(players):
			epsilon1 = player1[0]
			training_way1 = player1[1]
			filename = ('greedy' + str(epsilon1)[0] + '_' + 
						str(epsilon1)[2:] + '_vs' + training_way1)

			# Load first agent
			agent1 = RLAgent()
			agent1.load_model(filename)

			# Save config of agent1
			scores[idx1+3, 0] = epsilon1
			# 0: RANDOM | 1: SELF
			scores[idx1+3, 1] = (int(training_way1 == 'Self') + 
								int(training_way1 == 'SelfvsRandom'))
			# -1: nothing | 0: Random vs Self | 1: Self vs Random
			scores[idx1+3, 2] = -1+(2 * int(training_way1 == 'SelfvsRandom') +
										 int(training_way1 == 'RandomvsSelf')) 

			for idx2, player2 in enumerate(players):
				epsilon2 = player2[0]
				training_way2 = player2[1]
				filename = ('greedy' + str(epsilon2)[0] + '_' + 
							str(epsilon2)[2:] + '_vs' + training_way2)

				# Load second agent
				agent2 = RLAgent()
				agent2.load_model(filename)

				# Save config of agent2
				scores[0, idx2+3] = epsilon2
				scores[1, idx2+3] = (int(training_way2 == 'Self') + 
									int(training_way2 == 'SelfvsRandom'))
				scores[2, idx2+3] = -1+(2*int(training_way2 == 'SelfvsRandom')+
										 int(training_way2 == 'RandomvsSelf')) 

				print('Current match:')
				print('Player1: epsilon = {}, trained vs {}'.format(epsilon1, 
															training_way1))
				print('Player2: epsilon = {}, trained vs {}'.format(epsilon2, 
															training_way2))

				results = compare_agents(agent1, agent2, n_games = 10, 
										time_limit = 100, verbose = False)

				# Score of agent1
				scores[idx1+3, idx2+3] = results[2]
				# Score of agent2
				scores[idx2+3, idx1+3] = results[3]

				print('------')

		# Update tournament file name
		name = self.tournament_name[:-1]
		nbr = int(self.tournament_name[-1])
		nbr += 1
		self.tournament_name = name + str(nbr)

		# Save tournament
		np.savetxt(str('Models/results/' + self.tournament_name + '.csv'), 
														scores, delimiter=',')

		# Rank players
		self.tournament_ranking(self.tournament_name, self.tournament_name)

		print('Results of tournament are stored in {}.csv and {}.txt\n'.format(
									self.tournament_name, self.tournament_name))


	def tournament_ranking(self, input_filename, output_filename):
		"""
		Takes a tournament report CSV file as input and outputs 
		the final scores of each player, as long as their ranking.

		Parameters
		----------
		input_filename: string
			Name of tournament report CSV file.
		output_filename: string
			Name of tournament ranking TXT file.

		Output
		------
		Models/results/(output_filename).txt: TXT file
			File ranking the agents using the results of the tournament,
			with total score of each agent displayed.
		"""

		# Prepare output file
		with open('Models/results/' + output_filename + '.txt', "w") as f:
			f.write('Best players (from last to best):\n\n')

		# Import tournament CSV file
		data = np.loadtxt('Models/results/' + input_filename + '.csv', 
															delimiter = ',')
		scores = data[3:, 3:]
		scores = np.array(scores, dtype = 'int')

		# Compute final scores
		sum_scores = np.sum(scores, axis = 1)

		# Sort players by score
		indices_players_sorted = np.argsort(sum_scores)

		seen = []
		counter = 0
		# Output final scores
		for player in indices_players_sorted:
			# Extract player's info
			epsilon = data[player+3, 0]
			training_way = int(data[player+3, 1]) * 'Self' + ((1-
											int(data[player+3, 1])) * 'Random')
			# If this agent has been trained 2 times
			if int(data[player+3, 2]) != -1:
				training_way = (int(data[player+3, 2])) * 'SelfvsRandom' + ((1-
									int(data[player+3, 2])) * 'RandomvsSelf')

			# Avoid repetitions
			if [epsilon, training_way] in seen:
				continue
			seen.append([epsilon, training_way])
			counter += 1

			# Find number of previous epochs of training
			n_epochs = self.find_prev_epochs(epsilon, training_way)
		
			# Output player's final score
			with open('Models/results/' + output_filename + '.txt', "a") as f:
				f.write(str(counter) + ':\t' + str(sum_scores[player]) + 
						'\tepsilon = ' + str(epsilon) + ', \ttrained vs ' + 
						str(training_way) + ' \t' + 
						'\t'* (len(str(training_way)) < 7) + str(n_epochs) + 
						'\tepochs\n')


	def retrain_best_models(self, n_epochs, common_train_time = False, 
															min_frac = 0.3):
		"""
		Looks at previous tournament ranking TXT file (whose name is
		self.tournament_name) and selects some of the best current 
		models according to their total score. The values of epsilon
		not represented by those best models are definitely discarded
		by the Optimizer. Once selected, those models are retrained 
		for a given number of epochs, without playing against a 
		Random Agent during training (as opposed to grid-search method), 
		and eventually participate to a tournament.

		Parameters
		----------
		n_epochs: int
			Number of epochs used to retrain an already trained model.
		common_train_time: boolean
			Set to True to adjust all training times of considered 
			models (from the start) so that all models have been 
			trained during the same global number of epochs.
		min_frac: float
			Used to keep only a part of previous trained models to 
			retrain them. Using the previous tournament results, only 
			the models with total score above max_score * min_frac are 
			retrained (max_score is the maximum score achieved by a 
			model during latter tournament).

		Outputs
		-------
		Tournament report: CSV file
			Located at: 'Models/results/(self.tournament_name).csv'.
			File storing the results of each confrontation between 2 
			agents.
		Tournament ranking: TXT file
			Located at: 'Models/results/(self.tournament_name).txt'.
			File ranking the agents using the results of the tournament,
			with total score of each agent displayed.
		"""

		# Look at tournament txt output
		file_path = 'Models/results/' + self.tournament_name + '.txt'
		with open(file_path, "r") as f:
			rankings = f.readlines()
		rankings = rankings[2:]
		rankings = [line[:-1] for line in rankings]
		rankings =[ line.split('\t') for line in rankings ]

		# Get best models
		max_score = max([ int(line[1]) for line in rankings ])
		best_models = [ line for line in rankings 
						if int(line[1]) >= float(max_score)*min_frac ]
		best_models = [ [float(model[2][10:-2]), model[3][11:-1], 
									int(model[-2])] for model in best_models ]

		# Maximum number of epochs used to train the best models
		max_epochs = max([model[2] for model in best_models])

		epsilon_values = []

		print('New training of currently best models')
		print('--------------------------------------\n')
		for model in best_models:
			# Get info
			epsilon = model[0]
			if epsilon not in epsilon_values:
				epsilon_values.append(epsilon)
			training_way = model[1]
			training_ways = training_way.split('vs')
			last_training_way = training_ways[-1]
			assert (last_training_way == 'Self' or 
					last_training_way == 'Random'), \
					'Last method of training is not clear: {}'.format(
															last_training_way)
			prev_epochs = model[2]
			print('epsilon = ', epsilon)
			print('Trained before vs ' + training_way + ' during ' + 
											str(prev_epochs) + ' epochs.')

			# Define training method
			if last_training_way == 'Random':
				random_opponent = True
			else:
				random_opponent = False

			# Name of CSV model
			load_model = ('greedy' + str(epsilon)[0] + '_' + 
							str(epsilon)[2:] + '_vs' + training_way)

			if os.path.exists('Models/' + load_model + '.csv'):
				model_filename = load_model + '_temp'

			# Training time
			if common_train_time:
				epochs = n_epochs + max_epochs - prev_epochs
			else:
				epochs = n_epochs

			_ = train(n_epochs = epochs, epsilon = epsilon, gamma = 1.0, 
						load_model = load_model, filename = model_filename,
						random_opponent = random_opponent, n_games_test = 0, 
						freq_test = -1, n_skip_games = -1, verbose = False)

			use_training = self.delete_temp(load_model, model_filename)

			# Touch file to update number of epochs used to train the model
			if use_training:
				output_path = ('Models/train/GS_epsilon_' + str(epsilon)[0] + 
								'_' + str(epsilon)[2:] + '_vs' + 
								str(training_way) + '.txt')
				with open(output_path, "a") as f:
					f.write(str(n_epochs + prev_epochs) + ',' + str(-1) + 
							',' + str(-1) + ',' + str(-1) + '\n')
			else:
				print('Trained agent is worse than before training.')

			print('--------------------------------------\n')

		# Keep only best values in memory
		self.epsilon_values = epsilon_values

		# Start tournament with trained models
		self.tournament(change_opp = self.change_opp)


if __name__ == "__main__":

	epsilon_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]	

	optimizer = Optimizer(epsilon_values, random_training = True, 
							self_training = True, change_opp = True)

	n_epochs = 5000
	n_games_test = 10000

	# First training with simple opponents
	optimizer.grid_search(n_epochs = n_epochs, n_games_test = n_games_test, 
							freq_test = n_epochs // 5, retrain = False)
	
	# Second training with mixed opponents
	optimizer.grid_search(n_epochs = n_epochs, n_games_test = n_games_test, 
							freq_test = n_epochs //5, retrain = True)

	n_epochs = 40000
	# Further training for best current models
	optimizer.retrain_best_models(n_epochs = n_epochs, 
								common_train_time = False, min_frac = 0.3)

	n_epochs = 50000
	# Further training for best current models
	optimizer.retrain_best_models(n_epochs = n_epochs, 
								common_train_time = False, min_frac = 0.3)

