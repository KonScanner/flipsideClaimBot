from src.helpers.webdriver_instance import WebDriver
import time
import random


class Flipside(WebDriver):
    def __init__(self, email: str, password: str):
        super().__init__()
        self.discord_login(email=email, password=password)
        self.flipside_login()

    def sleep(self, seconds: int = 0.5) -> None:
        rand_val = random.random()
        time.sleep(seconds + rand_val)

    def discord_login(self, email: str, password: str):
        self.driver.get("https://discord.com/login")
        email_path = '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input'
        password_path = '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input'
        self.sleep()
        self.driver.find_element_by_xpath(email_path).send_keys(email)
        self.sleep()
        self.driver.find_element_by_xpath(xpath=password_path).send_keys(password)
        login_button_path = (
            '//*[@id="app-mount"]/div[2]/div/div/div/div/form/div/div/div[1]/div[2]/button[2]'
        )
        self.sleep()
        self.driver.find_element_by_xpath(xpath=login_button_path).click()
        self.sleep(seconds=2)

    def flipside_login(self):
        self.driver.get("https://flipsidecrypto.xyz/")
        # Sign with discord
        sign_w_disc_path = '//*[@id="desktop-header"]/div/div/nav/ul/li/form/button'
        authorize_disc = "/html/body/div[1]/div[2]/div/div/div/div/div[2]/button[2]"
        self.driver.find_element_by_xpath(xpath=sign_w_disc_path).click()
        self.sleep(seconds=4)
        self.driver.find_element_by_xpath(xpath=authorize_disc).click()
        self.sleep(seconds=2)
        return

    def refresh(self):
        self.sleep(seconds=2.5)
        self.driver.refresh()

    def _claim_helper(url):
        self.driver.get("https://www.google.tk")
        self.sleep(2)
        self.driver.get(url)
        self.sleep(seconds=2)
        unclaimed = True
        claim_path = "/html/body/div/div[2]/article/aside/section/div/div[2]/form/button"
        while unclaimed:
            try:
                self.sleep(seconds=2)
                self.driver.find_element_by_xpath(claim_path).click()
                unclaimed = False
                print(f"Successfully Claimed! {url}")
            except Exception:
                self.refresh()

    def get_claim(self, url: str):
        self._claim_helper(url)

    def get_claims(self, urls: list):
        for url in urls:
            self.get_claim(url)
