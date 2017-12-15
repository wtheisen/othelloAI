Sick Othello AI

William Theisen
Jose Badilla
Michael Burke
Daniel Jasek


Server:
    - Re-write curves to use variable length based on # of turns
    - Allow creation of game object to specify additional rules
    - Allow for creation of game object to specify different AI models
    - Fix bugs related to game crashing
    - Write wrapper functions for different playing styles

Front-End:
    - A shit-ton

Database:
    - Indexing for the gamestates to speed things up
    - Different tables for the different AI models?

Todo:

- turn rollback (Billy)
- possible move locations (Danny)
- stats
    - game stats
        - point differential graph (Danny)
    - user stats (Michael/Billy)
        - wins/losses/ties
        - average score
        - winning pct
    - global stats (Pat - backend)
        - number of entries in the database
        - board states with the highest/lowest win pct
        - win pct/vs entries in the database
    - adjusting difficulty
        - 1st level - random
- turn skipping if no moves available for both the AI.s and humans - Michael
- invalid move - Michael // Jose -- frontend
- end of game - Michael

