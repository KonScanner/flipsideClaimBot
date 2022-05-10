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

    def sleep(self, seconds: float = 0.75) -> None:
        rand_val = random.random()
        time.sleep(seconds + rand_val)

    def refresh(self, **kwargs):
        self.sleep(**kwargs)
        self.driver.refresh()
        return self

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
        return self._login_helper(login_button_path, 2)

    def flipside_login(self):  # sourcery skip: raise-specific-error
        self.driver.get("https://flipsidecrypto.xyz/")
        # Sign with discord

        sign_w_disc_path = "/html/body/div/header/div[2]/div/div[2]/form/button"
        authorize_disc = "/html/body/div[1]/div[2]/div/div/div/div/div/div[2]/button[2]"
        try:
            self.driver.find_element_by_xpath(xpath=sign_w_disc_path).click()
            self.sleep(seconds=3)
        except Exception as e:
            raise Exception(e) from e
        self.sleep(seconds=2)
        return self._login_helper(authorize_disc, 3)

    def _login_helper(self, xpath, seconds):
        self.driver.find_element_by_xpath(xpath=xpath).click()
        self.sleep(seconds=seconds)
        return self

    def capcha(self):
        s = input("Verified? (y/n)")
        if s.lower() == "y":
            print("Successfully logged in!")
            self.logged_in = True
        else:
            self.driver.quit()

    def get_body(self) -> list:
        body = self.driver.find_element_by_xpath("/html/body").text
        body = body.split("\n")
        return body

    def claimable(self, body: list):
        body_join = " ".join(body)
        if re.search("claim question", body_join, re.IGNORECASE):
            print("Claimable, due to 'claim question'...")
            return True
        if re.search("unlimited", body_join, re.IGNORECASE):
            return True
        if re.search("[1-9]+ /", body_join, re.IGNORECASE):
            return True
        if re.search("Drops in", body_join, re.IGNORECASE):
            return self._helper_for_claimable(seconds=0.5)
        if re.search("error", body_join, re.IGNORECASE):
            return self._helper_for_claimable(seconds=0.25)
        if re.search("uh oh", body_join, re.IGNORECASE):
            return self._helper_for_claimable(seconds=0.25)
        print("Not claimable...")
        return False

    def _helper_for_claimable(self, **kwargs):
        self.refresh(**kwargs)
        body = self.get_body()
        return self.claimable(body=body)

    def is_claimed(self, body: list) -> bool:
        body_join = " ".join(body)
        return bool(re.search("Question Claimed", body_join, re.IGNORECASE))

    def _get_index_available_claims(self, body: list) -> int:
        body_join = " ".join(body)
        if re.search("available", body_join, re.IGNORECASE):
            return body.index("Available Claims")
        self.refresh(seconds=0.15)
        body = self.get_body()
        return self._get_index_available_claims(body=body)

    def _claim_helper(self, url: str, persistent: bool = False):
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
            # claims_index = self._get_index_available_claims(body=body)
            if self.claimable(body=body):
                self.driver.find_element_by_xpath(claim_path).click()
                self.sleep(seconds=3.25)
                body = self.get_body()
                if self.is_claimed(body):
                    unclaimed = False
                    print(f"Successfully Claimed! {url}")
                    return self
            elif persistent:
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
