# BlackJackAI

AI that can play the game of BlackJack with an average win rate of 46% (which is 4% better than a human playing basic strategy).

## Files:
AI project report.pdf - The report. \
requirements.txt - modules/libraries needed to pip install. (makefile does this) \
Makefile - see Instructions below for usage.
## Code:
main.py - contains the Blackjack game connect AI agents with it. \
mdp.py - Markov Decision Process file. \
Qlearning.py - Q-Learning file. \
util.py - utilities file. \
value_iteration.py - the Value Iteration file.

## Instructions:
    make PARAMS='{AI_agent} {games_number}'
Running this command will run {AI_agent} on blackjack for {games_number}. Where {AI_agent} could be either mpd or ql, and {games_number} could be any positive integer. \
### Example:
	make PARAMS='mdp 1000'
### Note:
Running the command `make`, will run the default command: `make PARAMS='mdp 1000'` \
Running the command `make clean` will remove the files (venv) that have been created by makefile.
