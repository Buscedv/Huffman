import main
import unittest

class MainTest(unittest.TestCase):
    def test_add(self):
        huffman_tree = {'pa': {0: 'p', 1: 'a'}, 'm_': {0: 'm', 1: '_'}, 'es': {0: 'e', 1: 's'}, 'tpa': {0: 't', 1: 'pa'}, 'm_es': {0: 'm_', 1: 'es'}, 'tpam_es': {0: 'tpa', 1: 'm_es'}}
        self.assertEqual(main.decompress(huffman_tree,"111010011100"), "spam")

if __name__ == '__main__':
    unittest.main()
