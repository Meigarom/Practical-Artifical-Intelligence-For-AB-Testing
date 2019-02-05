# import libraries
import numpy as np
import random

# code the eps greedy agent
class EpsGreedyAgent( object ):
    def __init__( self, prob_list ):
        self.prob_list = prob_list

    def pull( self, action ):
        if np.random.random() < self.prob_list[ action ]:
            reward = 1
        else:
            reward = 0

        return reward

# experiment settings
trials = 1000
episodes = 200
eps_init = 1
decay = 0.05

# exponential decay
eps_array = [( eps_init*(1-decay) )**i for i in range(trials)]

# linear decay
#eps_array = np.linspace( 1, 0, num=trials )

prob_list = [0.3, 0.8]

bandit = EpsGreedyAgent( prob_list=prob_list )

# save final results
prob_reward_array = np.zeros( len( prob_list ) )
accumulated_reward_array = list()
avg_accumulated_reward_array = list()
#eps_array = np.linspace( eps_init, eps_end, num=trials )

# running experiment
for episode in range( episodes ):
    if episode % 100 == 0:
        print( 'Episode: {} / {}'.format( episode, episodes ) ) 

    # define varibles
    reward_array = np.zeros( len( prob_list ) )
    bandit_array = np.full( len( prob_list ), 1.0e-5 )
    accumulated_reward = 0

    # pull armed bandit 
    for trial in range( trials ):
        eps = eps_array[ trial ]

        if eps >= 0.5: # exploration mode
            bandit_machine = np.random.randint( low=0, high=2, size=1 )[0]
        else:          # exploitation mode
            prob_reward = reward_array / bandit_array
            max_prob_reward = np.where( prob_reward == np.max( prob_reward ) )[0]
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
