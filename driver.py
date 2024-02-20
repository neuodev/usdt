from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.webdriver import WebDriver
import sys


def init() -> WebDriver:
    headless = "--headless" in sys.argv
    options = Options()
    if headless:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')

    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.set_window_size(1300, 1500)

    return driver
