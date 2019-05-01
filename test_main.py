import main
import unittest

class MainTest(unittest.TestCase):
    def test_decompress(self):
        huffman_tree = {'pa': {0: 'p', 1: 'a'}, 'm_': {0: 'm', 1: '_'}, 'es': {0: 'e', 1: 's'}, 'tpa': {0: 't', 1: 'pa'}, 'm_es': {0: 'm_', 1: 'es'}, 'tpam_es': {0: 'tpa', 1: 'm_es'}}
        self.assertEqual(main.decompress(huffman_tree,"111010011100"), "spam")
    def test_text_to_bits(self):
        self.assertEqual(main.text_to_bits("a"), "01100001")
    def test_sort_dict(self):
        self.assertEqual(main.sort_dict({"c": 3,"b" : 2,"a" : 1}), dict([('a', 1), ('b', 2), ('c', 3)]))
    def test_compress(self):
        self.assertEqual(main.compress("test"),81.25)

if __name__ == '__main__':
    unittest.main()
