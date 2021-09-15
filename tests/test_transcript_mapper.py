import os
import unittest
from filecmp import cmp
from transcript_mapper.mapper import Mapper

tx_in_path = 'tests/input/transcripts.tsv'
qs_in_path = 'tests/input/queries.tsv'
out_path = 'tests/output/actual.tsv'

class TestMapper(unittest.TestCase):

    def setUp(self):
        self.mapper = Mapper(tx_in_path)

    def test_to_genomic(self):
        chrom, pos = self.mapper.to_genomic('TR1', 4)
        self.assertEqual(chrom, 'CHR1')
        self.assertEqual(pos, 7)

    def test_make_map(self):
        tx = "TR1"
        self.mapper.make_map(tx)
        exp_gen = ((3, 10), (18, 23), (24, 25), (37, 43))
        exp_tx = ((0, 7),(8, 13), (16, 17), (18, 24))
        self.assertEqual(exp_tx, self.mapper.txs[tx]["tx_map"])
        self.assertEqual(exp_gen, self.mapper.txs[tx]["gen_map"])

    def tearDown(self):
        try:
            os.remove(out_path)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()