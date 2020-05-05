from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.get("https://open.spotify.com/playlist/05mbSA2U0bQ1DqF84eQBBH")

# Get the current number of rows
current_rows_number = len(driver.find_elements_by_xpath('//tr'))
while True:
    # Scroll down to make new XHR (request more table rows)
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    try:
        # Wait until number of rows increased       
        wait(driver, 5).until(lambda: len(driver.find_elements_by_xpath('//tr')) > current_rows_number)
        # Update variable with current rows number
        current_rows_number = len(driver.find_elements_by_xpath('//tr'))
    # If number of rows remains the same after 5 seconds passed, break the loop
    # as there no more rows to receive
    except TimeoutException:
        break

# Now you can scrape the entire table
