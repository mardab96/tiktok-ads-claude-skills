---
name: gmv-max-profit-check-tiktok-ads
description: Turns TikTok Shop and GMV Max reporting into a per-product cost-stack ledger with refunds, affiliate commissions, seller-funded coupons, referral fees, ad spend, COGS, and seller-borne shipping, using gmv_profit.py to flag any incomplete cost stack (T09). Use when a TikTok Shop seller or media buyer says "GMV Max ROI looks great but we are not making money", "is this product profitable on TikTok Shop", "check our TikTok Shop margins", "affiliate commissions are eating us", or before raising a GMV Max budget or ROI target.
---

# GMV Max Profit Check: TikTok Ads

## Use this skill when

GMV Max reports gross merchandise value and a platform return figure on ad spend. Treat both as gross unless your report states otherwise: neither shows the refunds, affiliate commission, seller-funded coupons, referral fees, product cost, and seller-borne shipping that decide margin. This skill builds that ledger per product, refuses a profit claim while any cost line is missing (T09), and states what a buyer may and may not conclude. Work from Seller Center and Ads Manager exports; a TikTok for Business connector in Claude is optional.

Typical requests:

- "GMV Max shows strong ROI. Finance says we lose money on Shop. Who is right?"
- "Which SKUs should get more GMV Max budget?"
- "Affiliate creators drive most sales. What is left after their commission?"
- "Refunds spiked. What does that do to last month's numbers?"
- "Can we lower the ROI target and still make money?"

Do not use this skill when:

- Question concerns website pixel purchases instead of Shop orders. Run `pixel-events-api-check-tiktok-ads` or `attribution-gap-check-tiktok-ads`.
- Budget size and pacing is the decision after margin is known. Run `budget-scaling-planner-tiktok-ads`.
- Bid or ROI target mechanics need review. Run `bid-strategy-check-tiktok-ads`, with this ledger attached.
- A broader account with no Shop is in scope. Run `account-triage-tiktok-ads`.

## Required input

Every cost line comes from a supplied export or a business-owned figure. A blank line stays missing and never becomes zero.

Build one CSV per period with these exact column headers, one row per product or SKU:

`product, revenue, refunds, affiliate_commission, coupons, referral_fees, ad_spend`

Where each column comes from (Seller Center names vary by market, as labelled in your account):

| Column | Typical source | Note |
|---|---|---|
| `revenue` | Seller Center **Orders** or **Finance** settlement report | Gross product revenue before refunds |
| `refunds` | **Orders** returns and refunds, or settlement adjustments | Same order-date window |
| `affiliate_commission` | **Affiliate** commission report | Use settled or estimated, and say which |
| `coupons` | **Promotions** report | Seller-funded share only |
| `referral_fees` | **Finance** settlement fee lines | Platform commission or referral fee as labelled |
| `ad_spend` | Ads Manager GMV Max campaign report, product level if available | Same dates and currency |

Also required for a profit claim: COGS per unit and units sold per product, and seller-borne shipping per product or order. Also required: period, market, currency, and whether figures are by order date or settlement date.

### Optional input

- Platform GMV and ROI as shown in GMV Max reporting, for comparison with the ledger.
- Refund window or return policy length, to judge how mature recent orders are.
- Sample-order or free-sample cost sent to affiliates, if the business tracks it.

## Before analysis

1. Agree the unit of analysis: product, SKU, or GMV Max campaign. Keep one key across every export so rows join cleanly.
2. Ask how affiliate-driven orders and ad-driven orders overlap in the shop's reporting. If one order can carry both an affiliate commission and GMV Max credit, keep both costs on the row; the cost is real even if the credit is shared.
3. Ask who funds each promotion. Platform-funded and seller-funded discounts can sit in one report column.
4. Confirm the return window per market and today's date, so the immature part of the period is known before reading results.
5. Record whether ad spend is product-level or campaign-level. Campaign-level spend split across products by GMV share is an allocation, labelled `hypothesis`.

## Analysis workflow

1. Align period, market, and currency across every export. Mark whether each source is by order date or settlement date; a ledger that mixes them shows fees and revenue from different orders.
2. Normalise numbers before running the script. `gmv_profit.py` strips `$` and rejects commas or non-finite values as missing. Convert decimal commas (12,50) to points (12.50) and remove thousands separators (1.234,56 becomes 1234.56). Remove other currency symbols or codes (EUR, GBP, PLN), otherwise the row remains incomplete.
3. Build the CSV with the exact headers above. Enter a true zero as `0`; leave unknown cells blank so they stay missing.
4. Run the helper from this skill folder:

   ```bash
   python3 ../tiktok-ads-shared/scripts/gmv_profit.py shop_ledger.csv
   ```

   From an installed copy, use `~/.claude/skills/tiktok-ads-shared/scripts/gmv_profit.py`. A synthetic sample lives at `../tiktok-ads-shared/examples/data/gmv_profit.csv`.
5. Read the tab-separated output. Columns: `product`, `revenue`, `cost_stack`, `contribution_before_cogs`, `status`, `missing_columns`. `cost_stack` sums refunds, affiliate_commission, coupons, referral_fees, and ad_spend as absolute values, so negative signs from settlement exports are safe. `complete_cost_stack` means every visible cell parsed. `incomplete_cost_stack / needs_data` prints `n/a` and names each missing column (T09). Exit code 2 with an `ERROR:` line means the file could not open or a required header is absent.
6. Add COGS and seller-borne shipping by hand for complete rows: contribution after COGS and shipping equals `contribution_before_cogs` minus COGS minus seller shipping. Without both inputs, report contribution before COGS only and label profit `needs_data`.
7. Compare the ledger with platform figures. Show GMV, platform ROI, contribution before COGS, and contribution after COGS and shipping side by side, per product.
8. Check refund maturity. Orders still inside the return window can still refund; label the most recent period immature when the refund window has not closed.
9. Produce an action list: which cost lines to collect, which products are `monitor`, `hold`, or `approval_needed` for a budget or target conversation.

## Decision rules

| Condition | Evidence | Verdict | Next step |
|---|---|---|---|
| Any of revenue, refunds, affiliate commission, coupons, referral fees, or ad spend blank or unparseable (T09) | `shop_export` + script status | `needs_data` | Collect the named column; no profit or scale verdict |
| Visible stack complete, COGS or seller shipping missing (T09) | script output | `needs_data` for profit | Report contribution before COGS only |
| Contribution after COGS and shipping negative on a product carrying meaningful GMV Max spend | ledger | `approval_needed` | Owner decision on target, budget, or product exclusion; route to `bid-strategy-check-tiktok-ads` |
| Contribution positive, refund window closed | ledger | `monitor` or `approval_needed` for scale | Route to `budget-scaling-planner-tiktok-ads` |
| Contribution positive, refund window still open | ledger + return policy | `hold` | Recheck after the window closes |
| Order-date and settlement-date sources mixed | export metadata | `needs_data` | Rebuild on one basis |
| Affiliate commission estimated, not settled | Affiliate report | `possible` | Label estimate; recheck on settlement |

## Output format

```markdown
## GMV Max Profit Check: [shop], [market], [period], [currency], [order date / settlement date basis]

**Verdict:** [shared verdict label] because [strongest evidence]
**Script:** gmv_profit.py on [file name]; rows complete: [n] of [n]

### Shop economics ledger
| Product | GMV (platform) | Revenue | Refunds | Affiliate | Coupons | Referral fees | Ad spend | Contribution before COGS | COGS | Seller shipping | Contribution after COGS and shipping | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

### Platform view vs ledger
| Product | Platform ROI | Contribution after COGS and shipping per unit of ad spend | Gap explanation |
|---|---|---|---|

### Decision table
| Finding | Evidence | Verdict | Severity | Confidence | Business impact | Next step |
|---|---|---|---|---|---|---|

### Cost lines to collect
- [product]: [column], source: [report], owner: [name]

### Data gaps
- [missing item]: blocks [conclusion]
```

## Practical example

Illustrative numbers from the synthetic sample file, not a benchmark. Running the helper on `../tiktok-ads-shared/examples/data/gmv_profit.csv` returns:

```text
product	revenue	cost_stack	contribution_before_cogs	status	missing_columns
Starter kit	1000.00	445.00	555.00	complete_cost_stack
Incomplete refill	n/a	n/a	n/a	incomplete_cost_stack / needs_data	affiliate_commission
```

Starter kit: revenue 1,000, refunds 50, affiliate commission 100, coupons 75, referral fees 40, ad spend 180, so cost stack 445 and contribution before COGS 555. GMV Max reporting would show 1,000 GMV on 180 spend. Suppose the business supplies COGS of 320 and seller shipping of 90 for those units: contribution after COGS and shipping is 145. Verdict `monitor`, with scale routed to `budget-scaling-planner-tiktok-ads` once the refund window closes.

Incomplete refill: affiliate commission blank. T09 applies; verdict `needs_data`, no profit statement, collection task assigned to whoever owns the Affiliate report.

## Common misreads

- Reading GMV Max ROI as profit. As reported, it leaves out the fee, commission, COGS, and shipping stack, and refunds unless your report says it nets them.
- Feeding net-of-refund revenue into `revenue` and also filling `refunds`, which subtracts refunds twice.
- Counting platform-funded coupons as a seller cost. Only the seller-funded share belongs in `coupons`.
- Typing 0 into a blank affiliate cell to make the script pass. That turns an unknown into a fake profit.
- Running European-format numbers with decimal commas, which the script reads as values a hundred times too large.
- Comparing an order-date revenue export with a settlement-date fee export.
- Judging last week's products while the return window is still open.
- Allocating campaign-level ad spend to products by GMV share and then presenting product profit as measured.

## Route to next

- Ledger complete and positive, scale under discussion: `budget-scaling-planner-tiktok-ads`, then `learning-phase-guard-tiktok-ads` (T05) before any live edit.
- Ledger negative on a target-driven campaign: `bid-strategy-check-tiktok-ads` with the ledger attached.
- Affiliate creator content outperforming brand content: `spark-vs-brand-ad-split-tiktok-ads`.
- Client summary of Shop economics: `weekly-client-report-tiktok-ads`.

## Guardrails

- Do not call GMV, platform ROI, or contribution before COGS profit.
- Do not fill a missing fee, refund, or spend cell with zero or an estimate without labelling it `hypothesis`.
- Do not change GMV Max targets, budgets, product selection, or Shop promotions. Output stops at an approval-ready recommendation.
- Do not recommend scaling a product whose cost stack is incomplete under T09.
- Do not apply one market's fee categories to another market.
