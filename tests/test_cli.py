from filecmp import cmp
import os
from transcript_mapper.cmd_map import process_queries
from click.testing import CliRunner

tx_in_path = 'tests/input/transcripts.tsv'
qs_in_path = 'tests/input/queries.tsv'
actual_out_path = 'tests/output/actual.tsv'
expected_out_path = 'tests/output/expected.tsv'

def test_process_queries():
    runner = CliRunner()
    result = runner.invoke(
        process_queries, 
        ['-t',
        tx_in_path,
        '-q',
        qs_in_path,
        '-o',
        actual_out_path]
        )
    assert result.exit_code == 0
    assert cmp(actual_out_path, expected_out_path)
    os.remove(actual_out_path)