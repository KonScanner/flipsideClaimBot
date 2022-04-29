from src.helpers.webdriver_instance import WebDriver
from src.drops import get_drops
import time
import logging
import random


class Flipside(WebDriver):
    def __init__(self, email: str, password: str, headless=False):
        super().__init__(headless=headless)
        self.logged_in = False
        self.discord_login(email=email, password=password)
        self.flipside_login()

    def sleep(self, seconds: int = 0.75) -> None:
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
        return self

    def flipside_login(self):
        self.driver.get("https://flipsidecrypto.xyz/")
        # Sign with discord

        sign_w_disc_path = "/html/body/div/header/div[2]/div/div[2]/form/button"
        authorize_disc = "/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/button[2]"
        try:
            self.driver.find_element_by_xpath(xpath=sign_w_disc_path).click()
            self.sleep(seconds=3)
        except Exception as e:
            raise Exception(e)
        self.sleep(seconds=2)
        self.driver.find_element_by_xpath(xpath=authorize_disc).click()
        self.sleep(seconds=3)
        return self

    def capcha(self):
        s = input("Verified? (y/n)")
        if s.lower() == "y":
            print("Successfully logged in!")
            self.logged_in = True
        return

    def refresh(self, **kwargs):
        self.sleep(**kwargs)
        self.driver.refresh()
        return self

    def _claim_helper(self, url):
        self.driver.get("https://www.google.gr")
        self.sleep(0.16)
        self.driver.get(url)
        self.capcha() if self.logged_in is False else None
        self.sleep(seconds=0.2)
        unclaimed = True
        claim_path = "/html/body/div/div[2]/article/aside/section/div/div[2]/form/button"
        while unclaimed:
            try:
                self.sleep(seconds=0.5)
                self.driver.find_element_by_xpath(claim_path).click()
                unclaimed = False
                self.sleep(seconds=2)
                print(f"Successfully Claimed! {url}")
            except Exception:
                self.refresh(seconds=0.15)
                self.sleep(seconds=3.15)
        return self

    def get_claim(self, url: str):
        self._claim_helper(url)
        logging.info(f"{url} successfully claimed!")
        return self

    def get_claims(self, urls: list, strategy: str = "yield"):
        if urls is None:
            urls = get_drops(strategy=strategy)
            print(urls)
        for url in urls:
            logging.info(f"Claiming {url}...")
            self.get_claim(url)
        return self
