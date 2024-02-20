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
    timestamp: int
    avg_price: float
    screenshot: str

    def __init__(self,
                 id: str,
                 traders: list[Trader],
                 timestamp: int,
                 avg_price: float,
                 screenshot: str
                 ) -> None:

        self.id = id
        self.traders = traders
        self.timestamp = timestamp
        self.avg_price = avg_price
        self.screenshot = screenshot

    @staticmethod
    def from_web(id: str, rows: list[WebElement]) -> 'MarketSnapshot':
        """
        Expects list of table row elements
        """
        traders = [Trader.from_web(row) for row in rows]
        timestamp = int(datetime.now().timestamp())
        avg_price = MarketSnapshot.calc_avg_price(traders)
        screenshot = as_screenshot_path(id)
        
        return MarketSnapshot(
            id=id,
            traders=traders,
            timestamp=timestamp,
            avg_price=avg_price,
            screenshot=screenshot
        )

    @staticmethod
    def from_dict(snapshot: dict) -> 'MarketSnapshot':
        traders = [Trader.from_dict(trader) for trader in snapshot['traders']]

        return MarketSnapshot(
            id=snapshot['id'],
            traders=traders,
            timestamp=snapshot['timestamp'],
            avg_price=snapshot['avg_price'],
            screenshot=snapshot['screenshot']
        )

    def as_dict(self) -> dict:
        return {
            'id': self.id,
            'traders': [trader.as_dict() for trader in self.traders],
            'timestamp': self.timestamp,
            'avg_price': self.avg_price,
            'screenshot': self.screenshot,
        }

    @staticmethod
    def calc_avg_price(traders: list[Trader]) -> float:
        return sum([trader.price for trader in traders]) / len(traders)
