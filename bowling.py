import unittest


def totalscore(frames, prev_spare=False, prev_strike=False):
    if not frames:
        return 0

    roll1 = frames[0][0]
    roll2 = frames[0][1]
    strike = roll1 == 10
    spare = not strike and roll1 + roll2 == 10

    # add scores of current frames plus the totalled scores of all following
    # frames, which will include the bonuses of the current frame
    score = roll1 + roll2 + totalscore(frames[1:], spare, strike)

    # add spare and strike bonuses for previous frame
    score += roll1 * prev_spare
    score += (roll1 + roll2) * prev_strike

    # last frame: if 3 rolls and strike/spare, add last roll
    score += frames[0][2] if (strike or spare) and len(frames[0]) == 3 else 0

    return score


class ScoreTest(unittest.TestCase):
    def t(self, score, frames):
        self.assertEqual(totalscore(frames), score)

    def test_all(self):
        self.t(0, [])
        self.t(5, [(1, 4)])
        self.t(14, [(1, 4), (4, 5)])
        self.t(24, [(1, 4), (4, 5), (6, 4)])
        self.t(39, [(1, 4), (4, 5), (6, 4), (5, 5)])
        self.t(59, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0)])
        self.t(61, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0), (0, 1)])
        self.t(71, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0), (0, 1), (7, 3)])
        self.t(87, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0), (0, 1), (7, 3),
               (6, 4)])
        self.t(107, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0), (0, 1), (7, 3),
               (6, 4), (10, 0)])
        self.t(125, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0), (0, 1), (7, 3),
               (6, 4), (10, 0), (2, 7)])
        self.t(133, [(1, 4), (4, 5), (6, 4), (5, 5), (10, 0), (0, 1), (7, 3),
               (6, 4), (10, 0), (2, 8, 6)])


if __name__ == '__main__':
    unittest.main()
