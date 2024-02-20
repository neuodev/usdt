from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from utils import as_float


def get_limits(tr: WebElement) -> tuple[str, str]:
    div = tr.find_element(
        By.CSS_SELECTOR, 'td:nth-child(3) > div > div:nth-child(2)')
    lower = div.find_element(
        By.CSS_SELECTOR, 'div:nth-child(1)').text.replace('E£\n', '')
    upper = div.find_element(
        By.CSS_SELECTOR, 'div:nth-child(3)').text.replace('E£\n', '')

    return (upper, lower)


class Trader:
    name: str
    url: str
    price: float
    supply: float
    limit: tuple[float, float]

    def __init__(self, name: str, url: str, price: float, supply: float, limit: tuple[float, float]) -> None:
        self.name = name
        self.url = url
        self.price = price
        self.supply = supply
        self.limit = limit

    @staticmethod
    def from_web(el: WebElement) -> 'Trader':
        """
        Expects the table row web element  
        """
        trader = el.find_element(
            By.CSS_SELECTOR, 'td > div > div > div > a')
        price = el.find_element(
            By.CSS_SELECTOR, 'td:nth-child(2) > div > div')
        supply = el.find_element(
            By.CSS_SELECTOR, 'td:nth-child(3) > div > div')

        (lower_limit, upper_limit) = get_limits(el)

        return Trader(
            name=trader.text,
            url=trader.get_attribute('href'),
            price=as_float(price.text),
            supply=as_float(supply.text),
            limit=(as_float(upper_limit), as_float(lower_limit))
        )
