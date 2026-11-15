"""Run the first-pass verifier on a sample of the 211 certificates, its corruption test, and the zero-vector check."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIRST = ROOT / 'oeis211'
SAMPLE = ['A268881', 'A268887', 'A268636', 'A268763', 'A269007', 'A268623']
# A268636 and A268763 are two of the eight whose residual chain never reaches the zero vector.
sys.path.insert(0, str(FIRST))
import check_zero_vector  # noqa: E402


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True, check=False)


class FirstPassTests(unittest.TestCase):
    def test_sample_passes_normally_and_under_optimize(self):
        with tempfile.TemporaryDirectory() as temporary:
            for name in SAMPLE:
                shutil.copy(FIRST / 'certs' / (name + '.json'), temporary)
            for flags in ([], ['-O'], ['-I', '-O']):
                with self.subTest(flags=flags):
                    result = run(*flags, FIRST / 'verify_all.py', temporary)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn('%d certificates, 0 failed' % len(SAMPLE), result.stdout)

    def test_corruption_script_rejects_everything(self):
        for flags in ([], ['-O']):
            with self.subTest(flags=flags):
                result = run(*flags, FIRST / 'test_corrupt.py')
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn('rejected 105 of 105', result.stdout)

    def test_zero_vector_test_is_sufficient_but_not_necessary(self):
        for name, expected in (('A268881', True), ('A268763', False), ('A268778', False)):
            with self.subTest(entry=name):
                certificate = json.loads((FIRST / 'certs' / (name + '.json')).read_text())
                reached, _ = check_zero_vector.reaches_zero(certificate)
                self.assertEqual(reached, expected)
                kind = 'vector_chain' if expected else 'scalar_window'
                self.assertEqual(certificate['proof']['kind'], kind)

    def test_list_of_eight_in_the_certificates(self):
        kinds = {}
        for path in sorted((FIRST / 'certs').glob('A*.json')):
            certificate = json.loads(path.read_text())
            kinds[certificate['oeis_id']] = certificate['proof']['kind']
        self.assertEqual(len(kinds), 211)
        self.assertEqual(sorted(k for k, v in kinds.items() if v == 'scalar_window'), check_zero_vector.EXPECTED)


if __name__ == '__main__':
    unittest.main()
