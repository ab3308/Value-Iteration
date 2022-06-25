import numpy as np

class MyAgent(DiceGameAgent):
    
    #dictionary used for the polcy - quick searches of O(1) complexity
    policy = {}

    def __init__(self, game):
        
        # this calls the superclass constructor (does self.game = game)
        super().__init__(game) 
        
        #finding the number of actions and states for this game instance            
        numActions = len(game.actions)
        numStates = len(game.states)
        
        #define array of values to 0 for each state in state space
        valFn = np.zeros(numStates)
        
        #loops until breaking condition met at end
        while True:
            
            #delta - used to check breaking condition, 
            #state index - track iteration's state index
            delta = 0
            stateIndex = 0
            
            for s in game.states:
                #iterate through all states in state space
                
                #assign old value function for state to temp variable
                temp = valFn[stateIndex]
                
                #define array of action values to 0 along with action index, to loop through and calculate new values for current state
                actionValues=np.zeros(numActions)
                actionIndex = 0
                
                for a in game.actions:
                    #loop through all possible actions and pass action and state into below method
                    states, game_over, reward, probabilities = game.get_next_states(a, s)
                    #unpack all next states and relevant values
                    
                    for state, probability in zip(states, probabilities):
                        #loop through all possible next states and add each expected value to the action value for this action/current state combination
                        if(game_over):
                            actionValues[actionIndex] += probability * (reward + 0.91 * temp)
                        else:
                            actionValues[actionIndex] += (probability * (reward + 0.91 * valFn[game.states.index(state)]))
                                             
                    actionIndex += 1
                
                #assign largest action value to value function for current state
                valFn[stateIndex] = max(actionValues)
                
                #add current state and it's corresponding best action to the policy dictionary
                MyAgent.policy[s] = game.actions[np.argmax(actionValues)]
                
                #update delta to be the biggest of either the existing delta value or difference between old/new value function for state
                delta = max(delta, abs(temp - valFn[stateIndex]))
                
                stateIndex += 1
                
            if delta < 0.0025:
                #breaking condition for always-true while loop, theta = 0.0025
                break
        
    def play(self, state):
        
        #play method finds state's corresponding value (action) in policy dictionary
        return MyAgent.policy[state]
    