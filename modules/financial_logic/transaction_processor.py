from dataclasses import dataclass

from modules.financial_logic.ledger_module import (
    LedgerEntry,
    LedgerSummary,
    TransactionType,
    add_entry,
    get_summary,
)
from modules.financial_logic.pricing_engine import calculate_margin


@dataclass
class SaleResult:
    entry: LedgerEntry
    cost: float
    sale_price: float
    margin: float

    @property
    def margin_pct(self) -> str:
        return f"{self.margin * 100:.1f}%"

    @property
    def profit(self) -> float:
        return round(self.sale_price - self.cost, 2)


def process_purchase(sku: str, cost: float, description: str = "") -> LedgerEntry:
    if cost <= 0:
        raise ValueError("cost must be greater than 0")
    return add_entry(sku, TransactionType.PURCHASE, cost, description or f"Purchase of {sku}")


def process_sale(sku: str, sale_price: float, cost: float, description: str = "") -> SaleResult:
    if sale_price <= 0:
        raise ValueError("sale_price must be greater than 0")
    if cost <= 0:
        raise ValueError("cost must be greater than 0")
    if sale_price <= cost:
        raise ValueError("sale_price must be greater than cost")

    entry = add_entry(sku, TransactionType.SALE, sale_price, description or f"Sale of {sku}")
    margin = calculate_margin(cost, sale_price)
    return SaleResult(entry=entry, cost=cost, sale_price=sale_price, margin=margin)


def get_item_pnl(sku: str) -> LedgerSummary:
    return get_summary(sku)


def get_portfolio_pnl() -> LedgerSummary:
    return get_summary(sku=None)
