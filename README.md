# Instructions:
The project was created with Python 3.7.9
The pip environment for the project can be created using the requirements.txt file.


Coin machine: 
it can be run via the coin_machine.main file.
I first started with a solution which was working relatively well but became too slow for larger amounts. The problem was that I couldn't find
a good way of pruning out unfeasible solutions using itertools, because of the order in which itertools was returning the combinations.
Therefore I just googled and found a solution to a similar problem (just counting the number of possible solutions) and adapted it to the problem.
This performed quite well, but recursion was creating problems. 
I then noticed I was trying to solve the wrong problem - returning all the combinations rather than number of combinations, but now I don't have time to change it back. 
I'd need to go back to look into this but time is up!
Tests can be run with pytest

Energy Demand: 
All the info is in the jupyter file. If you can't get the jupyter to run, I saved the output in a html file.

