# import the libraries
import numpy as np
import random

# code the greedy agent
class GreedyAgent( object ):
    def __init__( self, prob_list ):
        self.prob_list = prob_list

    # pull method
    def pull( self, bandit_machine ):
        if np.random.random() < self.prob_list[ bandit_machine ]:
            reward = 1
        else:
            reward = 0

        return reward

# define the parameters of the experiment
trials = 1000
episodes = 200

prob_list = [0.3, 0.8]

bandit = GreedyAgent( prob_list=prob_list )

# variables to save the final results
prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()

# iterate over the episodes
for episode in range( episodes ):
    if episode % 100 == 0:
        print( 'Episode: {} / {}'.format( episode, episodes ) )

    # define variable to save the partial results
    reward_array = np.zeros( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5 )
    accumulated_reward = 0

    for trial in range( trials ):
        # pull the lever of all machines first
        prob_reward = reward_array / bandit_array
        max_prob_reward = np.where( prob_reward == np.max( prob_reward ) )[0] 

        if trial < len( prob_list ):
            bandit_machine = trial

        # In the case the probability of reward are equals for two bandit machines
        #   chose the bandit machine randomly
        elif len( max_prob_reward ) > 1:
            bandit_machine = np.random.choice( max_prob_reward ) 

        # choose the bandit with max value of probability of reward for each bandit machine
        else:
            bandit_machine = max_prob_reward[0]
        
        # get the reward
        reward = bandit.pull( bandit_machine )

        # save partial results
        reward_array[ bandit_machine ] += reward
        bandit_array[ bandit_machine ] += 1
        accumulated_reward += reward

    # compute the partial results
    prob_reward_array += reward_array / bandit_array
    accumulated_reward_array.append( accumulated_reward )
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

# compute the final results
prob_01 = 100*np.round( prob_reward_array[0] / episodes, 2 )
prob_02 = 100*np.round( prob_reward_array[1] / episodes, 2 )

# print them
print( '\nProb Bandit 01:{}% - Prob Bandit 02:{}%'.format( prob_01, prob_02 ) )
print( '\nAvg accumulated reward: {}\n'.format( np.mean( avg_accumulated_reward_array ) ) )
