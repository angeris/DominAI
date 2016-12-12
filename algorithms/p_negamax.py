from copy import deepcopy

class ZeroSumBayesGame:
    def __init__(self):
        pass
    def is_end(self):
        raise NotImplemented()
    def make_probabilistic_move(self, player, move):
        raise NotImplemented()
    def undo_move(self, player, move):
        raise NotImplemented()
    def possible_actions(self, player):
        raise NotImplemented()
    def evaluate(self, player):
        raise NotImplemented()
    def get_next_player(self, player):
        raise NotImplemented()

# Simple probabilistic idea thingie
class ProbabilisticNegaMax:
    def __init__(self, curr_game, MAX_DEPTH = 10):
        self.curr_game = curr_game
        assert isinstance(curr_game, ZeroSumBayesGame)

    def p_negamax_ab(self, initial, depth, alpha, beta, player):
        cg = self.curr_game
        if depth==0 or cg.is_end():
            if cg.is_end():
                q = cg.win_score(player)
                if not q:
                    return None, cg.evaluate(player)
                return None, q
            return None, cg.evaluate(player)

        max_move, max_score = None, None
        for move in sorted(cg.possible_actions(player), key=lambda x:-sum(x[0].vals)):
            prob = cg.make_probabilistic_move(player, move)
            assert prob > 0
            curr_move, curr_score = self.p_negamax_ab(initial, depth-1, -beta, -alpha, cg.get_next_player(player))
            curr_score = -prob*curr_score
            # if depth == initial:
                # print "Player", player, "Move", move, "how good it is:", curr_score

            if max_score is None or curr_score > max_score:
                max_move, max_score = move, curr_score
            alpha = max(alpha, curr_score)
            cg.undo_move(player, move)
            if alpha >= beta:
                break
        return max_move, max_score

    def p_negamax(self, depth, player):
        # TODO: alpha-beta pruning
        cg = self.curr_game
        if depth==0 or cg.is_end():
            return None, cg.evaluate(player)

        max_move, max_score = None, None
        for move in cg.possible_actions(player):
            #cop = deepcopy(cg)
            prob = cg.make_probabilistic_move(player, move)

            curr_move, curr_score = self.p_negamax(depth-1, cg.get_next_player(player))
            curr_score = -prob*curr_score

            if max_score is None or curr_score > max_score:
                max_move, max_score = move, curr_score
            cg.undo_move(player, move)
            #cop.is_equal(cg)
        return max_move, max_score
