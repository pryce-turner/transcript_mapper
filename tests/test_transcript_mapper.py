import os
import unittest
from filecmp import cmp

import sys
BASE = '/home/pryce/Desktop/transcript_mapper/'
sys.path.insert(0, BASE)

from transcript_mapper.mapper import Mapper

class TestMapper(unittest.TestCase):

    def setUp(self):
        self.out_path = os.path.join(BASE, 'tests/output/actual.tsv')
        self.mapper = Mapper(os.path.join(BASE, 'tests/input/transcripts.tsv'))

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

    def test_overall(self):
        
        self.mapper.process_queries(os.path.join(BASE, 'tests/input/queries.tsv'), self.out_path)
        self.assertTrue(cmp(os.path.join(BASE, 'tests/output/expected.tsv'), self.out_path))

    def tearDown(self):
        try:
            os.remove(self.out_path)
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()