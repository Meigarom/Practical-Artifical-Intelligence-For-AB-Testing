import numpy as np
import random

# write the random agent class
class RandomAgent( object ):
    def __init__( self, prob_list ):
        # inner-class variables
        self.prob_list = prob_list

    # Pull method
    def pull( self, bandit_machine ):
        if np.random.random() < self.prob_list[ bandit_machine ]:
            reward = 1
        else:
            reward = 0

        return reward

# define the parameters of the experiment
prob_list=[0.3, 0.8]
trials = 1000
episodes = 200

# instantiate the class
bandit = RandomAgent( prob_list=prob_list )

# define the list of the final results
prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()

# iterate over the episodes
for episode in range( episodes ):
    reward_array = np.zeros( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5 )
    accumulated_reward = 0

    # iterate over the trials
    for trial in range( trials ):
        # define the random strategy
        bandit_machine = np.random.randint( low=0, high=2, size=1 )[0]

        # get the reward
        reward = bandit.pull( bandit_machine )

        # compute the partial results
        reward_array[ bandit_machine ] += reward
        bandit_array[ bandit_machine ] += 1
        accumulated_reward += reward

    # save the partial results
    prob_reward_array += np.true_divide( reward_array, bandit_array )
    accumulated_reward_array.append( accumulated_reward )
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

# compute the final results
prob_01 = 100*np.round( prob_reward_array[0] / episodes, 2 )
prob_02 = 100*np.round( prob_reward_array[1] / episodes, 2 )

# print the final results
print( '\nProb Bandit 01:{}% - Prob Bandit 02:{}%'.format( prob_01, prob_02 ) )
print( '\nAvg accumulated reward: {}\n'.format( np.mean( avg_accumulated_reward_array ) ) )
