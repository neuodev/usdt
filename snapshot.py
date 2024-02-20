from trader import Trader
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from datetime import datetime
import json
from utils import as_screenshot_path
from uuid import uuid4


class MarketSnapshot:
    id: str
    traders: list[Trader]
    date: str
    avg_price: float
    screenshot: str

    def __init__(self,
                 id: str,
                 traders: list[Trader],
                 date: str,
                 avg_price: float,
                 screenshot: str
                 ) -> None:

        self.id = id
        self.traders = traders
        self.date = date
        self.avg_price = avg_price
        self.screenshot = screenshot

    @staticmethod
    def from_web(id: str, rows: list[WebElement]) -> 'MarketSnapshot':
        """
        Expects list of table row elements
        """
        traders = [Trader.from_web(row) for row in rows]
        date = datetime.now().strftime("%Y-%m-%d")
        avg_price = MarketSnapshot.calc_avg_price(traders)
        screenshot = as_screenshot_path(id)

        return MarketSnapshot(
            id=id,
            traders=traders,
            date=date,
            avg_price=avg_price,
            screenshot=screenshot
        )

    @staticmethod
    def from_dict(snapshot: dict) -> 'MarketSnapshot':
        traders = [Trader.from_dict(trader) for trader in snapshot['traders']]

        return MarketSnapshot(
            id=snapshot['id'],
            traders=traders,
            date=snapshot['date'],
            avg_price=snapshot['avg_price'],
            screenshot=snapshot['screenshot']
        )

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'traders': [trader.as_dict() for trader in self.traders],
            'date': self.date,
            'avg_price': self.avg_price,
            'screenshot': self.screenshot,
        }

    @staticmethod
    def calc_avg_price(traders: list[Trader]) -> float:
        return sum([trader.price for trader in traders]) / len(traders)
