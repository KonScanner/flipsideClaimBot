from src.flipside import Flipside
from src.helpers.bsoup import get_data
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    d_email = os.getenv("DISCORD_EMAIL")
    d_password = os.getenv("DISCORD_PASSWORD")
    df = get_data()  # To be implemented, for now only for manual use
    flipside_base_url = "https://flipsidecrypto.xyz"
    drops = [
        f"{flipside_base_url}/drops/3qDj4IqbvwuxpDbdubEAdc",
        f"{flipside_base_url}/drops/37jg5GsfeNx3WDsAZE8SNB",
        f"{flipside_base_url}/drops/3K6UmZzIqfGSDo5qFwWQZy",
        f"{flipside_base_url}/drops/3WHHQTFInblqtN83VqWMnl",
    ]
    # Example
    flipside_claim = Flipside(
        email=d_email,
        password=d_password,
    ).get_claims(urls=drops)
