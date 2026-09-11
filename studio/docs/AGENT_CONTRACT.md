# Agent and deterministic design contract

The agent proposes intent. The domain layer validates it. The source of truth remains SQLite.

## Current tools

Start the stdio MCP adapter with Python:

```sh
python3 studio/backend/mcp_server.py
```

In an MCP client, use the absolute path to that script and a Python 3.10+ executable. `STUDIO_DB` can point at an isolated database for evaluation. Protocol baseline is [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25); the adapter also negotiates the listed earlier compatible versions. It implements initialize, ping, tool listing and JSON-RPC tool calls over newline-delimited stdio.

| Tool | Operation |
|---|---|
| showroom_summary | Read current revision, coverage, issues and missing-product alternatives |
| showroom_records | Read a whitelisted table, optionally by stable ID |
| propose_showroom | Save a draft refresh, new-product placement, rotating color sequence or bounded fixture move |

No arbitrary SQL, shell execution, ordering, messaging, work release or physical verification is exposed as an agent tool. This adapter is implemented and covered by protocol/domain checks; a third-party MCP client connection has not been exercised in this delivery.

## Example agent request

```json
{
  "mode": "new_product",
  "product_id": "tuscano-burgundy",
  "base_revision": 1
}
```

Read the live revision first; do not copy `1` into later runs. The response returns a saved scenario ID. Read that scenario to inspect its slot, variant, reason, score and release dependencies.

## Deterministic behavior

1. Protect live applications, furniture and documented bookmatch groups during routine refresh. Exclude discontinued products and nominally incompatible formats.
2. Prefer a missing design that can replace a movable repeat while retaining at least one presentation of the old design.
3. Score eligible swaps using configured coverage, repeat value, Hit exposure and change cost. Whole panels precede cut waterfall work. Stable iteration/IDs break ties reproducibly.
4. Offer color sequencing as a separate complete run proposal: family, temperature group, then ascending image-derived brightness rank. Merch can replace these provisional ranks.
5. Accept explicit fixture targets in mm/degrees, preserving both faces with the frame. Check bounds, protected room rectangles, rotated-frame collisions and the draft central route.
6. Save source revision, before/after coverage and reasons. Proposals never rewrite reported installation records.

This is a bounded greedy planner, not a globally optimal constraint solver. It preserves coverage locally but does not yet optimize all family adjacency, cost, travel envelopes, stock allocation, lighting and architectural constraints together. Some hard domain protections intentionally cannot be disabled through a rule's UI switch.

## Judgment guidelines

- Read lifecycle, source confidence and identity aliases before treating a portfolio option as a released SKU.
- Prefer breadth without breaking an intentional bookmatch or useful finish comparison.
- Keep products in a family close together when the available run permits it. Explain tradeoffs when breadth and adjacency conflict.
- Treat visibility scores and brightness-derived colors as a sketch until Merch confirms them.
- Route a product with no suitable slot to a sample-library or new-fixture proposal; never claim a resized image establishes physical fit.
- Do not infer permission to notify staff or submit an order from a generated task. Integrations need explicit policy and actual delivery confirmation.
- Stop release at the exposed missing data; produce useful collection tasks instead of fabricating SKU, stock, measurements or approval.

## Authority

Merch owns guideline changes and release. Designers contribute geometry/brand judgments and drafts. Showroom managers record actual setup and completion evidence. Agents produce complete proposals through the same validator. Later bounded auto-release can be introduced under a Merch-approved policy after constraints and acceptance tests are proven.
