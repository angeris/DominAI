from domino import Dominoes

def bad(possible_moves, knowledge_of_game):
    '''
    @params:
        - possible_moves: dominoes that I can place
        Not empty
        - knowledge_of_game: ignore, who cares
    TODO: flip if you can place on either side
    '''
    # Greedy algorithm
    assert (possible_moves) # list of moves
    maximum = 0
    ret = possible_moves[0]
    for domino, placement in possible_moves:
        if domino[1] + domino[0] > maximum:
            maximum = domino[1] + domino[0]
            ret = (domino, placement)
    return ret

# Controller
def setupGame():
    '''
    Enter the tiles that I have.
    Enter who is starting the game.
    A little bit of checking about validity of inputs
    and organizing/standardizing/cleaning
    but please don't input something too crazy.
    @returns
        - Dominoes
    '''
    print 'Welcome.'
    tiles = []
    for i in range(7):
        for j in range(i, 7):
            tiles.append((i, j))
    while True:
        my_tiles_input = raw_input('Enter my tiles (e.g. 4-5) seperated by spaces: ').split()
        if len(my_tiles_input) == 7:
            break
        else:
            print "I need 7 tiles!"
    my_tiles = []
    for t in my_tiles_input:
        my_tiles.append(tuple(sorted([int(num) for num in t.split('-')])))
    print 'You have:', my_tiles
    print
    print 'Players are numbered as the following:'
    print '(0 = me, 1 = opponent on my right,'
    print '2 = partner across from me, 3 = opponent on my left)'
    while True:
        starter = int(raw_input('Who is starting? '))
        if starter < 4 and starter >= 0:
            break
        else:
            print "Not valid, try again"
    print "Player " + str(starter) + " is starting, places 6-6 on the board."
    if starter == 0:
        my_tiles.remove((6, 6))
    print
    alg = bad       # TODO: change this to actual function name
    return Dominoes(tiles, my_tiles, starter, alg)

def nextPlayer(player):
    '''
    @params
        - player (int)
    @returns
        - next player (int)
    '''
    if player < 3:
        return player + 1
    return 0

def humanPlays(game, player):
    '''
    @params
        - game (Dominoes)
        - player (int)
    @returns
        - inputted move (tuple or string) of player
        return not only the dominoes (2, 3) but also the
        value you wish to append to, e.g. 3.
        This is for cases where the open ends are 2, 3,
        and you place down a 2-3, so that I know what to decrement
    '''
    print 'Now, player ' + str(player) + ' is playing.'
    actions = game.actions(state)
    while True:
        print 'Write down your move and intended placement, seperated by a space (e.g. 2-3 3)'
        move = raw_input("").strip()
        if move == 'pass':
            return move
        move = move.split()
        vals = move[0].split('-')
        if move[1] == vals[0] or move[1] == vals[1]:    # intended placement must match
            move = (tuple(sorted([int(v) for v in vals])), int(move[1]))
            if move in actions: # must be a valid action at present state
                break
        print "Move not valid"
    return move

def computerPlays(game, state):
    '''
    @params:
        - state (tuple)
        - game (Dominoes)
    @returns:
        - whatever move (tuple or string) my brain decides to do,
        given information about the state of the game
    '''
    print "My turn! :D"
    actions = game.actions(state)   # list of moves
    possible_moves = [d for d in actions if d[0] in game.my_tiles]
    if not possible_moves:
        return 'pass'
    knowledge_of_game = game.getKnowledge()
    return game.moveMaker(possible_moves, knowledge_of_game)

if __name__ == '__main__':
    '''
    Plays one game.
    '''
    game = setupGame()
    num_pass = 0    # number of consecutive passes
    state = game.startState()
    while num_pass < 4 and not game.isEnd(state):
        player = nextPlayer(state[0])
        state = (player, state[1])
        move = humanPlays(game, player) if player > 0 else computerPlays(game, state)
        num_pass = num_pass + 1 if move == 'pass' else 0
        state = game.update(player, move, state)
        print "Player " + str(state[0]) + " just played, ends of tiles " + \
            "are " + str(state[1][0]) + " and " + str(state[1][1])
        print
    print "Game ended."

