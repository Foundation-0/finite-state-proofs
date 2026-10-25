"""Ensure the independently reconstructed proof rejects changed claims."""

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify_independent


class IndependentProofTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((ROOT / 'sources.json').read_text())
        cls.certificate = json.loads((ROOT / 'certificate.json').read_text())

    def test_all_claims_and_exhaustive_controls(self):
        self.assertEqual(verify_independent.verify(self.sources, self.certificate), (11, 19))

    def test_omitted_width_is_rejected(self):
        source = copy.deepcopy(self.sources)
        source['families'].pop()
        with self.assertRaisesRegex(ValueError, 'all six widths'):
            verify_independent.verify(source, self.certificate)

    def test_changed_transient_output_is_rejected(self):
        certificate = copy.deepcopy(self.certificate)
        certificate['families'][0]['claims'][0]['residual_outputs'][0] = 1
        with self.assertRaisesRegex(ValueError, 'stored claim differs'):
            verify_independent.verify(self.sources, certificate)


if __name__ == '__main__':
    unittest.main()
