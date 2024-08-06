from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from deep_translator import GoogleTranslator
import time

def find_and_interact(element_xpath: str, action: str = "click", query: str = "") -> webdriver:
    global driver
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, element_xpath))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    driver.implicitly_wait(2)

    if action == "select":
        Select(element).select_by_value(query)
    elif action == "send_keys":
        element.send_keys(query)
    else:
        # element.click()
        actions = ActionChains(driver)
        actions.move_to_element(element)
        driver.execute_script("arguments[0].click();", element)

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[-1])
    return driver

def extract_date_time_text():
    global driver
    text = driver.find_element(By.TAG_NAME, "body").text
    start, end = "Centrum", ", kaart"

    try:
        start_pos = text.index(start) + len(start)
        end_pos = text.index(end)
        filtered_text = text[start_pos:end_pos].strip()
        translated = GoogleTranslator(source='auto', target='en').translate(filtered_text)
        print(translated)
    except ValueError:
        return ""

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://www.rotterdam.nl/eerste-inschrijving-in-nederland/start-eerste-inschrijving-in-nederland")

xpaths = {
    "appointment": "//a[@class='styles_button__BEjUn' and @title='Afspraak maken' and contains(@href, 'afspraak/maken/zoek/eerstevestigingb')]",
    "subject": "//button[@class='btn btn-link btn-block text-left' and @type='submit' and @name='matches:form:keuzes:0:button:form:give-focus' and @id='id5']",
    "rental": "//select[@class='form-control' and @aria-required='true' and @name='matches:form:keuzes:0:button:form:in-focus:hvv:form:huurOfKoop:field' and @id='id10']",
    "postcode": "//input[@type='text' and @class='form-control' and @maxlength='6' and @name='matches:form:keuzes:0:button:form:in-focus:hvv:form:postcodeContainer:postcode' and @id='id17']",
    "postcode_input": "//button[@class='btn btn-secondary' and @type='submit' and @name='matches:form:keuzes:0:button:form:in-focus:hvv:form:afspraak' and @id='id12']",
    "quantity_input": "//button[@class='btn btn-secondary' and @type='submit' and @value='button' and @name='verder' and @id='id1a']",
    "dates": "//button[@class='list-group-item list-group-item-action flex-column align-items-start' and @name='keuzes:0:give-focus' and @id='id1f']",
    "dates_input": "//button[@class='btn btn-secondary' and @type='submit' and @value='button' and @name='keuzes:0:in-focus:button' and @id='id20']",
    "calendar": "//span[@class='input-group-text' and @title='Kies datum ...']"
}

find_and_interact(xpaths["appointment"])
find_and_interact(xpaths["subject"])
find_and_interact(xpaths["rental"], action="select", query="HUUR")
find_and_interact(xpaths["postcode"], action="send_keys", query="3039RL")
find_and_interact(xpaths["postcode_input"])
find_and_interact(xpaths["quantity_input"])
find_and_interact(xpaths["dates"])

driver.save_screenshot("options.png")
extract_date_time_text()

find_and_interact(xpaths["dates_input"])
find_and_interact(xpaths["calendar"])

time.sleep(0.5)
driver.save_screenshot("calendar.png")
driver.quit()