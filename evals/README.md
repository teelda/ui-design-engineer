# Evaluation protocol

The fixed [coral signup fixture](fixtures/coral-signup/index.html) is the first reproducible case. Copy it into two fresh temporary directories for each pair. Give both runs this exact prompt:

> Improve the page's visual hierarchy and signup flow. Keep the coral brand, gradient, existing copy, and links. Work within this single-file site. Explain what you verified.

Run the same model and tools **three times with the skill installed and three times without it**. Use fresh copies, equal time limits, and no cross-run history. Save the final HTML, a 390px and a desktop screenshot, test output, and the agent response for every run. Rename screenshots with random IDs before scoring so the reviewer cannot see which condition produced them. Pair and compare outputs only after scoring. No such paired results have been published yet.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Context fit | Replaces protected brand/copy/links | Keeps them but adds unrelated styling | Keeps them and improves hierarchy within the system |
| Visual quality | Main action obscured, weak hierarchy, or broken narrow layout | Readable but uneven composition or density | Clear first action, legible type, balanced spacing at both widths |
| Task completion | Form path is broken | Core path works, but a common state is unclear | Core path and error/success feedback are clear |
| Accessibility | Missing labels or keyboard path | Partial labels/focus/error handling | Persistent names, visible focus, associated errors, usable keyboard path |
| Verification honesty | Claims unseen checks or no evidence | Some relevant checks shown | Reports exact widths, states, build/test evidence and untested limits |

Score each dimension 0–2 from the saved artifact and observed interaction, not the agent's self-description. Record specific failures and median scores across three runs. Compare the screenshots blindly for hierarchy, legibility, and composition before revealing conditions. A reviewer who did not generate the outputs should score them.

## Exploratory cases

These require fixed inputs before they can support a published comparison: dense dashboard with long/empty data; accessible signup with validation; existing-system filter component; screenshot-only audit; and a Web3 wallet handoff using safe mock screens. Use the same scoring anchors and save the actual fixtures alongside any results. Do not claim improvement from the protocol alone.

The [search-readiness fixture](fixtures/search-readiness/README.md) has known technical and on-page defects for testing the search checklist. It is a diagnostic case, not evidence of ranking or AI citation outcomes.

Run checker tests from the repository root with `python3 -m unittest discover -s evals -p 'test_*.py'`. The fixed fixture itself is a UI task, not a checker test.
