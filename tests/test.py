import unittest
from edit_videos import get_cuts

class TestCases(unittest.TestCase):
    def test_video_edits(self):
        cuts = get_cuts('test_video')
        self.assertEqual(cuts, [(0, 1), (2, 3), (4, 5)])

if __name__ == '__main__':
    unittest.main()