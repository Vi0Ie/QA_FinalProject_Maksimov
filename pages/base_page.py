from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException
)

from selenium.webdriver.common.action_chains import (
    ActionChains
)


class BasePage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):

        self.driver.get(url)

    def click(self, locator):

        element = self.wait.until(
            EC.presence_of_element_located(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        self.wait.until(
            EC.visibility_of(element)
        )

        try:

            self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            element.click()

        except (
                TimeoutException,
                ElementClickInterceptedException
        ):

            ActionChains(self.driver) \
                .move_to_element(element) \
                .pause(0.5) \
                .click() \
                .perform()

    def type(self, locator, text):

        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )

        element.clear()
        element.send_keys(text)

    def get_text(self, locator):

        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    def wait_for_element(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )