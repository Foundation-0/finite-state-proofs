# Working on finite-state-proofs

Read README.md and PROOF.md before changing a result. Keep research changes in
pull requests and preserve concurrent work. Do not merge your own result.

- State the counting problem and its source independently of the implementation.
- Preserve pinned source facts and attribution. Do not call a formula or proof
  new merely because a limited search found no earlier proof.
- Prove the state-to-object correspondence and the all-indices implication.
  Matching initial terms alone is not a proof of a recurrence.
- Preserve exact arithmetic, exceptional starting indices, independent checks,
  and tests that reject corrupted certificates.
- Run both verifiers, the unittest suite, and `sha256sum -c SHA256SUMS`.
  Deliberate changes require regenerated certificates and reviewed hash updates.
- Disclose AI assistance and name the human sponsor. Human review remains
  distinct from independent AI review or successful software checks.
- Do not submit to OEIS or contact editors without the person's instruction;
  its policy restricts bulk or serial automated submissions.
- Do not invent licensing grants, citations, or proof-assistant verification.
