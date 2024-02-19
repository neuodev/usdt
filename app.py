from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webelement import WebElement
import sys
from time import sleep
import json
from datetime import datetime


headless = "--headless" in sys.argv

options = Options()

if headless:
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)
driver.set_window_size(1300, 1200)

url = 'https://p2p.binance.com/en/trade/sell/USDT?fiat=EGP&payment=BANK'
driver.get(url)


sleep(10)
elements = driver.find_elements(By.CSS_SELECTOR, '.bn-table-row')
print("Found {} rows".format(len(elements)))


driver.save_screenshot('./test.png')


def get_trader(tr: WebElement):
    trader = tr.find_element(
        By.CSS_SELECTOR, 'td > div > div > div > a').text
    price = tr.find_element(
        By.CSS_SELECTOR, 'td:nth-child(2) > div > div').text
    supply = tr.find_element(
        By.CSS_SELECTOR, 'td:nth-child(3) > div > div').text

    (lower_limit, upper_limit) = get_limits(tr)

    return {
        'trader': trader,
        'price': clean_numeric_str(price),
        'supply':  clean_numeric_str(supply.replace('USDT', '').strip()),
        'limit': [clean_numeric_str(lower_limit), clean_numeric_str(upper_limit)]
    }


def get_traders(table_rows: list[WebElement]):
    return [get_trader(row) for row in table_rows]


def clean_numeric_str(value: str):
    return float(value.replace(',', ''))

# todo: save a screenshot (path to it)!


def get_limits(tr: WebElement):
    div = tr.find_element(
        By.CSS_SELECTOR, 'td:nth-child(3) > div > div:nth-child(2)')
    lower = div.find_element(
        By.CSS_SELECTOR, 'div:nth-child(1)').text.replace('E£\n', '')
    upper = div.find_element(
        By.CSS_SELECTOR, 'div:nth-child(3)').text.replace('E£\n', '')

    return (upper, lower)

def calc_avg_price(traders) -> float: 
    return sum([trader['price'] for trader in traders]) / len(traders)




traders = get_traders(elements)
timestamp = int(datetime.now().timestamp())
avg_price = calc_avg_price(traders)
as_json = json.dumps({'traders': traders, 'timestamp': timestamp, 'avg_price': avg_price})


with open('data.json', 'w') as f:
    f.write(as_json)

driver.close()
