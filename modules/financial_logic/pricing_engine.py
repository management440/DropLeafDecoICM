from dataclasses import dataclass


DEFAULT_TARGET_MARGIN = 0.60  # 60% gross margin


@dataclass
class PricingResult:
    cost: float
    list_price: float
    margin: float  # as a decimal, e.g. 0.60 for 60%

    @property
    def margin_pct(self) -> str:
        return f"{self.margin * 100:.1f}%"

    @property
    def profit(self) -> float:
        return self.list_price - self.cost


def suggest_list_price(cost: float, target_margin: float = DEFAULT_TARGET_MARGIN) -> float:
    """Return the list price required to achieve target_margin on cost."""
    if not (0 < target_margin < 1):
        raise ValueError("target_margin must be between 0 and 1 (e.g. 0.60 for 60%)")
    if cost <= 0:
        raise ValueError("cost must be greater than 0")
    return round(cost / (1 - target_margin), 2)


def calculate_margin(cost: float, list_price: float) -> float:
    """Return the gross margin as a decimal given cost and list price."""
    if list_price <= 0:
        raise ValueError("list_price must be greater than 0")
    if cost <= 0:
        raise ValueError("cost must be greater than 0")
    if cost >= list_price:
        raise ValueError("cost must be less than list_price")
    return round((list_price - cost) / list_price, 4)


def price(cost: float, target_margin: float = DEFAULT_TARGET_MARGIN) -> PricingResult:
    """Return a PricingResult with suggested list price and achieved margin."""
    list_price = suggest_list_price(cost, target_margin)
    margin = calculate_margin(cost, list_price)
    return PricingResult(cost=cost, list_price=list_price, margin=margin)
