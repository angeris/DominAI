# DominAI
An AI for the final project of CS221: A dominoes AI

Fall 2016

No files require arguments, so the following are runnable using the following command

```
python name_of_program.py
```

- *smart_smart.py*: PIMC team plays multiple rounds against IMS team 
- *smart_team.py*: An advanced team against greedy. The advanced team is in the smartPlays function, and it is currently PIMC, but can be quickly modified by commenting and uncommenting a few lines of code to become IMS (lines 62-71). The alpha and beta for depth can be changed on line 59, and the number of samples in the calculate_expectation function. 
- *main.py*: Requires two human players, a human to input moves, and a domino set. Plays PIMC team against humans. 
- *oracle.py*: Negamax oracle team against greedy team. 

Outputs for *smart_smart.py*, *smart_team.py*, and *oracle.py* can be found in the *results_texts* folder.

Negamax algorithms used by IMS and PIMC can be found in the *algorithms* folder. Game and domino classes are in *domino.py*. 

There are some other files in this repo, that are older iterations of our project or miscellaneous attempts.
