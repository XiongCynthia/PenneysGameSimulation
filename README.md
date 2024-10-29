## Introduction

Penney’s Game is a fascinating mind-bender in probability that’s deceptively simple yet full of surprises. Imagine you’re flipping a fair coin repeatedly, trying to predict which sequence of heads and tails will appear first. Here’s the twist: even if two players choose sequences of the same length, the game is not fair! In fact, the order of the chosen sequences creates unexpected advantages, leading to counterintuitive outcomes. This game of strategic sequence-choosing is both a lesson in the nature of real-life probabilities and an exploration of how small changes can tip the odds in a seemingly fair game.

For more background, check out these resources:
- [Humble and Nishiyama's 2-Page paper](https://www.datascienceassn.org/sites/default/files/Humble-Nishiyama%20Randomness%20Game%20-%20A%20New%20Variation%20on%20Penney%27s%20Coin%20Game.pdf) on their Randomness Game, a variation of Penney's game
- A fun [video by Vsauce](https://www.youtube.com/watch?v=s4tyO4V2im8) on the Humble-Nishiyama Randomness Game
- [Wikipedia article](https://en.wikipedia.org/wiki/Penney%27s_game) on the original Penney's game and variations
  
## Overview

### Game Rules

In our two variations of Penney's game, two players compete with a standard deck of 52 cards. There should be 27 blacks cards and 27 red cards, and the deck should be randomly shuffled. The variations differ by scoring system.

1. Player A and Player B each choose a color sequence of length 3.
2. Begin turning over cards from the shuffled deck and place them in a new pile. Continue until a consecutive sequence matches that of Player A's or Player B's.

    1. Variation 1 (by cards): Give all cards in the pile to the corresponding player.
    2. Variation 2 (by tricks): Give one point to the corresponding player, and reset the pile.

4. Repeat step 2 until all cards in the deck are exhausted. Any leftover cards in the pile do not count towards any additional points.
5. Tally points. The player with the most points win.

    1. Variation 1 (by cards): The number of points each player has corresponds to the number of cards in possession.
    2. Variation 2 (by tricks): The number of points each player has corresponds to the number of times the chosen sequence appeared during the game.

### Simulation Results

![heatmaps.png](figs/heatmaps.png)

Alternatively, see html versions for [cards variation](https://htmlpreview.github.io/?https://github.com/XiongCynthia/PenneysGameSimulation/blob/main/figs/cards.html) and [tricks variation](https://htmlpreview.github.io/?https://github.com/XiongCynthia/PenneysGameSimulation/blob/main/figs/tricks.html) (made with Plotly).

These plots were generated through [RunPenneySimulation.ipynb](https://nbviewer.org/github/XiongCynthia/PenneysGameSimulation/blob/main/RunPenneySimulation.ipynb).

## Documentation

```generate_sequence(seed:int|None, seq:list) -> list```: Generates a randomly shuffled sequence from the given values in seq, and returns it.

Arguments:
- `seed`: Random seed. If None, uses no seed.
- `seq`: Values for the sequence.


<br />

```generate_data(n:int) -> None```: Adds a new deck dataset with n additional randomly shuffled decks to the "data" folder. Stores the datasets as .npy files.

Arguments:
- `n`: Number of decks

<br />

```score_deck(deck:str, seq1:str, seq2:str) -> tuple[int, int, int, int]```: Simulates a game with the given deck and color sequences. Returns the tallied points of each player for each game variation in the following order: p1cards, p2cards, p1tricks, p2tricks.

Arguments:
- `deck`: A deck of cards consisting of 0's (for black) and 1's (for red).
- `seq1`: Color sequence for player.
- `seq2`: Color sequence for opposing player.

<br />

```get_heatmaps(format:str) -> None```: Runs simulations on all deck datasets stored in the "data" folder and stores the results in data/results.json. If the file already exists, no simulation is run. Uses the results data to produce two heatmaps.

Arguments:
- format: Takes 'html' or 'png' as input. Determines file format of the saved heatmap.
