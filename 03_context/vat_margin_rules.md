# VAT Margin Scheme Rules — DropLeaf Deco

## What Is the VAT Margin Scheme?

The VAT Margin Scheme allows dealers of eligible second-hand goods to account for VAT on the **margin** (the difference between purchase price and selling price) rather than on the full selling price. This significantly reduces the VAT liability compared to standard VAT accounting.

Vintage and antique furniture qualifies as an eligible good under HMRC's scheme.

**Reference:** HMRC VAT Notice 718 — The VAT Margin Scheme and global accounting.

---

## Eligibility

Items qualify for the margin scheme if:

- They are **second-hand goods** (previously owned and used)
- They were purchased from a **private individual, unregistered business, or another margin scheme dealer**
- The seller did **not** charge VAT on the sale (i.e., no VAT invoice was issued)
- The item can be **re-used in its current state** or after repair

Items that do **not** qualify:

- Goods purchased with a standard VAT invoice (input VAT was charged)
- Precious metals or investment gold
- Items purchased from a VAT-registered seller who charged VAT

---

## How VAT Is Calculated Under the Scheme

VAT is calculated on the **gross margin** (VAT-inclusive), not the selling price.

### Formula

```
Gross Margin  = Selling Price − Purchase Price
VAT Amount    = Gross Margin × (VAT Rate / (100 + VAT Rate))
             = Gross Margin / 6          (at 20% VAT rate)
Net Margin    = Gross Margin − VAT Amount
```

### Example

| | |
|---|---|
| Purchase price | £100.00 |
| Selling price | £250.00 |
| Gross margin | £150.00 |
| VAT (÷ 6) | £25.00 |
| Net margin (retained) | £125.00 |

If margin is **zero or negative**, no VAT is due on that item. The loss cannot be offset against other items (under individual item accounting).

---

## Integration with the Pricing Engine

The `pricing_engine.py` module targets a **60% gross margin** by default. Under the margin scheme, the effective net margin after VAT is lower:

| Target Gross Margin | VAT Deducted (÷6) | Net Margin Retained |
|---|---|---|
| 60% | ~10% of selling price | ~50% of selling price |
| 50% | ~8.3% of selling price | ~41.7% of selling price |

**Practical implication:** If the business is VAT-registered and operating under the margin scheme, the 60% target in `pricing_engine.py` should be treated as the **gross (VAT-inclusive) margin**. The actual retained margin is approximately 50%.

For a 50% net retained target, the current `DEFAULT_TARGET_MARGIN = 0.60` setting is correct.

---

## VAT Registration Threshold

| | |
|---|---|
| Mandatory registration threshold | £90,000 taxable turnover (rolling 12 months) |
| Voluntary registration | Below threshold — can still register voluntarily |
| VAT rate on margin | 20% (standard rate) |

**Note:** Turnover for threshold purposes = total **selling prices**, not margins.

---

## Record-Keeping Requirements

HMRC requires the following records for each item sold under the scheme:

### Stock Book (per item)
- Stock reference number
- Date of purchase
- Description of item
- Name and address of seller
- Purchase price
- Date of sale
- Selling price
- Margin and VAT due

### Supporting Documents
- Purchase receipts or invoices (even informal ones from private sellers)
- Sales invoices — must **not** show VAT separately (margin scheme invoices must state: *"This invoice is issued under the VAT margin scheme and does not give the right to reclaim the VAT shown"*)
- Records must be kept for **6 years**

---

## Global Accounting (Alternative Method)

Instead of calculating VAT per item, HMRC permits **global accounting** for items purchased for under £500. Under this method:

- Total purchases in the period are pooled
- Total sales are pooled
- VAT is calculated on the overall net margin for the period
- Losses on individual items **can** offset gains

This may be preferable if DropLeaf Deco deals in high volumes of lower-value pieces.

---

## Key Rules Summary

| Rule | Detail |
|---|---|
| VAT on margin only | Never on full selling price |
| No input VAT reclaim | Cannot reclaim VAT on purchases made under the scheme |
| Negative margin | No VAT due; loss not transferable (individual method) |
| Invoice format | Must not show VAT as a separate line |
| Records | 6-year retention requirement |
| Threshold | £90,000 rolling 12-month turnover |
