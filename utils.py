from trader import Trader


def as_float(value: str) -> float:
    return float(value.replace(',', ''))


def calc_avg_price(traders: list[Trader]) -> float:
    return sum([trader.price for trader in traders]) / len(traders)
