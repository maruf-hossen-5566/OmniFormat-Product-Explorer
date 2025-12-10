import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver import Keys
from scraper.driver import get_driver
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st
import random_address
from logger import setup_logger
from scraper.utils import random_sleep

logger = setup_logger(__name__)
load_dotenv()


def run_bot_detection(driver, wait):
    random_sleep()
    try:
        logger.info("Waiting for 'continue shopping' button...")
        if "Click the button below to continue shopping" in driver.page_source:
            continue_btn_selector = (By.CSS_SELECTOR, "button[type='submit']")
            wait.until(EC.presence_of_element_located(continue_btn_selector))
            continue_btn = wait.until(EC.element_to_be_clickable(continue_btn_selector))
            if continue_btn:
                continue_btn.click()
                logger.info("Successfully clicked 'continue shopping' button.")
                return
    except Exception as e:
        logger.info("Failed clicking 'continue shopping' button.")

    try:
        logger.info("Waiting for 'something went wrong' image...")
        image_selector = (
            By.XPATH,
            '//img[contains(@alt, "Sorry! Something went wrong")]',
        )
        wait.until(EC.presence_of_element_located(image_selector))
        image = wait.until(EC.element_to_be_clickable(image_selector))
        if image:
            image.click()
            return
    except Exception as e:
        logger.info("Failed clicking 'something went wrong' image")

    logger.info("Bot detection complete.")
    time.sleep(0.7)


"""Uncomment this method to change location if not US"""
"""def run_location_change(driver, wait):
    try:
        logger.info("Waiting for 'zip change modal' button...")
        zip_change_modal_btn_selector = (By.ID, "nav-global-location-slot")
        wait.until(EC.presence_of_element_located(zip_change_modal_btn_selector))
        zip_change_modal_btn = wait.until(
            EC.element_to_be_clickable(zip_change_modal_btn_selector)
        )
        if zip_change_modal_btn:
            zip_change_modal_btn.click()
    except Exception as e:
        logger.exception("Failed clicking 'zip change modal' button.")

    try:
        logger.info("Waiting for 'zip input' field...")
        zip_input_selector = (By.ID, "GLUXZipUpdateInput")
        wait.until(EC.presence_of_element_located(zip_input_selector))
        zip_input = wait.until(
            EC.element_to_be_clickable((By.ID, "GLUXZipUpdateInput"))
        )

        if zip_input:
            zip_input.clear()
            random_zip = random_address.real_random_address()["postalCode"]
            zip_input.send_keys(random_zip + Keys.ENTER)
            logger.info(f"Successfully filled and submitted zip input.")
    except Exception as e:
        logger.exception("Failed filling and submitting zip input field.")

    try:
        logger.info("Waiting for 'zip apply' button...")
        zip_apply_btn = driver.find_element(By.ID, "GLUXZipUpdate")
        if zip_apply_btn:
            zip_apply_btn.click()
            logger.info("Successfully clicked 'zip apply' button.")
    except Exception as e:
        logger.info("Failed/Skipped clicking 'zip apply' button.")

    random_sleep()
    logger.info("Successfully completed location change.")
    driver.refresh()"""


def run_search(driver, wait, query):
    try:
        random_sleep()
        logger.info("Waiting for 'search input' field...")
        search_input_selector = (By.ID, "twotabsearchtextbox")
        wait.until(EC.presence_of_element_located(search_input_selector))
        search_input = wait.until(EC.element_to_be_clickable(search_input_selector))
        logger.info(f"User searched for '{query}'.")
        if search_input:
            search_input.clear()
            search_input.send_keys(f"{query}" + Keys.ENTER)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("Successfully filled and submitted search input.")
    except Exception as e:
        logger.exception("Failed to fill and submit search input field.")
        st.session_state.got_error = True
        raise e


def scraper(query):
    try:
        driver = get_driver()
        st.session_state.driver = driver
        logger.info("Driver initialized successfully.")
    except Exception as e:
        logger.exception("Failed to initialize driver.")
        st.session_state.clear()
        raise e

    try:
        url = f"{os.getenv('BASE_URL')}"
        driver.get(url)
        logger.info(f"Website opened successfully.")
        wait = WebDriverWait(driver, 25)
    except Exception as e:
        logger.exception("Failed to get the page.")
        st.session_state.clear()
        raise e

    try:
        run_bot_detection(driver, wait)
        """run_location_change(driver, wait)"""

        run_search(driver, wait, query)
        time.sleep(3)
        page_source = driver.page_source
        logger.info("Successfully extracted page source.")
        return page_source
    except Exception as e:
        logger.exception("Failed at run 'scraping'.")
        raise e
    finally:
        driver.quit()
        if st.session_state.get("driver"):
            st.session_state.driver = None
        logger.info("Driver closed successfully.")
