For this project, dice_game.py was provided and I was tasked with implementing an agent which optimises the score achieved in the described dice game.
My implementation is found in myAgent.py

=====================================
||             MyAgent             ||
=====================================

(Please see the attached document: ReadmeReferences.pdf to view referenced images and data.)

---------
The game:
---------
    
    The game in hand is a dice game. Rules are simple:
    
    1. Start with 0 points.
    2. n dice are rolled.
    3. You can either:
       a) Stick with the values. If 2+ dice are the same, all values are flipped. Total added to your score. Game over.
       b) Reroll any combination of dice. This incurs a penalty of 1 point. You can reroll multiple times before sticking.

-----------------
Algorithm choice:
-----------------
    
    - For my algorithm, I chose to implement value iteration which calculates an optimal function for each state. 
    
    - In this specific case, it provides an optimal policy of actions for each possible set of dice rolls. 
    
    - For example, it provides the best move when you roll two 3's and a 4.

--------------------------
How value iteration works: 
--------------------------

    - Essentially, the goal of value iteration is to update the value function for each state until converging on the optimal solution. 
    
    - Using the pseudocode (reference 1), you can see that the value function, v(s) is updated with each iteration until the 
      change in value is below a certain threshold (theta).
    
    - To update the value, v(s), you use the Bellman optimality equation (reference 2).
      This equation calculates the action value for all possible actions on that state.
      It then selects the largest action value and assigns it to v(s).
    
    - The corresponding action for this value is added to the policy for that state. (see final line of reference 1)
    
    - For each action, you use the reward, probability and value function of all possible next states 
      to calculated the expected value of the action on that current state.
      
    - As previously said, the values are continously updated until the change in value is below the threshold.
    
    - At this point, the optimal policy is produced which contains the best action for each state to maximise it's value function.

----------------------------------
How I implemented value iteration:
----------------------------------

Initialising all value functions to be 0 before beginning value iteration:
    
    - I used numpy.zeros while passing in the number of states (game.states length)
    
    - This creates a new array of zeros with length equal to the number of states.

Looping until below threshold (theta):
    
    - For this, I used an always-true loop to effectively recreate the do... until... seen in the pseudocode.
    
    - This allows me to check the breaking condition (delta < theta) at the end of the while loop.

Initialising delta and updating delta:
    
    - Initialised with delta = 0 at the beginning of each iteration of while loop
    
    - Before checking the break condition, delta is set to the biggest of either the current delta
      value or the difference between the old and new value function for a state.
    
Looping through all states:

    - I used a for loop to iterate through all states in game.states
    
    - Inside the while loop, but before the for loop, I define stateIndex = 0
    
    - This is to track the state index and match with it's corresponding value function
      without the lengthy process of finding the state index inside game.states.
    
    - Using the for loop enabled me to directly use the state corresponding to the current iteration
    
    - In each iteration, I assign the current value function of the state to a temporary variable, using
      the state index to find it within the array of values.

    - I also define an actionIndex = 0 for the same purpose as stateIndex = 0 but for actions. Also, I initialise
      an array of action values of length (number of actions in game.actions) filled with 0's using numpy.zeros.
      
Looping through all actions, calculating action values:

    - I used a for loop to iterate through each action in game.actions
    
    - I pass the state from the current iteration and action from the action iteration into
      game.get_next_states to find all possible next states and their values for this action.
    
    - First, I unpack these next states and their corresponding probabilities, rewards etc.
    
    - Using these values, the expected value for each next state is calculated and added to the action value
      in the correct index of the actionValues array. 
     
    - Once all next states dealt with, the iteration is complete and it moves onto the next action
      and increments action index
      
Updating the value function and creating the policy:

    - Using max(), the largest action value for the state is assigned to it's value function
    
    - Using numpy.argmax() to find the largest value's action index, the corresponding action is found from game.actions.
    
    - This action is added to the policy as a key-value pair in a dictionary.
    
    - The key is the state, the value is the action. This enables fast lookups in the play() method.
    
----------------------------------------------------------------------
How I decided the optimal values for my discount factor and threshold:
----------------------------------------------------------------------
(The results can be found in the attached references pdf)
    
    - To decide my values, I conducted testing to compare the effect of the discount factor and threshold on runtime and avg.
      score since these are the two most important factors in this implementation.
    
    - Please note, for each value - only 1 test occurred barring clear anomalies. 
      If I had more time, I would conduct more tests at each level to calculate an average.
    
    - Furthermore, it is worth noting that the actual game instances were not identical for each test meaning score may vary based on this.

Discount factor (reference 3):

    - I chose to test the values from 0.8 to 1 in increments of 0.02
    - As you can see from reference x, the greater the discount factor, the greater the average score.
    - However, as they increase so does the time taken.
    - The average score is greatest between a discount factor of 0.92 and 0.94.
    - The time grows in a relatively linear fashion until a discount factor of around 0.9.
    - Hence, I selected a discount factor of 0.91 as this offers a high average score
      without an un-proportionate increase in time.

Threshold (theta) (reference 4):

    - I chose to test values of theta ranging from 0.000001 to 1, in powers of 10 while also recording the midpoints.
    - As you can see from reference y, theta has a small effect on the score in my testing.
      Between max. and min. the difference in score is around 0.05.
    - However, it has a big effect on runtime. From max to min there is a difference of just under 20 seconds.
    - Hence, once again I chose the middleground. Although it has little effect, I chose a value 
      theta producing around the median of average score and also runtime.
    - I selected a value of 0.0025 for theta having previously experimented with 0.001 heavily.
    - Between 0.001 and 0.0025 (theta value), the score varies by a very small margin but over a second is knocked off 
      the running time.
    - Hence, I increased the threshold to 0.0025 as it had marginal effect on score relative to time.
    
My final values:

    - Threshold = 0.0025
    - Discount factor = 0.91

If you wanted to increase score further, simply increase the discount factor and reduce the threshold. 
This will lead to a greater runtime, but will lead to better results when playing the game.
