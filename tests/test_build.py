import unittest
from level.build import Paths_Build

class TestPaths_Build(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Paths_Build.add(5, 2), 7)



if __name__ ==  '__main__':
    unittest.main()


   