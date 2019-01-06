# import the libraries
import numpy as np
import random

# code the random agent class
class RandomAgent( object ):
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
prob_list = [0.3, 0.8]
trials = 1000
episodes = 200

# instantiate the class
bandit = RandomAgent( prob_list=prob_list )

# define the variables to save the final results
prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()

# iterate over the episodes
for episode in range( episodes ):
    if episode % 10 == 0:
        print( 'Episode: {} / {}'.format( episode, episodes ) )

    # define variable to save the partial results
    reward_array = np.zeros( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5 )
    accumulated_reward = 0

    # iterate over the triasl
    for trial in range( trials ):
        #define the random strategy
        bandit_machine = np.random.randint( low=0, high=2, size=1 )[0]

        # get the reward
        reward = bandit.pull( bandit_machine )

        # compute the partial results
        reward_array[ bandit_machine ] += reward
        bandit_array[ bandit_machine ] += 1
        accumulated_reward += reward

    # save them
    prob_reward_array += reward_array / bandit_array
    accumulated_reward_array.append( accumulated_reward )
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

# compute the final results
prob_01 = 100*np.round( prob_reward_array[0] / episodes, 2 )
prob_02 = 100*np.round( prob_reward_array[1] / episodes, 2 )

# print them
print( '\nProb Bandit 01:{}% - Prob Bandit 02:{}%'.format( prob_01, prob_02 ) )
print( '\nAvg accumulated reward: {}\n'.format( np.mean( avg_accumulated_reward_array ) ) )

