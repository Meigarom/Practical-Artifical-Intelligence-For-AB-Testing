from flask import Flask, redirect, render_template, url_for, request
import numpy as np

app = Flask( __name__ )

class OmniscientAgent( object ):
    def __init__( self, prob_list, trials, episodes ):
        # inner-class variables
        self.prob_list = prob_list
        self.trials = trials
        self.episodes = episodes

        self.trial = 0
        self.episode = 0
        self.current_bandit = 0
        self.accumulated_reward = 0

        self.reward_array = np.zeros( len( self.prob_list ) )
        self.prob_reward_array = np.zeros( len( self.prob_list ) )
        self.bandit_array = np.full( len( self.prob_list ), 1.0e-5 )
        self.accumulated_reward_array = list()
        self.avg_accumulated_reward_array = list()

    # setters
    def set_current_bandit( self, bandit_machine ):
        self.current_bandit = bandit_machine
        return None

    def set_reward_array( self, bandit_machine, reward ):
        self.reward_array[ bandit_machine ] += reward
        return None

    def set_bandit_array( self, bandit_machine ):
        self.bandit_array[ bandit_machine ] += 1
        return None

    def set_trial( self, reset ):
        if reset == 1:
            self.trial = 0
            self.reward_array = np.zeros( len( self.prob_list ) )
            self.bandit_array = np.full( len( self.prob_list ), 1.0e-5 )
            self.accumulated_reward = 0
        else:
            self.trial += 1
        return None

    def set_episode( self ):
        self.episode += 1
        return None

    def set_prob_reward_array( self ):
        self.prob_reward_array+= self.reward_array / self.bandit_array
        return None

    def set_accumulated_reward( self, reward ):
        self.accumulated_reward += reward
        return None

    def set_append_accumulated_reward( self ):
        self.accumulated_reward_array.append( self.accumulated_reward ) 
        return None

    def set_append_avg_accumulated_reward( self ):
        self.avg_accumulated_reward_array.append( np.mean( self.accumulated_reward_array ) )
        return None

    def reset_episode( self ):
        self.episode = 0
        return None

    # getters
    def get_prob_list( self ):
        return self.prob_list

    def get_current_bandit( self ):
        return self.current_bandit

    def get_prob_reward_array( self ):
        return self.prob_reward_array

    def get_avg_accumulated_reward_array( self ):
        return self.avg_accumulated_reward_array

    def get_trial( self ):
        return self.trial

    def get_trials( self ):
        return self.trials

    def get_episode( self ):
        return self.episode

    def get_episodes( self ):
        return self.episodes


@app.route( '/home' )
def index():
    # retrieve the agent from the applicaton object
    agent = app.config['AGENT']

    print( 'Episode: {} / {}'.format( agent.get_episode(), agent.get_episodes() ) )
    print( 'Trial: {} / {}'.format( agent.get_trial(), agent.get_trials() ) )
    if agent.get_episode() > agent.get_episodes():
        # compute the final probabiliry of reward from each bandit machine
        prob_reward_array = agent.get_prob_reward_array()
        prob_01 = 100*np.round( prob_reward_array[0] / agent.get_episodes(), 2 )
        prob_02 = 100*np.round( prob_reward_array[1] / agent.get_episodes(), 2 )

        # average the accumulate reward
        avg_accumulated_reward = agent.get_avg_accumulated_reward_array()

        # print the final results
        print( '===> Final Result ==== ' )
        print( '\n Prob Bandit 01:{}% - Prob Bandit 02:{}%'.format( prob_01, prob_02 ) )
        print( '\n Avg accumulated reward:{}\n'.format( np.mean( avg_accumulated_reward ) ) )

        # reset the episodes
        agent.reset_episode()

        return redirect( url_for( 'index' ) )

    if agent.get_trial() > agent.get_trials():
        print( '===> trials are over' )
        # increase the episode
        agent.set_episode()

        # compute the partial probability of reward from each bandit machine
        agent.set_prob_reward_array()

        # append the accumulated reward from each bandit machine
        agent.set_append_accumulated_reward()

        # append the avg accumulated reward
        agent.set_append_avg_accumulated_reward()

        # reset the trial and the initial variables
        agent.set_trial( reset=1 )

        # get partial results
        partial_result = agent.get_prob_reward_array()
        prob_01 = partial_result[0] / agent.get_episode()
        prob_02 = partial_result[1] / agent.get_episode()

        # print the partial results
        print( '\nProb Bandit 01:{} - Prob Bandit 02:{}\n'.format( prob_01, prob_02 ) )

        return redirect( url_for( 'index' ) )

    else:
        # code the Omniscient Agent
        bandit_machine = np.argmax( agent.get_prob_list() )

        # set the current bandit machine
        agent.set_current_bandit( bandit_machine )

        # pick up the web page
        if bandit_machine == 0: #web page with RED yes button
            return render_template( 'layout_red.html' )
        else:
            return render_template( 'layout_blue.html' )

        return None

@app.route( '/yes', methods=['POST'] )
def yes_event():
    agent = app.config['AGENT']

    # set the reward
    reward = 1

    # get the current bandit machine
    bandit_machine = agent.get_current_bandit()

    # add a reward to the bandit machine
    agent.set_reward_array( bandit_machine, reward )

    # incrase how many times the bandit machines gets the lever pulled
    agent.set_bandit_array( bandit_machine )

    # sum the accumulated reward
    agent.set_accumulated_reward( reward )

    # increase the number of trial
    agent.set_trial( reset=0 )

    return redirect( url_for( 'index' ) )

@app.route( '/no', methods=['POST'] )
def no_event():
    agent = app.config['AGENT']

    # set the reward
    reward = 0

    # get the current bandit machine
    bandit_machine = agent.get_current_bandit()

    # add a reward to the bandit machine
    agent.set_reward_array( bandit_machine, reward )

    # incrase how many times the bandit machines gets the lever pulled
    agent.set_bandit_array( bandit_machine )

    # sum the accumulated reward
    agent.set_accumulated_reward( reward )

    # increase the number of trial
    agent.set_trial( reset=0 )
    return redirect( url_for( 'index' ) )

if __name__ == '__main__':
    trials = 100
    episodes = 20

    prob_list = [0.3, 0.8]
    agent = OmniscientAgent( prob_list, trials, episodes )
    app.config['AGENT'] = agent

    app.run()
