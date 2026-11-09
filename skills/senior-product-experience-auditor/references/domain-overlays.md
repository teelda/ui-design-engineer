# Conditional domain overlays

Use only applicable overlays, not every checklist on every product.

- **SaaS / enterprise:** first value, progressive setup, import, roles/invites/removal, tenant isolation, stale data, sorting/filtering/search, pagination, bulk actions, exports, timezone interpretation, audit logs and long-running jobs. Billing needs clear plan limits, trial expiry, cancellation and failed-payment recovery when present.
- **AI products / agents:** Read → Prepare → Execute boundaries, progress tied to actual work, uncertainty and evidence, cancellation, editing/rejecting output, human handoff, interrupted work, source freshness, hallucination recovery, and tool permissions. Evaluate the generated output as well as its presentation.
- **Fintech / Web3:** wallet/account/network identity; correct units and decimals; approval versus transfer; spender, recipient, asset, amount, fees and slippage before signing; unlimited permissions; rejected signatures; pending/replaced/dropped transactions; refresh persistence and explorer links. Use safe fixtures; never send funds or sign a transaction merely to audit.
- **Commerce / marketplaces:** variants, stock, total price, fees, delivery, returns, cart persistence, checkout recovery, seller identity, trust and dispute paths. Do not place real orders without authorization.
- **Healthcare:** sensitive-data exposure, roles, provenance, urgent-state handling, plain language, human review and error recovery. Do not diagnose, certify compliance or use real patient data for testing.
- **Mobile:** keyboard and safe-area overlap, orientation, touch targets, interruptions, navigation/back behavior, long text and poor connections. Separate a responsive browser test from a native-device test.

## Industry questions

| Domain | Ask only when relevant |
|---|---|
| Healthcare | Which role is acting (patient, clinician, staff)? Are units, uncertainty, urgent escalation, sensitive information and human review clear at the decision point? Use safe fixtures; verify any legal or clinical claim against current authoritative sources. |
| Finance | Are amounts, fees, settlement status, reversibility, reconciliation and authorization understandable? Distinguish an estimate from a posted result. |
| Education | Can learner and instructor each understand feedback, progress, assessment consequences, retries and recovery? |
| Commerce | Are variants, availability, total cost, delivery, returns and order recovery visible before commitment? |
| Enterprise operations | Are permissions, bulk actions, audit history, dense comparisons and destructive changes controllable and reviewable? |
| AI products | Can users inspect evidence, uncertainty, correction, cancellation, stale results and human approval boundaries? |

These are review lenses, not compliance certifications. Use current jurisdiction- and product-specific sources before asserting a legal, clinical or financial requirement.

## Web3 journey review

Start with the user's actual goal, experience with wallets, device and accessibility needs. A token purchase is often an intermediate task; follow through to membership, play, exchange or another intended outcome. Do not assume a crypto-native audience.

1. **Simple without losing power:** put the default path first; reveal advanced controls when needed. Evaluate whether the user can predict the result, not merely how few clicks it takes.
2. **Understandable language:** explain signatures, approvals, gas and network changes in the audience's terms. Never hide material risks behind friendly wording.
3. **Necessary safeguards:** provide contextual guidance for backup/recovery and applicable authentication. Do not require every wallet to support the same recovery method. Never request a seed phrase or private key.
4. **Useful conventions:** show asset units and appropriate fiat equivalents with quote freshness, network, recipient, amount, fees and slippage. Separate an estimate from a guaranteed outcome.
5. **End-to-end handoffs:** map product → wallet → onramp → swap/bridge/marketplace → product. Check return paths, preserved intent, cancellation, rejected signatures, insufficient funds, wrong network, pending/replaced/dropped transactions and refresh recovery using safe fixtures. Completion means the user's outcome, not simply a successful signature.
6. **Context at decision time:** explain what enters/leaves the wallet, spender permissions and approval vs transfer before signing. Keep technical details inspectable with progressive disclosure.

Assess support/community handoff, user feedback and upgrade/migration burdens when evidence is available. These are research questions when only screenshots are supplied. Record untested steps explicitly. This is a UX review, never a smart-contract security audit, custody assurance or investment recommendation.

## Web3 product branches

| Product | Additional decision points |
|---|---|
| Wallet | Connected account, permission scope, signing request meaning, recovery responsibility and account switching. |
| Swap or bridge | Quote freshness, minimum received, destination asset/network, delay, partial completion and return path. |
| Lending | Collateral, borrowing limit, changing position, liquidation conditions and exit options. |
| Staking | Lockup, withdrawal queue, reward assumptions and exit conditions. |
| Governance | Voting power, delegation, proposal effect and execution status. |
| Embedded wallet | What the user controls, who can recover access, and what recovery actually restores. |

Inspect only mechanics present in the product. Verify protocol-specific claims against the product's documentation and observed behavior; do not infer them from common Web3 patterns.
