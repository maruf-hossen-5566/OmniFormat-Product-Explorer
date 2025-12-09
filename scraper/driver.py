from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .proxy import get_proxy


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-background-networking")
    chrome_options.add_argument("--disable-default-apps")
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_argument("--metrics-recording-only")
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--disable-features=InterestFeedContentSuggestions")
    chrome_options.add_argument("--disable-features=AutofillServerCommunication")
    chrome_options.add_argument("--window-size=1920,1080")

    proxy = get_proxy()
    if proxy:
        chrome_options.add_argument(f"--proxy-server-{proxy}")

    return webdriver.Chrome(options=chrome_options)
