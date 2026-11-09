# Web3 UI checks

Use only for a relevant wallet or decentralized-product audit. Establish the user's wallet experience and the real outcome before judging complexity.

| Moment | Check |
|---|---|
| Entry | Plain-language purpose, a clear default path, and advanced details on demand. |
| Wallet connection | Network, account, permission scope, rejected connection, and return to task. |
| Transaction preview | Asset units and fiat estimate when reliable, recipient/spender, assets entering and leaving, fees, slippage, and approval versus transfer. |
| Confirmation and recovery | Pending, replaced, dropped, failed, wrong-network, insufficient-funds, refresh, and return paths. |
| Handoffs | Preserve intent across wallet, onramp, swap/bridge, marketplace, and product. |
| Safety | Contextual backup and recovery guidance; migration burden and support handoff where relevant. |

Use safe fixtures for interaction tests. Never ask for seed phrases, sign transactions, or send funds solely for an audit. This checks UX, not smart-contract security.
