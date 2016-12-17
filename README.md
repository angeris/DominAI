# DominAI
An AI for the final project of CS221: A dominoes AI

Fall 2016

No files require arguments, so the following are runnable using 

```
python name_of_program.py
```

- *smart_smart.py*: PIMC team plays multiple rounds against IMS team 
- *smart_team.py*: An advanced team against greedy. The advanced team is in the smartPlays function, and it is currently PIMC, but can be quickly modified by commenting and uncommenting a few lines of code to be IMS. 
- *main.py*: Requires two human players, a human to input moves, and a domino set. Plays PIMC team against humans. 
- *oracle.py*: Negamax oracle team against greedy team. 

Negamax algorithms used by IMS and PIMC can be found in the **algorithms** folder. Game and domino classes are in *domino.py*. 

There are some other files in this repo, that are older iterations of our project or miscellaneous attempts.
