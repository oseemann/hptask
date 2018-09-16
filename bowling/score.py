import sys
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
    return _totalscore(frames, False, False, False)


def totalscore_fromstring(frames_str):
    """
    A helper that converts an entered string representation of the game scores
    into a list as required by the `totalscore()` function.

    String format: rolls separated by comma, frames separated by spaces,
                   e.g.: "0,10 1,9 2,8 3,7 4,6 5,5 6,4 7,3 8,2 9,1"
    """
    return totalscore(split_frames_string(frames_str))


def split_frames_string(frames_str):
    """
    Splits score string into list of tuples:
    "1,2 3,4" -> [(1, 2), (3, 4)]
    """
    return [
        tuple(int(points) if points else 0 for points in frame.split(','))
        for frame in frames_str.split(' ')
    ]


def _totalscore(frames, prev_spare, prev_strike, double_strike):
    """
    Calculate bowling score recursively.

    Each invocation looks only at the first frame in the list and calls the
    same function again with the remainder of the list.

    @param frames: A list of frames, see `totalscore` function
    @param prev_spare: Boolean indicating the previous frame was a spare
    @param prev_strike: Boolean indicating the previous frame was a strike
    @param double_strike: Boolean indicating the two previous frames where
                          strikes

    @return Cumulated score of all given frames
    """
    if not frames:
        # This is where the recursion ends
        return 0

    # Find out what's in the current frame
    frame = frames[0]
    roll1 = frame[0]
    roll2 = frame[1]
    strike = roll1 == 10
    spare = not strike and roll1 + roll2 == 10

    # Start the score with both rolls
    score = roll1 + roll2

    # Add spare and strike bonuses for previous frames
    # (In Python the following expressions are true:
    #  `3 * True == 3` and `3 * False == 0`)
    score += roll1 * prev_spare
    score += (roll1 + roll2) * prev_strike
    score += roll1 * double_strike

    # Last frame: if 3 rolls and strike/spare, add last roll
    score += frame[2] if (strike or spare) and len(frame) == 3 else 0

    # Add scores of all following frames, which will include the bonuses of
    # the current frame.
    score += _totalscore(frames[1:], spare, strike, strike and prev_strike)

    return score


class ScoreTest(unittest.TestCase):
    def t(self, score, frames):
        self.assertEqual(totalscore(frames), score)

    def test_example(self):
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

    def test_more(self):
        # Test case scores were calculated using https://bowlinggenius.com/
        self.t(300, [(10, 0)] * 9 + [(10, 10, 10)])  # max score
        self.t(245, [(10, 0)] * 9 + [(1, 1, 0)])
        self.t(180, [(9, 1)] * 9 + [(9, 0)])
        self.t(100, [(10, 0), (5, 0)] * 5)
        self.t(200, [(10, 0), (5, 5)] * 4 + [(10, 0), (5, 5, 10)])
        self.t(20, [(1, 1)] * 10)
        self.t(0, [(0, 0)] * 10)

    def test_split_frame_string(self):
        self.assertEqual([(1, 1)], split_frames_string("1,1"))
        self.assertEqual([(1, 1), (2, 2), (3, 3, 3)],
                         split_frames_string("1,1 2,2 3,3,3"))

    def test_with_strings(self):
        self.assertEqual(5, totalscore_fromstring("1,4"))
        self.assertEqual(145, totalscore_fromstring(
                              "0,10 1,9 2,8 3,7 4,6 5,5 6,4 7,3 8,2 9,1"))


def main(args):
    if len(args) > 0:
        for arg in args:
            score = totalscore_fromstring(arg)
            print("Score: {} for {}".format(score, arg))
    else:
        unittest.main()


if __name__ == '__main__':
    main(sys.argv[1:])
