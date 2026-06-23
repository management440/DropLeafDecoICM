# VAT Margin Scheme (Antiques) — ICM Sovereign Knowledge Base

## Core Principle

VAT is due only on the **profit margin**, not the full selling price.

---

## Formula

```
Selling Price   = Selling Price (inclusive of VAT)
Purchase Price  = Purchase Price (exclusive of VAT)

Margin          = Selling Price - Purchase Price
VAT Due         = Margin * (1/6)    # Assuming 20% standard rate
```

---

## Constraints

- Items must be **eligible for the scheme** (e.g., antiques, second-hand furniture)
- Purchase and sale records must be **strictly linked by SKU**
- **Negative margins** (losses) result in **zero VAT liability**

---

## Ledger Implementation

`transaction_processor.py` must look up the `purchase_price` from the `items` table before calculating tax on a `sale` type transaction.

The VAT calculation must not be performed using the `amount` field alone — the cost basis must be retrieved from the item record to ensure the margin is computed correctly per-SKU.

### Required flow for `process_sale()`

```
1. Receive: sku, sale_price
2. Look up: purchase_price = items[sku].cost_price
3. Calculate: margin = sale_price - purchase_price
4. Calculate: vat_due = margin * (1/6)  if margin > 0 else 0
5. Record:    sale transaction to ledger
6. Return:    SaleResult with margin, vat_due, net_retained
```

---

## Eligibility

Items qualify if:

- They are second-hand or antique goods (previously owned)
- They were purchased without a VAT invoice (private seller, unregistered dealer, or margin scheme dealer)
- They can be re-used in their current state or after repair

Items that do **not** qualify:

- Goods purchased with a standard VAT invoice
- Items where input VAT was charged and reclaimed
- Precious metals or investment gold

---

## VAT Registration Threshold

| | |
|---|---|
| Mandatory registration | £90,000 taxable turnover (rolling 12 months) |
| Voluntary registration | Available below threshold |
| VAT rate on margin | 20% standard rate |

Turnover for threshold purposes = total **selling prices**, not margins.

---

## Record-Keeping Requirements (HMRC VAT Notice 718)

Per-item stock book must record:

- Stock reference / SKU
- Date of purchase
- Description of item
- Name and address of seller
- Purchase price
- Date of sale
- Selling price
- Margin and VAT due

Sales invoices must **not** show VAT as a separate line. Required invoice statement:

> *"This invoice is issued under the VAT margin scheme and does not give the right to reclaim the VAT shown."*

Records must be retained for **6 years**.

---

## Key Rules Summary

| Rule | Detail |
|---|---|
| VAT base | Margin only — never full selling price |
| Cost basis | Must be linked to purchase record by SKU |
| Negative margin | Zero VAT due; loss is not transferable |
| No input VAT reclaim | Cannot reclaim VAT on eligible purchases |
| Invoice format | VAT must not appear as a separate line |
| Retention | 6 years |
| Threshold | £90,000 rolling 12-month turnover |
