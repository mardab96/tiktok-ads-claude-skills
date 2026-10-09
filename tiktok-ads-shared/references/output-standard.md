# Output standard

Every output separates supplied evidence from an explanation. A missing export or screenshot becomes `needs_data`; it never becomes a made-up fact.

## Evidence tags

- `ads_export`
- `search_terms_export`
- `events_diagnostics`
- `shop_export`
- `analytics_export`
- `screenshot`
- `creative_script`
- `comment_cluster`
- `change_log`
- `landing_page`
- `hypothesis`
- `needs_data`

## Verdict vocabulary

Use only these labels for a finding or recommendation:

| Label | Meaning |
|---|---|
| `confirmed` | Direct supplied evidence establishes the finding. |
| `likely` | The pattern fits and stronger alternatives were checked, but no direct confirmation exists. |
| `possible` | The pattern is compatible with more than one explanation. |
| `needs_data` | A required source, setting, date range, or denominator is missing. |
| `monitor` | The evidence is mature enough to watch, but does not justify an action. |
| `hold` | Do not advance a live change until a stated prerequisite is met. |
| `approval_needed` | The recommendation is ready for a named human decision. |

Severity remains `low`, `medium`, `high`, or `critical`. Confidence remains `low`, `medium`, or `high`. Business impact is `spend`, `conversion`, `revenue`, `profit`, `measurement`, `brand_safety`, or `client_trust`.

## Required decision table

| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

## Failure modes

Reject an output that treats platform conversions as profit, calls tracking broken from CPA alone, calls fatigue from a thin window, hides the conversion lag, compares unmatched reporting sources, or promises a live result. Recommendations stop at an approval-ready action.