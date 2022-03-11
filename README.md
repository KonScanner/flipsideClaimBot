# Flipside Claim Bot

A bot made to claim flipside bounties, for whenever you do not have the time to perform the task manually.

Flipside has made it harder and harder for people to use bots in order to claim the bounties. Now only releasing the actual links when the time comes.

## How to use

- Create `.env` with your credentials.

```
DISCORD_EMAIL=example@example.io
DISCORD_PASSWORD=examplePassW0rd
```

- Create virtual environment and install requirements

```sh
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

- Give the bot a url to claim (for now)

```python
# Change this
drops = [
        f"{flipside_base_url}/drops/drop_HASH_1251257192",
        f"{flipside_base_url}/drops/drop_HASH_12512162122"
    ]
```

- Start the bot:

```sh
python3 main.py
```

## Next steps

Find a way to grab the links from the bounties as soon as they launch and do an auto-claim for only the ones that the user may be interested in. i.e. using the `denom` they're paying out in.

## Contributing

Fork, change and submit a pull request. As long as it fits with the "Next steps" it will most probably be accepted
