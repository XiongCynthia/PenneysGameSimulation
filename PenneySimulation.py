# Data computation and storage
import numpy as np
import os
import json

# Jupyter notebook
from IPython.display import clear_output

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go



def generate_sequence(seed:int|None, seq:list) -> list:
    '''
    Randomly generate a sequence of the given values.

    Args:
        seed: Random seed. If None, uses no seed.
        seq: Values for the sequence.
    
    Returns:
        seq: Randomly shuffled sequence.
    '''
    np.random.seed(seed)
    np.random.shuffle(seq)
    return seq


def generate_data(n:int) -> None:
    '''
    Adds a new deck dataset with n additional randomly shuffled decks to the "data" folder.
    '''
    SEED = 420
    np.random.seed(SEED)

    deck_data = np.empty(n, dtype='<U52') # Array of n card decks
    
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


def score_deck(deck:str, seq1:str, seq2:str) -> tuple[int, int, int, int]:
    '''
    Simulates a game with the given deck and color sequences.

    Args:
        deck: A deck of cards consisting of 0's (for black) and 1's (for red).
        seq1: Color sequence for player.
        seq2: Color sequence for opposing player.

    Returns:
        p1cards: Player score in the cards game variation.
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


def __instantiate_dataset() -> np.ndarray:
    '''
    Returns an 8x8 numpy array, with the diagonal filled with NaN.
    '''
    data = np.zeros((8,8))
    np.fill_diagonal(data, np.nan)
    return data


def __process_dataset(data) -> list[float]:
    '''
    Finalize the dataset.
    '''
    # Decimal to percent
    data = data*100
    # Round all values to the nearest whole number
    data = np.round(data)
    # Flip on the axis such that the origin (0,0) is at the bottom-let
    data = np.flip(data, axis=1)
    # To list, because json can't directly save a numpy array
    return data.tolist()


def __run_simulations() -> None:
    '''
    Simulate both variations of Penney's game and generate win probabilities by players' color sequences.
    Results and N (for N simulations total) are saved in a json file.
    '''
    # Color sequences:
    #      ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    seqs = ['000', '001', '010', '011', '100', '101', '110', '111']

    # Datasets
    cards = __instantiate_dataset() # Number of wins for player in cards game variation
    tricks_ties = __instantiate_dataset() # Number of ties with cards game variation
    tricks = __instantiate_dataset() # Tricks game variation
    cards_ties = __instantiate_dataset() # Tricks game variation
    N = 0 # Number of decks to simulate on

    # Simulate on all available decks in the data folder
    for file in os.listdir('data'):
        filename = os.fsdecode(file)
        # Skip files that are not .npy files
        if not filename.endswith('.npy'):
            print(f'Invalid file extension found: {filename}')
            continue
        deck_data = np.load(f'data/{filename}', allow_pickle=True)

        for deck in deck_data:
            # Show progress
            if N%100_000 == 0:
                clear_output()
                print(f'Running a simulation on deck #{N} from {filename}.')            
            N += 1

            # Fill datasets
            for i, seq2 in enumerate(seqs):
                for j, seq1 in enumerate(seqs):
                    # Skip if sequence 1 and sequence 2 are the same (illegal in-game)
                    if i == j:
                        continue
                    
                    p1cards, p2cards, p1tricks, p2tricks = score_deck(deck, seq1, seq2)
                    
                    # Cards
                    if p1cards > p2cards:
                        cards[i,j] += 1
                    elif p1cards == p2cards:
                        cards_ties[i,j] += 1
                    # Tricks
                    if p1tricks > p2tricks:
                        tricks[i,j] += 1 
                    elif p1tricks == p2tricks:
                        tricks_ties[i,j] += 1
    clear_output()
    print(f'Ran {N} simulations.')
    
    # Compile data into dictionary
    data = {}
    data['cards'] = __process_dataset(cards/N)
    data['cards_ties'] = __process_dataset(cards_ties/N)
    data['tricks'] = __process_dataset(tricks/N)
    data['tricks_ties'] = __process_dataset(tricks_ties/N)
    data['N'] = N

    # Save dictionary as json file
    with open("data/results.json", "w") as f: 
        json.dump(data, f)
        print("Saved results.json in data folder.")
    return


def __make_annots(wins:np.ndarray, ties:np.ndarray) -> np.ndarray:
    '''
    Generate annotations for heatmap values.
    Annot format: Win(Tie)

    Args:
        wins: 8x8 array of win probabilities.
        ties: 8x8 array of tie probabilities.

    Returns:
        annots: 8x8 array of heatmap cell annotations (includes win and tie probabilities).
    '''
    annots = []
    for i in range(8):
        row = []
        for j in range(8):
            if np.isnan(wins[i,j]):
                row.append('')
            else:
                row.append(f'{str(int(wins[i,j]))} ({str(int(ties[i,j]))})')
        annots.append(row)
    return np.array(annots)


def __prepare_html(wins:np.ndarray, ties:np.ndarray, title:str) -> go.Figure :
    '''
    Produces a Plotly heatmap.

    Args:
        wins: 8x8 array of win probabilities.
        ties: 8x8 array of tie probabilities.
        title: Plot title.
    
    Returns:
        fig: Plotly heatmap
    '''
    # Settings
    TITLE_SIZE = 22
    LABEL_SIZE = 18
    TICK_LABEL_SIZE = 16
    
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    annots = __make_annots(wins, ties)
    fig = go.Figure(go.Heatmap(z=wins, x=seqs, y=seqs[::-1],
                               text=annots, texttemplate='%{text}', textfont={'size':15},
                               hovertemplate='Me: %{x}<br />Opponent: %{y}',
                               name='', # Remove trace in tooltip
                               colorscale='Blues', zmin=0, zmax=100,
                               colorbar=dict(ticksuffix='%')
                              ),
                   layout=go.Layout(plot_bgcolor='lightgray'))
    fig.update_layout(width=700, height=700, 
                      title=title, title_font_size=TITLE_SIZE,
                      title_x=0.5, title_y=0.92,
                      xaxis=dict(title='Me', title_font=dict(size=LABEL_SIZE), tickfont=dict(size=TICK_LABEL_SIZE)), 
                      yaxis=dict(title='Opponent', title_font=dict(size=LABEL_SIZE), tickfont=dict(size=TICK_LABEL_SIZE)))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.update_traces(xgap=1, ygap=1, textfont_size=13)
    fig['layout']['yaxis']['autorange'] = 'reversed'
    return fig


def __create_seaborn(data:np.ndarray, annots:np.ndarray,
                     ax:plt.Axes|None = None, hide_yticks:bool = False, title:str|None = None
                    ) -> tuple[plt.Figure, plt.Axes]:
    '''
    Produces a Seaborn heatmap.

    Args:
        data: 8x8 array of win probabilities.
        annots: 8x8 array of annotations (includes win and tie probabilities).
        ax: The Axes object to add heatmap to. If None, create a new Figure.
        hide_yticks: If True, remove y ticks and labels from the heatmap.
        title: Plot title.

    Returns:
        fig, ax: Seaborn heatmap
    '''
    seqs = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    
    settings = {
        'vmin': 0,
        'vmax': 100,
        'linewidth': 0.01,
        'cmap': 'Blues',
        'cbar': False,
        'annot': annots,
        'fmt': ''
    }
    TICKLABEL_SIZE = 12
    TITLE_SIZE = 18
    
    if ax is None:
        # Create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
    else:
        # Get the parent figure
        fig = ax.get_figure()

    sns.heatmap(data=data, ax=ax, **settings)

    ax.set_xticklabels(seqs, fontsize=TICKLABEL_SIZE)
    ax.set_yticklabels(seqs[::-1], fontsize=TICKLABEL_SIZE)
    ax.set_title(title, fontsize=TITLE_SIZE)
    ax.set_facecolor('lightgray')
    
    if hide_yticks:
        ax.set_yticks([])
    
    return fig, ax

    
def get_heatmaps(format:str) -> None:
    '''
    Runs simulations on all deck datasets stored in the "data" folder (if not done yet), 
    and uses the data results to produce two heatmaps.

    Args:
        format: Takes 'html' or 'png' as input. Determines file format of the saved heatmap.
    '''
    # Run simulations, if not done yet
    if not os.path.isfile('data/results.json'):
        __run_simulations()
    
    # Get data results from simulation
    with open('data/results.json') as json_file:
        data = json.load(json_file)
    cards = np.array(data['cards'])
    cards_ties = np.array(data['cards_ties'])
    tricks = np.array(data['tricks'])
    tricks_ties = np.array(data['tricks_ties'])
    N = data['N']
        
    if format == 'html':
        # Variation 1 (cards)
        cards_fig = __prepare_html(cards, cards_ties, 
                                   title=f'My Chance of Winning by Cards<br />(from {N} Random Decks) [Win(Tie)]')
        path = 'figs/cards.html'
        cards_fig.write_html(path)
        print(f'{path} saved successfully.')
        cards_fig.show()
        
        # Variation 2 (tricks)
        tricks_fig = __prepare_html(cards, cards_ties, 
                                    title=f'My Chance of Winning by Tricks<br />(from {N} Random Decks) [Win(Tie)]')
        path = 'figs/tricks.html'
        tricks_fig.write_html(path)
        print(f'{path} saved successfully.')
        tricks_fig.show()
    
    elif format == 'png':
        # Figure specifications
        LABEL_SIZE = 14
        TICK_SIZE = 10
        ANNOT_SIZE = 8
        
        fig, ax = plt.subplots(1, 2, 
                               figsize=(16,8), 
                               gridspec_kw={'wspace':.05})
    
        # Left heatmap
        cards_annots = __make_annots(cards, cards_ties)
        __create_seaborn(cards, cards_annots, ax[0], 
                         title=f'My Chance of Winning by Cards\n(from {N} Random Decks)')
        ax[0].set_xlabel('Me', fontsize=LABEL_SIZE)
        ax[0].set_ylabel('Opponent', fontsize=LABEL_SIZE)
    
        # Right heatmap
        tricks_annots = __make_annots(tricks, tricks_ties)
        __create_seaborn(tricks, tricks_annots, ax[1], 
                         title=f'My Chance of Winning by Tricks\n(from {N} Random Decks)',
                         hide_yticks=True)
        ax[1].set_xlabel('Me', fontsize=LABEL_SIZE)
    
        # Add custom colorbar
        cbar_ax = fig.add_axes([.92, 0.11, 0.02, .77])
        cb = fig.colorbar(ax[1].collections[0], cax=cbar_ax, format='%.0f%%')
        cb.outline.set_linewidth(.2)
        
        # Add caption
        fig.suptitle('Cell text are formatted as follows: Chance of Win (Chance of Tie)', x=0.3, y=0.01)
        fig.savefig('figs/heatmaps.png', bbox_inches='tight')

    else:
        print(f'{format} is not a valid file format. Please use \'png\' or \'html\'.')
    return
