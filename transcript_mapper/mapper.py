import os
import csv
from collections import namedtuple

class Mapper:

    def __init__(self, tx_path):
        self.tx = {}
        with open(tx_path, 'r') as tx_in:
            for r in csv.reader(tx_in, delimiter='\t'):
                self.tx[r[0]] = {
                    "chrom": r[1],
                    "start": int(r[2]),
                    "cig": r[3]
                }
        # print(self.tx)
    
    def make_map(self, tx_name):
        to_map = self.tx[tx_name]
        tx_coord = 0
        gen_coord = to_map["start"]
        tx_map = []
        gen_map = []
        
        ops = ['M', 'D', 'I']
        int_str = ''
        for i in to_map["cig"]:
            if i not in ops:
                int_str += i
            else:
                op = i
                count = int(int_str)
                int_str = ''
                # print(f'{count} - {op}')

                if op == 'M':
                    tx_pair = [tx_coord,0]
                    gen_pair = [gen_coord,0]
                    tx_pair[1] = tx_coord + count - 1
                    gen_pair[1] = gen_coord + count - 1
                    tx_map.append(tx_pair)
                    gen_map.append(gen_pair)
                    continue
                elif op == 'D':
                    gen_coord += count
                    continue
                elif op == 'I':
                    tx_coord += count
                    continue
        
        return gen_map, tx_map



    def map(self, qs):
        ...