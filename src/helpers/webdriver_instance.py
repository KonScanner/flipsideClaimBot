from src.config import Config
from selenium import webdriver
import time as t
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class WebDriver:
    def __init__(self, headless=True):
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=Config(headless=headless).options
        )
        self.driver.maximize_window()

    def __exit__(self):
        self.driver.quit()
