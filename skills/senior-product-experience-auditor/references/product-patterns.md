# Product-pattern checks

Choose only patterns present in the product. Follow state through the full workflow, not just the first screen.

| Pattern | Critical transitions and recovery |
|---|---|
| Transaction or checkout | Quote/total, authorization, confirmation, pending state, duplicate action, failure, reversal/refund and receipt. Verify amounts and who bears fees. |
| Dashboard or operations tool | Data freshness, dense comparison, filters, sorting, empty/partial results, permissions, bulk action preview, undo and audit history. |
| Editor or creator | Unsaved changes, autosave, version history, concurrent edits, conflict resolution, export and return after interruption. |
| Marketplace | Search/filter, item availability, variants, seller identity, total cost, delivery, cancellation, dispute and order recovery. |
| AI assistant or agent | Input intent, source provenance, uncertain output, correction, approval before external action, progress truthfulness, cancellation and stale results. |
| Background job | Start, progress, timeout, leaving/returning, notification, partial success, retry and duplicate prevention. |

For each transition, record expected state, observed state, evidence source, and untested conditions. Avoid assigning a failure merely because a product does not implement an irrelevant pattern.
