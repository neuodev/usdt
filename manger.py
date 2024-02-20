from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from time import sleep
from snapshot import MarketSnapshot
from uuid import uuid4
from utils import as_screenshot_path
from store import Store


class Manger:
    driver: WebDriver
    store: Store

    def __init__(self, driver: WebDriver, store: Store) -> None:
        self.driver = driver
        self.store = store

    def start(self):
        while True:
            url = 'https://p2p.binance.com/en/trade/sell/USDT?fiat=EGP&payment=BANK'
            self.driver.get(url)

            sleep(5)  # wait until page is populated with data

            rows = self.driver.find_elements(By.CSS_SELECTOR, '.bn-table-row')
            id = str(uuid4())
            self.driver.save_screenshot(as_screenshot_path(id))
            snapshot = MarketSnapshot.from_web(id, rows)
            self.store.append(snapshot)

            sleep(60 * 4)  # 4min
