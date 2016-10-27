'''
Initial implementation of the dominoes game.

There are likely better ways of organizing/passing/storing
information about the current state of the game and memory of
the game. (should/will edit for p-progress/p-final)

In general, the following indices/ints correspond to the following
players: 0 = me, 1 = first opp, 2 = partner, 3 = third opp.
In the game, I sit opposite my partner and we play counter-clockwise,
hence this numbering of players.
'''

class Dominoes(object):
	def __init__(self, game_tiles, my_tiles, starter, alg):
		'''
		@params:
			- game_tiles (list of tuples of ints): each tuple has two
			values representing a domino in the game. This list contains
			all dominoes in the game. The first value is less or equal
			to the second value in the domino tuple.
			- my_tiles (list of tuples of ints): the seven dominoes
			that I begin with in the game.
			- starter (int): Who is starting the game?
			0 = me, 1 = first opp, 2 = partner, 3 = third opp.
			- alg (function): the algorithm I am using to beat humans.
		'''
		self.tiles = game_tiles
		self.my_tiles = my_tiles
		self.starter = starter
		self.moveMaker = alg

		# my tiles, tiles of opp1, tiles of partner, tiles of opp2
		self.placed_tiles = [[], [], [], []]
		# passes: me, opp1, partner, opp2
		self.passes = [set(), set(), set(), set()]

	def getKnowledge(self):
		'''
		@returns:
			- a tuple consisting of:
			placed_tiles (list of lists) and passes (list of sets)
			What tiles have been placed by whom on the table? What values
			do people not have?
		'''
		return (self.placed_tiles, self.passes)

	def startState(self):
		'''
		@return
			- a state (tuple): who is playing (int) and the open
			ends of dominoes (tuple of ints)
		'''
		return (self.starter, (6, 6))

	def actions(self, state):
		'''
		@params
			- state tuple
		@returns
			- returns possible moves (set of tuples, (domino, placement))
			that could be placed given the open ends of dominoes on the table.
		'''
		options = state[1]
		res = set()
		vals = set(options)
		for v in vals:
			for t in game.tiles:
				if t[0] == v or t[1] == v:
					res.add((t, v))
		return res

	def isEnd(self, state):
		'''
		@params
			- state tuple
		@returns
			- Has the previous player run out of dominoes? (bool)
		'''
		player = state[0]
		return len(self.placed_tiles[player]) == 7

	def update(self, player, move, state):
		'''
		@params
			- move (tuple): valid move e.g. ((2, 3), 3) or 'pass'
			In example, (2, 3) is a domino and 3 is the end you
			wish to attach to the dominoes on the table.
			- player (int)
			- state (tuple)
		@returns
			- state, with open ends of dominoes on table modified
			as necessary
		'''
		options = list(state[1])
		if move == 'pass':
			self.passes[player] |= set(options)
			return state
		# else
		placed_domino = move[0]
		placement = move[1]
		if placed_domino[0] == placement:
			new_end = placed_domino[1]
		else:
			new_end = placed_domino[0]
		assert (player == state[0])
		if options[0] == placement:
			options[0] = new_end
		else:
			options[1] = new_end
		state = (player, options)
		self.placed_tiles[player].append(placed_domino)
		if player == 0:	# I just played, must update myself
			self.my_tiles.remove(placed_domino)
		return state

def bad(possible_moves, knowledge_of_game):
	'''
	@params:
		- possible_moves: dominoes that I can place
		Not empty
		- knowledge_of_game: ignore, who cares
	TODO: flip if you can place on either side
	'''
	# Greedy algorithm
	assert (possible_moves)	# list of moves
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
	alg = bad		# TODO: change this to actual function name
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
		if move[1] == vals[0] or move[1] == vals[1]:	# intended placement must match
			move = (tuple(sorted([int(v) for v in vals])), int(move[1]))
			if move in actions:	# must be a valid action at present state
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
	actions = game.actions(state)	# list of moves
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
	num_pass = 0	# number of consecutive passes
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

