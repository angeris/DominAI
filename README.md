# DominAI
An AI for the final project of CS221: A dominoes AI

Fall 2016

Roadmap of files in this repository: 

- *domino.py*: Contains a Domino class which represents a domino and a Dominoes class that tracks the state of the game. Dominoes is used by p-negamax to simulate possible games as well. 
- *main.py*: Allows three humans to play with an AI player. Deprecated, because no longer evaluating performance against humans. 
- *oracle.py*: The advanced AI players know the allocation of tiles in the game. 
- *smart_team.py*: Two advanced AI players play multiple rounds against greedy players. 
- *greedy_vs_smarter.py*: An early version of smart_team.py where an advanced player and greedy player played against a greedy team. Deprecated. 
- *test.py*: Tests our negamax function on the halving game 
- **algorithms**
	- *negamax.py*: traditional negamax
	- *p_negamax.py*: our imperfect minimax search 

To pin a smart team against a greedy team, do

```
python smart_team.py
```

Can also run a negamax oracle: 

```
python oracle.py 
```
