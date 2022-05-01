from src.helpers.webdriver_instance import WebDriver
from src.drops import get_drops
import time
import logging
import random
import re
import numpy as np


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

    def get_body(self) -> list:
        body = self.driver.find_element_by_xpath("/html/body").text
        body = body.split("\n")
        return body

    def claimable(self, body: list, index: int):
        if body[index + 2].lower() == "claim question":
            return True
        if body[index + 1].lower() == "unlimited":
            claims = np.inf
        if body[index + 1][0].lower().isnumeric():
            claims = int(body[index + 1][0])
        if claims <= 0:
            return False
        else:
            return True

    def is_claimed(self, body: list) -> bool:
        body_join = " ".join(body)
        if re.search("Question Claimed", body_join, re.IGNORECASE):
            return True
        else:
            return False

    def refresh(self, **kwargs):
        self.sleep(**kwargs)
        self.driver.refresh()
        return self

    def _claim_helper(self, url: str, persistent=False):
        self.driver.get("https://www.google.gr")
        self.sleep(0.16)
        self.driver.get(url)
        self.capcha() if self.logged_in is False else None
        self.sleep(seconds=0.2)
        body = self.get_body()
        unclaimed = True
        claim_path = "/html/body/div/div[2]/article/aside/section/div/div[2]/form/button"
        while unclaimed:
            body = self.get_body()
            if self.is_claimed(body):
                return self
            claims_index = body.index("Available Claims")
            if self.claimable(body=body, index=claims_index):
                self.driver.find_element_by_xpath(claim_path).click()
                unclaimed = False
                self.sleep(seconds=5.2)
                print(f"Successfully Claimed! {url}")
            else:
                if persistent:
                    self.refresh(seconds=0.15)
                    self.sleep(seconds=3.15)
                else:
                    return self

        return self

    def get_claim(self, url: str, **kwargs):
        self._claim_helper(url, **kwargs)
        logging.info(f"{url} successfully claimed!")
        return self

    def get_claims(self, urls: list, strategy: str = "yield", **kwargs):
        if urls is None:
            urls = get_drops(strategy=strategy)
            print(urls)
        for url in urls:
            logging.info(f"Claiming {url}...")
            self.get_claim(url, **kwargs)
        return self
