from transcript_mapper.cmd_map import process_queries
from click.testing import CliRunner

tx_in_path = 'tests/input/transcripts.tsv'
qs_in_path = 'tests/input/queries.tsv'
out_path = 'tests/output/actual.tsv'

def test_process_queries():
    runner = CliRunner()
    result = runner.invoke(
        process_queries, 
        ['-t',
        tx_in_path,
        '-q',
        qs_in_path,
        '-o',
        out_path]
        )
    assert result.exit_code == 0