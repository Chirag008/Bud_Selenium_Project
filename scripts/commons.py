from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class Common_Utils():
    driver = None

    def __init__(self):
        super()

    def wait_and_get_element(self, driver, locator, by=By.XPATH, timeout=20):
        try:
            element = WebDriverWait(driver=driver, timeout=timeout).until(
                expected_conditions.presence_of_element_located((by, locator)))
        except TimeoutException as te:
            script = None
            if by == By.CLASS_NAME:
                script = 'return document.getElementsByClassName("' + locator + '")[0];'
            elif by == By.ID:
                script = 'return document.getElementById("' + locator + '");'
            elif by == By.TAG_NAME:
                script = 'return document.getElementsByTagName("' + locator + '")[0];'
            elif by == By.XPATH:
                script = 'return document.evaluate("' + locator + '"), document, null,'\
                                                           'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;'
            element = driver.execute_script(script)
            if element is None:
                raise te
        return element

    def get_property_using_js(self, driver: WebDriver, element, property_name='color'):
        script = 'return window.getComputedStyle(arguments[0],null).getPropertyValue("' + property_name + '");'
        value = driver.execute_script(script, element)
        if property_name == 'font-family':
            value = value.split(',')[0][1:-1]
        return value

    def verify(self, actual, exp, errors, message):
        try:
            assert actual == exp
        except AssertionError:
            errors.append(message)

    def is_element_checked(self, driver, element):
        script = 'return arguments[0].checked;'
        return driver.execute_script(script, element)

    @staticmethod
    def get_browser_instance():
        if Common_Utils.driver is None:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            Common_Utils.driver = webdriver.Chrome(executable_path='./drivers/chromedriver.exe', options=options)
        return Common_Utils.driver
