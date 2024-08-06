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

def find_and_click(element_xpath: str, dropdown: bool=False, dropdown_query: str="", textbox: bool=False, textbox_query: str="") -> webdriver:
    clickable_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, element_xpath))
    )
    # Scroll the button into view
    driver.execute_script("arguments[0].scrollIntoView(true);", clickable_element)

    # Wait a bit for the page to settle after scrolling
    driver.implicitly_wait(2)

    if dropdown:
        select = Select(clickable_element)
        select.select_by_value(dropdown_query)
    
    elif textbox:
        # button.clear()

        # Send keys to the text box
        clickable_element.send_keys(textbox_query)
    
    else:
        actions = ActionChains(driver)
        actions.move_to_element(clickable_element)
        driver.execute_script("arguments[0].click();", clickable_element)

    # Wait for a new window or tab to open
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    return driver

# Extract text between the keywords
def extract_date_time_text():
    text = driver.find_element(By.TAG_NAME, "body").text

    start = "Centrum"
    end = ", kaart"  
    try:
        # Find the start and end positions
        start_pos = text.index(start) + len(start)
        end_pos = text.index(end)
        
        # Extract and return the text between the keywords
        filtered_text = text[start_pos:end_pos].strip()
        translated = GoogleTranslator(source='auto', target='en').translate(filtered_text)
        print(translated)

    except ValueError:
        # If either keyword is not found, return an empty string
        return ""


# Setup the webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Maximize the window to ensure all elements are visible
driver.maximize_window()

# Navigate to the initial page
driver.get("https://www.rotterdam.nl/eerste-inschrijving-in-nederland/start-eerste-inschrijving-in-nederland")

# Wait for the button to be present, using a very specific XPath
appointment_xpath = "//a[@class='styles_button__BEjUn' and @title='Afspraak maken' and contains(@href, 'afspraak/maken/zoek/eerstevestigingb')]"
subject_xpath = "//button[@class='btn btn-link btn-block text-left' and @type='submit' and @name='matches:form:keuzes:0:button:form:give-focus' and @id='id5']"
rental_xpath = "//select[@class='form-control' and @aria-required='true' and @name='matches:form:keuzes:0:button:form:in-focus:hvv:form:huurOfKoop:field' and @id='id10']"
postcode_xpath = "//input[@type='text' and @class='form-control' and @maxlength='6' and @name='matches:form:keuzes:0:button:form:in-focus:hvv:form:postcodeContainer:postcode' and @id='id17']"
postcode_input_xpath = "//button[@class='btn btn-secondary' and @type='submit' and @name='matches:form:keuzes:0:button:form:in-focus:hvv:form:afspraak' and @id='id12']"
quantity_input_xpath = "//button[@class='btn btn-secondary' and @type='submit' and @value='button' and @name='verder' and @id='id1a']"
dates_xpath = "//button[@class='list-group-item list-group-item-action flex-column align-items-start' and @name='keuzes:0:give-focus' and @id='id1f']"
dates_input_xpath = "//button[@class='btn btn-secondary' and @type='submit' and @value='button' and @name='keuzes:0:in-focus:button' and @id='id20']"
calendar_xpart = "//span[@class='input-group-text' and @title='Kies datum ...']"

driver = find_and_click(appointment_xpath)
driver = find_and_click(subject_xpath)
driver = find_and_click(rental_xpath, dropdown=True, dropdown_query="HUUR")
driver = find_and_click(postcode_xpath, textbox=True, textbox_query="3039RL")
driver = find_and_click(postcode_input_xpath)
driver = find_and_click(quantity_input_xpath)
driver = find_and_click(dates_xpath)

# Save date time options screenshot
driver.save_screenshot("options.png")

# Extract and print the filtered text
extract_date_time_text()

driver = find_and_click(dates_input_xpath)
driver = find_and_click(calendar_xpart)

time.sleep(0.5)

# Save calendar screenshot
driver.save_screenshot("calendar.png")

# Don't forget to close the browser when you're done
driver.quit()