from src.flipside import Flipside
from src.helpers.bsoup import get_data
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    headless = False  # Change to True for Dockerized image to work
    d_email = os.getenv("DISCORD_EMAIL")
    d_password = os.getenv("DISCORD_PASSWORD")
    df = get_data()  # To be implemented, for now only for manual use
    flipside_base_url = "https://flipsidecrypto.xyz"
    drops = [
        f"{flipside_base_url}/drops/4x135WJK9pyUkqoJ83H4jQ",
    ]
    # Example
    flipside_claim = Flipside(email=d_email, password=d_password, headless=headless).get_claims(
        urls=drops
    )
