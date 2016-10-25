'''
Not finished/commented

a.k.a messy af
'''

class Dominoes(object):
	def __init__(self, game_tiles, my_tiles, starter, alg):
		'''
		@params:
			- game_tiles (list of tuples of ints): each tuple has two
			values representing a domino in the game. This list contains
			all dominoes in the game.
			- my_tiles (list of tuples of ints): the dominoes that I have.
			- starter (int): 0 = me, 1 = first opp, 2 = partner, 3 = third opp.
			In the game, I sit opposite my partner and we play counter-clockwise,
			hence this numbering of players.
			- alg (function): greedy or optimal
		'''
		self.tiles = game_tiles
		self.my_tiles = my_tiles
		self.starter = starter
		self.moveMaker = alg

		# TODO: Change these to lists of lists
		self.tiles_opp1 = []	# none of us have played any tiles yet
		self.tiles_opp2 = []
		self.tiles_partner = []
		self.tiles_me = []
		# everyone has equal chance of having a domino that I don't have
		self.passes = [None, None, None, None]

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
			-
		@returns
			-
		'''
		options = state[1]
		res = set()
		vals = set(options)
		for v in vals:
			for t in game.tiles:
				if t[0] == v or t[1] == v:
					res.add(t)
		return res

	def isEnd(self, state):
		'''
		@params
			-
		@returns
			-
		'''
		player = state[0]
		if player == 0:
			return len(self.tiles_me) == 7
		if player == 1:
			return len(self.tiles_opp1) == 7
		if player == 2:
			return len(self.my_tiles) == 7
		if player == 3:
			return len(self.my_tiles) == 7

	def update(self, player, move, state):
		'''
		@params
			- move: valid move
		@returns
			-
		'''
		# TODO check if move == 'pass'
		placed_domino = move[0]
		placement = move[1]
		if placed_domino[0] == placement:
			new_end = placed_domino[1]
		else:
			new_end = placed_domino[0]
		options = list(state[1])
		assert (player == state[0])
		if options[0] == placement:
			options[0] = new_end
		else:
			options[1] = new_end
		state = (player, options)
		# TODO: update lists of lists of played things
		return state

	def getKnowledge(self):
		'''
		@return:
			- a dictionary.
		'''
		return {'opp1 tiles':self.tiles_opp1, 'opp2 tiles':self.tiles_opp2,
			'partner tiles':self.tiles_partner, 'me tiles':self.tiles_me,
			'my tiles':self.my_tiles,
			'passes':self.passes}

def bad():
	# DELETE!
	return 'pass'

# Controller
def setupGame():
	'''
	@params
		-
	@returns
		-
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
	print 'Players are numbered as the following:'
	print '(0 = me, 1 = opponent on my right, 2 = partner across from me, 3 = opponent on my left)'
	while True:
		starter = int(raw_input('Who is starting? '))
		if starter < 4 and starter >= 0:
			break
		else:
			print "Not valid, try again"
	alg = bad		# TODO: change this to actual function name
	return Dominoes(tiles, my_tiles, starter, alg)

def nextPlayer(player):
	'''
	@params
		-
	@returns
		-
	'''
	if player < 3:
		return player + 1
	return 0

def humanPlays(game, player):
	'''
	@params
		-
	@returns
		-
	'''
	print 'Player %d is playing', player
	actions = game.actions(state)
	while True:
		print 'Write down your move and intended placement, seperated by a space'
		move = raw_input("e.g. 2-3 3")
		move = move.split()
		vals = move[0].split('-')
		if move[1] == vals[0] or move[1] == vals[1]:	# intended placement must match
			move = (tuple(sorted([int(v) for v in vals])), int(move[1]))
			if move[0] in actions:	# must be a valid action at present state
				break
		print "Move not valid"
	return move

def computerPlays(game, state):
	'''
	@params:
		- state (tuple)
	NOTE:
	It would be great to return not only the dominoes (2, 3) but also the
	value you wish to append to, e.g. 3.
	This is for cases where the open ends are 2, 3, and you place down a 2-3,
	so that I know what to decrement
	'''
	actions = game.actions(state)
	possible_moves = [d for d in actions if d in game.my_tiles]
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
		move = humanPlays(game, player) if player > 0 else computerPlays(game, state)
		num_pass = num_pass + 1 if move == 'pass' else 0
		state = game.update(player, move, state)
		print "Player %d just played, ends of tiles " + \
			"are %d and %d", state[0], state[1][0], state[1][1]
	print "Game ended."

