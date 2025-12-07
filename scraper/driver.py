from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .proxy import get_proxy


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    proxy = get_proxy()
    if proxy:
        chrome_options.add_argument(f"--proxy-server-{proxy}")

    return webdriver.Chrome(options=chrome_options)
