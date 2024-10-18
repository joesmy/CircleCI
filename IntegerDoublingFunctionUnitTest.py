# Integer Doubling Function Unit Test

import unittest

class TestNum(unittest.TestCase):

    def testDouble(self):
        result = twiceNumber(17)
        self.assertEqual(result,34)

    def testFloat(self):
        result = twiceNumber(5.5)
        self.assertFalse(result,)

if __name__ == '__main__':
    unittest.main()
        





