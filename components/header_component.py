from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HeaderComponent:

    PROFILE_AVATAR = (
        By.CSS_SELECTOR,
        "div.v-avatar.cursor-pointer"
    )

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            20
        )

    def is_user_logged_in(self):

        try:

            self.wait.until(
                EC.visibility_of_element_located(
                    self.PROFILE_AVATAR
                )
            )

            return True

        except Exception:

            return False