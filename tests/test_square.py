"""Run the square-law verifier on a sample, run its corruption test, also under `python -O`, and check the tables.

The square-law verifier needs NumPy. Without it the tests that run it are skipped, and the table test still runs.
"""

import csv
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

try:
    import numpy  # noqa: F401
except ImportError:  # pragma: no cover
    numpy = None

ROOT = Path(__file__).resolve().parents[1]
SQUARE = ROOT / 'square'
SAMPLE = ['A268622', 'A268888', 'A268906', 'A269763', 'A269279', 'A268635']
# A268888 is a square times (x + 1); A268906 and A269279 need a nonzero power s of x.


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, check=False)


@unittest.skipIf(numpy is None, 'NumPy is not installed')
class SquareVerifierTests(unittest.TestCase):
    def test_sample_passes_normally_and_under_optimize(self):
        paths = [SQUARE / 'proofs' / (name + '.json') for name in SAMPLE]
        for flags in ([], ['-O'], ['-I', '-O']):
            with self.subTest(flags=flags):
                result = run(*flags, SQUARE / 'verify.py', *paths)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(result.stdout.count('PASS'), len(SAMPLE))

    def test_corruption_script_rejects_everything(self):
        for flags in ([], ['-O']):
            with self.subTest(flags=flags):
                result = run(*flags, SQUARE / 'test_corrupt.py')
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('corrupted inputs rejected: 73 / 73', result.stdout)

    def test_changed_start_is_rejected_from_the_command_line(self):
        certificate = json.loads((SQUARE / 'proofs' / 'A268635.json').read_text())
        certificate['start'] += 1
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / 'changed.json'
            path.write_text(json.dumps(certificate))
            for flags in ([], ['-O']):
                with self.subTest(flags=flags):
                    result = run(*flags, SQUARE / 'verify.py', path)
                    self.assertEqual(result.returncode, 1)
                    self.assertIn('REJECT', result.stdout)


class SquareTableTests(unittest.TestCase):
    def test_table_matches_the_certificates(self):
        with open(SQUARE / 'table.csv', newline='', encoding='utf-8') as handle:
            rows = list(csv.DictReader(handle))
        files = sorted(p.stem for p in (SQUARE / 'proofs').glob('A*.json'))
        self.assertEqual(len(files), 238)
        self.assertEqual(sorted(r['entry'] for r in rows), files)
        self.assertEqual({r['group'] for r in rows}, {'first211', 'skipped27'})
        self.assertEqual(sum(r['group'] == 'first211' for r in rows), 211)
        self.assertEqual(sum(r['group'] == 'skipped27' for r in rows), 27)
        self.assertTrue(all(r['status'] == 'proved' and r['agrees'] == 'True' for r in rows))
        for r in rows:
            certificate = json.loads((SQUARE / 'proofs' / (r['entry'] + '.json')).read_text())
            self.assertEqual(certificate['start'], int(r['start']))
            self.assertEqual(certificate['theorem_index'], int(r['index_N']))


if __name__ == '__main__':
    unittest.main()
