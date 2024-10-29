import numpy as np
import os
from IPython.display import clear_output

def generate_sequence(seed:int|None, seq:list) -> list:
    '''
    Randomly generate a sequence of the given values.

    Args:
        seed: Random seed
        seq: Values for the sequence
    '''
    np.random.seed(seed)
    np.random.shuffle(seq)
    return seq

def generate_data(n: int) -> None:
    '''
    Augments the existing data with n additional simulations.
    '''
    deck_data = np.empty(n, dtype=np.ndarray) # All card decks
    
    for iter in range(n):
        # Show progress
        if iter%100_000 == 0:
            clear_output()
            print(f"Generated {iter}/{n} card decks.")
            
        deck = np.repeat(['0','1'], 26) # Instantiate a deck of 52 cards
        generate_sequence(None, deck) # Shuffle deck
        deck_data[iter] = ''.join(deck) # Save deck as string
    clear_output()
    print(f"Generated {n}/{n} card decks.")
    
    print("Saving decks...")
    i = 0
    while os.path.exists(f'data/decks_{i}.npy'):
        i += 1
    np.save(f'data/decks_{i}.npy', deck_data)
    print("Done.")
    return