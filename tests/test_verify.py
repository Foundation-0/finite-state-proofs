"""Independent counting controls and must-fail certificate probes."""

import copy
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify


def direct_counts(height, width):
    """Exhaust every board and count cell pairs; no row-mask/transfer logic."""
    exactly_one = at_most_one = 0
    for bits in itertools.product((0, 1), repeat=height * width):
        board = [bits[r * width:(r + 1) * width] for r in range(height)]
        pairs = 0
        for r in range(height):
            for c in range(width - 1):
                pairs += board[r][c] == board[r][c + 1] == 1
                if r + 1 < height:
                    pairs += board[r][c + 1] == board[r + 1][c] == 1
        exactly_one += pairs == 1
        at_most_one += pairs <= 1
    return exactly_one, at_most_one


class ExactProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((ROOT / 'sources.json').read_text())

    def test_transfer_matches_independent_exhaustion(self):
        for width in range(2, 8):
            states, edges, vector = verify.build_model(width)
            for height in range(1, min(4, 16 // width) + 1):
                with self.subTest(width=width, height=height):
                    observed = (verify.output(vector, states, 'exactly_one'),
                                verify.output(vector, states, 'at_most_one'))
                    self.assertEqual(observed, direct_counts(height, width))
                vector = verify.advance(vector, edges)

    def test_every_published_recurrence_has_zero_vector_certificate(self):
        certificate = verify.compute_certificate(self.sources)
        self.assertEqual(sum(len(f['claims']) for f in certificate['families']), 11)
        self.assertEqual([len(f['residual_vectors']) - 1 for f in certificate['families']],
                         [0, 1, 2, 2, 3, 3])
        for family in certificate['families']:
            self.assertFalse(any(family['residual_vectors'][-1]))
        self.assertEqual(verify.encode(certificate), (ROOT / 'certificate.json').read_bytes())

    def test_changed_coefficient_is_rejected(self):
        for i in range(len(self.sources['families'])):
            with self.subTest(family=i):
                corrupt = copy.deepcopy(self.sources)
                corrupt['families'][i]['recurrence_coefficients'][0] += 1
                with self.assertRaisesRegex(ValueError, 'does not reach zero'):
                    verify.compute_certificate(corrupt)

    def test_premature_start_is_rejected(self):
        for i in range(2, len(self.sources['families'])):
            with self.subTest(family=i):
                corrupt = copy.deepcopy(self.sources)
                corrupt['families'][i]['claims'][0]['recurrence_starts_at'] -= 1
                with self.assertRaisesRegex(ValueError, 'fails at its claimed start'):
                    verify.compute_certificate(corrupt)

    def test_changed_initial_count_is_rejected(self):
        corrupt = copy.deepcopy(self.sources)
        corrupt['families'][0]['claims'][0]['initial_terms'][0] += 1
        with self.assertRaisesRegex(ValueError, 'initial terms do not match'):
            verify.compute_certificate(corrupt)

    def test_cli_rejects_certificate_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            for name in ('verify.py', 'sources.json', 'certificate.json'):
                (folder / name).write_bytes((ROOT / name).read_bytes())
            certificate = json.loads((folder / 'certificate.json').read_text())
            certificate['families'][0]['initial_vector'][0] += 1
            (folder / 'certificate.json').write_bytes(verify.encode(certificate))
            result = subprocess.run([sys.executable, str(folder / 'verify.py')],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn('differs from exact regeneration', result.stderr)


if __name__ == '__main__':
    unittest.main()
