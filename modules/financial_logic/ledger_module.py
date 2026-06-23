from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from modules.marketplace_integration.export_module import get_supabase_client

TABLE = "transactions"


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    SALE = "sale"


@dataclass
class LedgerEntry:
    sku: str
    type: TransactionType
    amount: float
    description: str = ""
    id: str = ""
    created_at: str = ""


@dataclass
class LedgerSummary:
    sku: str | None  # None means all SKUs
    total_cost: float
    total_revenue: float
    entries: list[LedgerEntry] = field(default_factory=list)

    @property
    def gross_profit(self) -> float:
        return round(self.total_revenue - self.total_cost, 2)

    @property
    def margin(self) -> float | None:
        if self.total_revenue == 0:
            return None
        return round(self.gross_profit / self.total_revenue, 4)

    @property
    def margin_pct(self) -> str:
        return f"{self.margin * 100:.1f}%" if self.margin is not None else "N/A"


def add_entry(sku: str, type: TransactionType, amount: float, description: str = "") -> LedgerEntry:
    client = get_supabase_client()
    row = {
        "sku": sku,
        "type": type.value,
        "amount": amount,
        "description": description,
    }
    response = client.table(TABLE).insert(row).execute()
    data = response.data[0]
    return LedgerEntry(
        id=data.get("id", ""),
        sku=data["sku"],
        type=TransactionType(data["type"]),
        amount=data["amount"],
        description=data.get("description", ""),
        created_at=data.get("created_at", ""),
    )


def get_entries(sku: str | None = None) -> list[LedgerEntry]:
    client = get_supabase_client()
    query = client.table(TABLE).select("*").order("created_at", desc=False)
    if sku:
        query = query.eq("sku", sku)
    response = query.execute()
    return [
        LedgerEntry(
            id=row.get("id", ""),
            sku=row["sku"],
            type=TransactionType(row["type"]),
            amount=row["amount"],
            description=row.get("description", ""),
            created_at=row.get("created_at", ""),
        )
        for row in response.data
    ]


def get_summary(sku: str | None = None) -> LedgerSummary:
    entries = get_entries(sku)
    total_cost = sum(e.amount for e in entries if e.type == TransactionType.PURCHASE)
    total_revenue = sum(e.amount for e in entries if e.type == TransactionType.SALE)
    return LedgerSummary(
        sku=sku,
        total_cost=round(total_cost, 2),
        total_revenue=round(total_revenue, 2),
        entries=entries,
    )
