# BigSmallGame
An Idea learned from Jinxong 

##Game Idea:

for 2 players
each player has bank of 100 points
in 5 rounds the players secretly bids a number to be drawn out of the bank to play in the round, then reveal the number to each other. The person with the bigger number wins the round and the first person to win 3 rounds win the game.

#Example:

initially player A and B each have 100 points in their bank.
[1st round] A plays 5 and B plays 20
result: B has 1 win; A and B each have 95 and 80 points left,
[2nd round] A plays 9 and B plays 6
result: A, B each has 1 win; A, B have 86 and 74 points left.
[3rd round] A plays 55 and B plays 37
result: A has 2 win and B has 1; A, B have 33 and 37 points left.
[4th round] A plays 10 and B plays 22
result: A, B each has 2 win; A, B have 23 and 15 points left.
[2nd round] A plays 22 and B plays 15
result: A have 3 win, A won the game!

#Analysis
The best outcome for a player is to bid a number just slightly higher than the opponent. If we could foretell that the opponent bids 30 in the first round, it would be best for us to bid 31, or 0, and would be worst to bid 29.
For a human player, we would tend to guess if the opponent wants to go big or go small and act on it.
I believe that to guess the trends of the opponents behaviour is purely a psychological effect. Meaning if the opponent chooses the numbers *randomly*, the long term probabilty of winning would tend to 50%.

#the plan
1. build a q learning algorithm to play this game against itself
2. build a chatbot for the q learning algorithm to play with human
3. find or develop the underlying game theory
