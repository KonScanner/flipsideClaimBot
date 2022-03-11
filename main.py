from src.flipside import Flipside
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    d_email = os.getenv("DISCORD_EMAIL")
    d_password = os.getenv("DISCORD_PASSWORD")
    # Example
    flipside_claim = Flipside(
        email=d_email,
        password=d_password,
    ).get_claim(url="https://flipsidecrypto.xyz/drops/4x135WJK9pyUkqoJ83H4jQ")
