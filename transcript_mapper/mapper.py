import os
import csv

class Mapper:

    def __init__(self, tx_path):
        """ Creates Mapper object and loads transcript definitions
        Args:
          tx_path (str): path to tab-separated transcript definition file
        Returns:
          None
        """
        self.txs = {}
        with open(tx_path, 'r') as tx_in:
            for r in csv.reader(tx_in, delimiter='\t'):
                self.txs[r[0]] = {
                    "chrom": r[1],
                    "start": int(r[2]),
                    "cig": r[3]
                }

    @staticmethod
    def parse_cig(cig):
        """ CIGAR string parser
          Parses input CIGAR string and generates operator/count pairs
        Args:
          cig (str): input CIGAR string
        Yields:
          op (char), count (int): operator and count for each operator in input
        """
        ops = ['M', 'D', 'I']
        int_str = ''
        for i in cig:
            if i not in ops:
                int_str += i
            else:
                op = i
                count = int(int_str)
                int_str = ''
                yield op, count

    def make_map(self, tx_name):
        """ Create transcript<>genomic positional maps
          Iterate through CIGAR string and create complementary, equal length tuples
          of (start, stop) coordinate pairs
        Args:
          tx_name (str): name of transcript as it exists in object's tx dict
        Returns:
          None - results saved to object's tx dict
        """
        tx = self.txs[tx_name]
        tx_idx = 0
        gen_idx = tx["start"]
        tx_map = []
        gen_map = []
        
        for op, count in self.parse_cig(tx["cig"]):
            if op == 'M':
                tx_pair = [tx_idx]
                gen_pair = [gen_idx]
                tx_idx += count
                gen_idx += count
                tx_pair.append(tx_idx - 1)
                gen_pair.append(gen_idx - 1)
                tx_map.append(tuple(tx_pair))
                gen_map.append(tuple(gen_pair))
            elif op == 'D':
                gen_idx += count
            elif op == 'I':
                tx_idx += count
        
        tx["gen_map"] = tuple(gen_map)
        tx["tx_map"] = tuple(tx_map)

    def to_genomic(self, tx_name, tx_pos):
        """ Translate transcript coordinate to genomic
          Checks if the maps are available for queried transcript and generates them if not.
          Iterates through the maps in a pairwise fashion and returns chrom and position if found.
        Args:
          tx_name (str): name of the transcript
          tx_pos (int): transcript position
        Returns:
          chrom (str), gen_pos (int): chromosome and complementary genomic position
        """
        tx = self.txs[tx_name]
        if tx.get("gen_map") is None:
            self.make_map(tx_name)

        for g, t in zip(tx["gen_map"], tx["tx_map"]):
            if t[0] <= tx_pos <= t[1]:
                gen_pos = g[0] + (tx_pos - t[0])
                return tx["chrom"], gen_pos

    def process_queries(self, in_path, out_path):
        in_ = open(in_path, 'r')
        out_ = open(out_path, 'a')
        for r in csv.reader(in_, delimiter='\t'):
            tx_name, tx_pos = r[0], int(r[1])

            try:
                chrom, gen_pos = self.to_genomic(tx_name, tx_pos)
            except TypeError:
                print(f'No match found for {tx_name} at {tx_pos}, insertion perhaps? Continuing..')
                continue

            out_.write(f'{tx_name}\t{tx_pos}\t{chrom}\t{gen_pos}\n')

        in_.close()
        out_.close()
