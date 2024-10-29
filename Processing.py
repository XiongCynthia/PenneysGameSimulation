
def score_deck(deck:str, seq1:str, seq2:str):
    '''
    Simulate a game with the given deck and color sequences.

    Args:
        deck: Decks of cards consisting of 0's (for black) and 1's (for red).
        seq1: Color sequence for player.
        seq2: Color sequence for opposing player.

    Returns:
        p1cards: Player score in the cards game variation
        p2cards: Opposing player score in the cards game variation.
        p1tricks: Player score in the tricks game variation.
        p2tricks: Opposing player score in the tricks game variation.
    '''    
    # Cards scores
    p1cards = 0
    p2cards = 0

    # Tricks scores
    p1tricks = 0
    p2tricks = 0

    t1 = deck[1] # t-1
    t2 = deck[0] # t-2
    pile_count = 2 # Number of cards in the pile
    
    i = 2 # Start with 3rd card in deck
    while i < len(deck): 
        pile_count += 1 # Add next card to the pile
        t0 = deck[i] # t time
        t1 = deck[i-1] # t-1
        t2 = deck[i-2] # t-2
        cur_seq = ''.join(map(str, [t2, t1, t0]))
        
        if seq1 == cur_seq:
            p1cards += pile_count
            p1tricks += 1
            pile_count = 2 # Reset pile count
            i += 3 # See next 3 cards
        elif seq2 == cur_seq:
            p2cards += pile_count
            p2tricks += 1
            pile_count = 2 # Reset pile count
            i += 3 # See next 3 cards
            continue
        else:
            i += 1
    
    return p1cards, p2cards, p1tricks, p2tricks
