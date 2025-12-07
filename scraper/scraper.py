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


load_dotenv()


def run_bot_detection(driver, wait):
    try:
        if "Click the button below to continue shopping" in driver.page_source:
            try:
                wait.until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "button[type='submit']")
                    )
                )
                btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                if btn:
                    btn.click()
                    return
            except Exception as e:
                print("Bot detection button click error: ", e)

        try:
            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//img[contains(@alt, "Sorry! Something went wrong")]')
                )
            )
            imgs = driver.find_elements(
                By.XPATH, '//img[contains(@alt, "Sorry! Something went wrong")]'
            )
            if imgs:
                imgs[0].click()
                return
        except Exception as e:
            print("Bot detection image click error: ", e)
    except Exception as e:
        print(f"Bot detection error: {e}")


def run_location_change(driver, wait):
    try:
        location_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "nav-global-location-slot"))
        )
        location_btn.click()

        zip_input = wait.until(
            EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput"))
        )

        random_zip = random_address.real_random_address()["postalCode"]
        zip_input.clear()
        zip_input.send_keys(random_zip)

        try:
            apply_btn = wait.until(EC.element_to_be_clickable((By.ID, "GLUXZipUpdate")))
            apply_btn.click()
        except:
            pass

        try:
            done_btn = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Done')]")
                )
            )
            done_btn.click()
        except:
            pass

        driver.refresh()
        time.sleep(1)

    except Exception as error:
        print("Location change error: ", error)


def run_search(driver, wait, query):
    try:
        search_input = wait.until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        if search_input:
            search_input.send_keys(query + Keys.ENTER)
    except Exception as e:
        raise e


def scraper(query):
    driver = get_driver()
    st.session_state.driver = driver
    url = f"{os.getenv('BASE_URL')}"
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    try:
        run_bot_detection(driver, wait)
        run_location_change(driver, wait)

        run_search(driver, wait, query)
        return driver.page_source
    except Exception as e:
        st.session_state.clear()
        st.rerun()
        raise e
    finally:
        driver.quit()
        if st.session_state.get("driver"):
            st.session_state.driver = None
