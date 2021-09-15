import unittest
from filecmp import cmp
import sys
sys.path.insert(0,'/home/pryce/Desktop/transcript_mapper/')
from transcript_mapper.mapper import Mapper

class TestMapper(unittest.TestCase):

    def setUp(self):
        self.mapper = Mapper('/home/pryce/Desktop/transcript_mapper/tests/input/transcripts.tsv')

    # def test_mapper(self):
    #     ...

    # def test_overall(self):
    #     self.mapper.map()
    #     self.assertTrue(cmp('output/expected.tsv', 'output/actual.tsv'))

    def test_make_map(self):
        cig = "8M7D6M2I2M11D7M"
        tx = "TR1"
        actual_gen, actual_tx = self.mapper.make_map(tx)
        exp_gen = [[3, 10], [18, 23], [24, 25], [36, 42]]
        exp_tx = [[0, 7],[8, 13], [16, 17], [18, 24]]
        self.assertEqual(exp_gen, actual_gen)

if __name__ == '__main__':
    unittest.main()