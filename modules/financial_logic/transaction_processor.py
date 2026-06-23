from dataclasses import dataclass

from modules.financial_logic.ledger_module import (
    LedgerEntry,
    LedgerSummary,
    TransactionType,
    add_entry,
    get_item_cost,
    get_summary,
)
from modules.financial_logic.pricing_engine import calculate_margin


@dataclass
class SaleResult:
    entry: LedgerEntry
    cost: float
    sale_price: float
    margin: float        # decimal ratio, e.g. 0.60
    vat_due: float       # £ amount (margin / 6 at 20% VAT)
    net_retained: float  # £ amount after VAT

    @property
    def margin_pct(self) -> str:
        return f"{self.margin * 100:.1f}%"

    @property
    def gross_margin(self) -> float:
        return round(self.sale_price - self.cost, 2)

    @property
    def profit(self) -> float:
        return self.net_retained


def process_purchase(sku: str, cost: float, description: str = "") -> LedgerEntry:
    if cost <= 0:
        raise ValueError("cost must be greater than 0")
    return add_entry(sku, TransactionType.PURCHASE, cost, description or f"Purchase of {sku}")


def process_sale(sku: str, sale_price: float, description: str = "") -> SaleResult:
    if sale_price <= 0:
        raise ValueError("sale_price must be greater than 0")

    cost = get_item_cost(sku)

    if sale_price <= cost:
        raise ValueError(
            f"sale_price £{sale_price} must exceed cost_price £{cost} for SKU '{sku}'"
        )

    gross_margin = round(sale_price - cost, 2)
    vat_due = round(gross_margin / 6, 2) if gross_margin > 0 else 0.0
    net_retained = round(gross_margin - vat_due, 2)
    margin = calculate_margin(cost, sale_price)

    entry = add_entry(sku, TransactionType.SALE, sale_price, description or f"Sale of {sku}")

    return SaleResult(
        entry=entry,
        cost=cost,
        sale_price=sale_price,
        margin=margin,
        vat_due=vat_due,
        net_retained=net_retained,
    )


def get_item_pnl(sku: str) -> LedgerSummary:
    return get_summary(sku)


def get_portfolio_pnl() -> LedgerSummary:
    return get_summary(sku=None)
