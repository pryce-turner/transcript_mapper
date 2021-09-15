import sys
import csv
import click
import logging
from transcript_mapper.mapper import Mapper

logging.basicConfig(level=logging.INFO)

@click.command()
@click.option('--input-transcripts', '-t', required=True, help="File path from which to load transcript definitions")
@click.option('--input-queries', '-q', required=True, help="File path for position translation queries")
@click.option('--output-path', '-o', help="File path for translation output")
def process_queries(input_transcripts, input_queries, output_path):
    
    try:
        mapper = Mapper(input_transcripts)
        qs = open(input_queries, 'r')
        out = open(output_path, 'a')
    except FileNotFoundError:
        logging.error('Input/query file not found or unsuitable output path, exiting..', exc_info=True)
        sys.exit()

    for r in csv.reader(qs, delimiter='\t'):
        tx_name, tx_pos = r[0], int(r[1])

        try:
            chrom, gen_pos = mapper.to_genomic(tx_name, tx_pos)
        except TypeError:
            logging.warn(f'No match found for {tx_name} at {tx_pos}, insertion perhaps? Continuing..')
            continue

        out.write(f'{tx_name}\t{tx_pos}\t{chrom}\t{gen_pos}\n')

    qs.close()
    out.close()
    logging.info(f'Successfully processed transcripts in {input_queries}, exiting..')

if __name__ == "__main__":
    process_queries()