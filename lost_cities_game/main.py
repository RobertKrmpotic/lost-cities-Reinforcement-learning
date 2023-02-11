import gamemanager

def run_games(n:int = 1000):
    """Run games n times."""
    for x in range(0,n):
        gm = gamemanager.GameManager()
        gm.start_game()
        gm.play_game()
        gm.write_score()

def start_league(species:list,):
    """TODO: Create docstring."""
    pass
