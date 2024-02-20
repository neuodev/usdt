from trader import Trader
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from selenium.webdriver.chrome.webdriver import WebDriver
import json
from utils import calc_avg_price
from uuid import uuid4


class MarketSnapshot:
    id: str
    traders: list[Trader]
    timestamp: int
    avg_price: float
    screenshot: str

    def __init__(self, id: str, traders: list[Trader], timestamp: int, avg_price: float, screenshot: str) -> None:
        self.id = id
        self.traders = traders
        self.timestamp = timestamp
        self.avg_price = avg_price
        self.screenshot = screenshot

    @staticmethod
    def from_web(driver: WebDriver, rows: list[WebElement]) -> 'MarketSnapshot':
        """
        Expects list of table row elements
        """
        id = uuid4()
        traders = [Trader.from_web(row) for row in rows]
        timestamp = int(datetime.now().timestamp())
        avg_price = calc_avg_price(traders)
        screenshot = "./screenshots/{}.png".format(id)
        driver.save_screenshot(screenshot)

        return MarketSnapshot(
            id=id,
            traders=traders,
            timestamp=timestamp,
            avg_price=avg_price,
            screenshot=screenshot
        )

    @classmethod
    def as_json(self) -> str:
        return json.dumps({
            'id': self.id,
            'traders': self.traders,
            'timestamp': self.timestamp,
            'avg_price': self.avg_price,
            'screenshot': self.screenshot,
        })

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
