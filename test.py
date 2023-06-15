import os
import unittest
from edit_videos import get_cuts

class TestCases(unittest.TestCase):
    def test_video_edits(self):
        try:
            os.mkdir('test-videos')
        except:
            pass

        cuts = get_cuts('test-videos/test_video', intervals=15, start_grace=5, end_grace=5)
        self.assertEqual(cuts, [(0, 1), (2, 3), (4, 5)])

if __name__ == '__main__':
    unittest.main()