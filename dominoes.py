
# pass current state and what the board looks like to baseline/better.
# who has played what that we currently see in the board, and what are my possible moves
# once someone has probability zero of having a
# domino, they continue having that probability zero

class Dominoes(object):
	def __init__(self, game_tiles, my_tiles, starter):
		'''
		@params:
			- game_tiles (list of tuples of ints): each tuple has two
			values representing a domino in the game. This list contains
			all dominoes in the game.
			- my_tiles (list of tuples of ints): the dominoes that I have.
			- starter (int): 0 = me, 1 = first opp, 2 = partner, 3 = third opp.
			In the game, I sit opposite my partner and we play counter-clockwise,
			hence this numbering of players.
		'''
		self.tiles = game_tiles
		self.my_tiles = my_tiles
		self.tiles_by_opp1 = []
		self.tiles_by_opp2 = []
		self.tiles_by_partner = []
		self.tiles_by_me = []
		self.start = starter

	def startState(self):
		# (who is playing, open ends)
		return (self.starter, (6, 6))

	def isEnd(self, state):
		'''
		The game ends when everyone passes once
		Also when one person has no dominoes left?
		'''
		pass

	def actions(self, state):
		pass

	def states(self):
		pass


# Controller

def setupGame():
	print 'Welcome.'
	tiles = []
	for i in range(7):
		for j in range(i, 7):
			tiles.append((i, j))
	my_tiles_input = raw_input('Enter my tiles (e.g. 4-5) seperated by spaces: ').split()
	assert (len(my_tiles_input) == 7), "I need 7 tiles!"
	my_tiles = []
	for t in my_tiles_input:
		my_tiles.append(tuple([int(num) for num in t.split('-')]))
	print '(0 = me, 1 = opponent on my right, 2 = partner across from me, 3 = opponent on my left)'
	starter = int(raw_input('Who is starting? '))
	assert (starter < 4 and starter >= 0)
	return Dominoes(tiles, my_tiles, starter)

if __name__ == '__main__':
	game = setupGame()
	


