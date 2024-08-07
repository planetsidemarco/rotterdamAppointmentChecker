"""
06/08/24
Marco Tyler-Rodrigue
Selenium webscraper for checking rotterdam municipality appointment times
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from deep_translator import GoogleTranslator


XPATHS = {
    "appointment": "//a[@class='styles_button__BEjUn' and @title='Afspraak maken']",
    "subject": "//button[@class='btn btn-link btn-block text-left' and @type='submit'"
    "and @name='matches:form:keuzes:0:button:form:give-focus' and @id='id5']",
    "rental": "//select[@class='form-control' and @aria-required='true' and "
    "@name='matches:form:keuzes:0:button:form:in-focus:hvv:form:huurOfKoop:field' and @id='id10']",
    "postcode": "//input[@type='text' and @class='form-control' and @maxlength='6' and"
    "@name='matches:form:keuzes:0:button:form:in-focus:hvv:form:postcodeContainer:postcode'"
    "and @id='id17']",
    "postcode_input": "//button[@class='btn btn-secondary' and @type='submit' and"
    "@name='matches:form:keuzes:0:button:form:in-focus:hvv:form:afspraak' and @id='id12']",
    "quantity_input": "//button[@class='btn btn-secondary' and @type='submit' and"
    "@value='button' and @name='verder' and @id='id1a']",
    "options": "//button[@class='list-group-item list-group-item-action flex-column "
    "align-items-start' and @name='keuzes:0:give-focus' and @id='id1f']",
    "options_input": "//button[@class='btn btn-secondary' and @type='submit' and @value='button'"
    "and @name='keuzes:0:in-focus:button' and @id='id20']",
    "calendar": "//span[@class='input-group-text' and @title='Kies datum ...']",
}


def find_and_interact(element_xpath: str, action: str = "button", query: str = ""):
    """Find elements and interact with them on a webpage

    Args:
        element_xpath (str): expected element name
        action (str, optional): type of element [button, dropdown, textbox]. Defaults to "button".
        query (str, optional): query for dropdown and textbox elements. Defaults to "".
    """
    print(f"Selecting {element_xpath} element")

    element = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, XPATHS[element_xpath]))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

    time.sleep(1)

    if action == "dropdown":
        select = Select(element)
        select.select_by_value(query)
    elif action == "textbox":
        element.send_keys(query)
    else:
        actions = ActionChains(driver)
        actions.move_to_element(element)
        driver.execute_script("arguments[0].click();", element)

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[-1])


def get_date_time_text():
    """Extract date and time from webpage and creates textfile with result"""
    time.sleep(1)
    text = driver.find_element(By.TAG_NAME, "body").text
    start, end = "Centrum", "Coolsingel"

    try:
        start_pos = text.index(start) + len(start)
        end_pos = text.index(end)
        filtered_text = text[start_pos:end_pos].strip()
        translated = GoogleTranslator(source="auto", target="en").translate(
            filtered_text
        )
        print("Saving earliest appointment date/time to date_time.txt")
        with open("date_time.txt", "w", encoding="utf-8") as file:
            # Write the string to the file
            file.write(f"{translated}\n")
    except ValueError as e:
        print(e)


def no_bookings_text():
    """Creates text file stating no bookings available"""
    print("Saving no bookings available to date_time.txt")
    with open("date_time.txt", "w", encoding="utf-8") as file:
        # Write the string to the file
        file.write("not currently available :(\n")


def check_for_no_bookings():
    """Text"""
    time.sleep(3)
    no_booking_text = "Het spijt ons."
    # Update current url source and get body text
    driver.get("view-source:" + driver.current_url)
    time.sleep(3)
    current_body_text = driver.find_element(By.TAG_NAME, "body").text
    # Check if no booking text exists on page
    if no_booking_text in current_body_text:
        print("No bookings available")
        no_bookings_text()
        driver.quit()
        sys.exit()


def save_full_page_screenshot(filename: str):
    """Helper function to save screenshot of current webpage

    Args:
        filename (str): name of image file
    """
    time.sleep(1)
    print(f"Saving screenshot to {filename}")
    driver.save_screenshot(filename)


# Set up Firefox options
firefox_options = Options()
firefox_options.add_argument("--headless")

# Specify the path to Geckodriver
GECKODRIVER_PATH = "/usr/local/bin/geckodriver"
BASE_URL = "https://www.rotterdam.nl"

# Set up Firefox service
firefox_service = FirefoxService(executable_path=GECKODRIVER_PATH)

# Initialize the Firefox driver with the specified service
driver = webdriver.Firefox(service=firefox_service, options=firefox_options)
driver.maximize_window()
driver.get(
    f"{BASE_URL}/eerste-inschrijving-in-nederland/start-eerste-inschrijving-in-nederland"
)

find_and_interact("appointment")
find_and_interact("subject")
find_and_interact("rental", action="dropdown", query="HUUR")
find_and_interact("postcode", action="textbox", query="3039RL")
find_and_interact("postcode_input")
find_and_interact("quantity_input")

check_for_no_bookings()

find_and_interact("options")
save_full_page_screenshot("options.png")
get_date_time_text()
find_and_interact("options_input")
find_and_interact("calendar")
save_full_page_screenshot("calendar.png")

driver.quit()
