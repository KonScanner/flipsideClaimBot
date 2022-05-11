from src.flipside import Flipside
from src.helpers.bsoup import get_data
from dotenv import load_dotenv
import os
import sys
import re
import logging

if __name__ == "__main__":
    load_dotenv()
    headless = False  # Change to True for Dockerized image to work
    d_email = os.getenv("DISCORD_EMAIL")
    d_email2 = os.getenv("DISCORD_EMAIL2")
    d_password = os.getenv("DISCORD_PASSWORD")
    d_password2 = os.getenv("DISCORD_PASSWORD2")
    df = get_data()  # To be implemented, for now only for manual use
    drops = ["https://flipsidecrypto.xyz/drops/2GKV028SZCBkuod8RKDy9i"]
    # idx = 0
    # Example
    if len(sys.argv) > 1:
        logging.basicConfig(filename=f"flipside_logs_{sys.argv[1]}.log", level=logging.INFO)
        if len(sys.argv) > 2 and re.search("headless", sys.argv[2], re.IGNORECASE):
            headless = True
            if len(sys.argv) > 3:
                idx = int(sys.argv[3])
        if sys.argv[1] == "1":
            flipside_claim = Flipside(
                email=d_email, password=d_password, headless=headless
            ).get_claims(urls=drops, strategy="yield", persistent=False)
        elif sys.argv[1] == "2":
            flipside_claim2 = Flipside(
                email=d_email2, password=d_password2, headless=headless
            ).get_claims(urls=drops, strategy="first", persistent=False)
        else:
            raise ValueError("Please choose from 1 or 2")
