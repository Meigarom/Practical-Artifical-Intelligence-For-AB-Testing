# import libraries
from scipy.stats import binom, beta
from matplotlib import pyplot as plt

import numpy as np
import random

# Reward Probability Plot function
def reward_prob( success_array, failure_array ):
    linestyles = ['-', '--']
    x = np.linspace( 0, 1, 1002 )[1:-1]

    plt.clf()
    plt.xlim( 0, 1 )
    plt.ylim( 0, 30 )

    for a, b, ls in zip( success_array, failure_array, linestyles ):
        dist = beta( a, b )

        plt.plot( x, dist.pdf( x ), ls=ls, c='black', 
                  label=r'$\alpha=%.1f,\ \beta=%.1f$' % ( a, b ) )
        plt.draw()
        plt.pause( 0.001 )

        plt.legend( loc= 0 )

    print( 'Success: {}'.format( success_array ) )
    print( 'Failure: {}'.format( failure_array ) )

# Thompson agent class
class ThompsonAgent( object ):
    def __init__( self, prob_list ):
        self.prob_list = prob_list

    def pull( self, bandit_machine ):
        if np.random.random() < self.prob_list[ bandit_machine ]:
            reward = 1
        else:
            reward = 0

        return reward

# experiment settings
trials = 1000
episodes = 200
prob_list = [0.3, 0.8]

bandit = ThompsonAgent( prob_list )

# results storage
prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()

# running experiment
for episode in range( episodes ):
    if episode % 100 == 0:
        print( 'Episode: {}/{}'.format( episode, episodes ) )

    success_array = np.ones( len( prob_list ) )
    failure_array = np.ones( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5 )
    accumulated_reward = 0

    # iterate over trials
    for trial in range( trials ):
        # Thompson strategy
        prob_reward = np.random.beta( success_array, failure_array )
        bandit_machine = np.argmax( prob_reward )
                
        # get the reward
        reward = bandit.pull( bandit_machine )

        # get results
        if reward == 1:
            success_array[ bandit_machine ] += 1
        else:
            failure_array[ bandit_machine ] += 1

        # save partial results
        bandit_array[ bandit_machine ] += 1
        accumulated_reward += reward

    # compute partial results
    accumulated_reward_array.append( accumulated_reward )
    prob_reward_array += success_array / bandit_array
    avg_accumulated_reward_array.append( np.mean( accumulated_reward_array ) )

# compute final results
prob_01 = 100*np.round( prob_reward_array[0] / episodes, 2 )
prob_02 = 100*np.round( prob_reward_array[1] / episodes, 2 )

print( 'Prob 01:{}% - Prob 02:{}%'.format( prob_01, prob_02 ) )
print( 'Avg accumulated reward: {}'.format( np.mean( accumulated_reward_array ) ) )
