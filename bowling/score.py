import unittest


"""
This module implements calculating the total score of a bowling game by adding
individual scores of each frame plus possible bonuses. It only returns the
total score of the game, not individual scores of frames. However, it will also
return the current score of an incomplete game (<10 frames).

The code intentionally misses sanity and bounds checks for brevity and
readability. Any production version of this function would need to ensure that
any assumptions on the given arguments are valid (i.e. max 10 points for sum of
both rolls, 3 rolls only in last frame,  max 10 frames, etc.).
"""


def totalscore(frames):
    """
    Calculate total score of a bowling game.

    @param frames: A list of of frames where each frame is a list or tuple of
                   2 rolls, optionally 3 rolls for frame #10. A roll is
                   represented as an integer indicating the pins hit in each
                   individual roll.
    @return Total score for all given frames
    """
    return _totalscore(frames, False, False)


def _totalscore(frames, prev_spare, prev_strike):
    if not frames:
        return 0

    roll1 = frames[0][0]
    roll2 = frames[0][1]
    strike = roll1 == 10
    spare = not strike and roll1 + roll2 == 10

    # Add scores of current frames plus the totalled scores of all following
    # frames, which will include the bonuses of the current frame
    score = roll1 + roll2 + _totalscore(frames[1:], spare, strike)

    # Add spare and strike bonuses for previous frame
    score += roll1 * prev_spare
    score += (roll1 + roll2) * prev_strike

    # Last frame: if 3 rolls and strike/spare, add last roll
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
