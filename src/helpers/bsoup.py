import requests
import bs4
import re
import pandas as pd

url = "https://flipsidecrypto.xyz/"


def get_html(url):
    r = requests.get(url)
    return r.text


def parse_html(html):
    soup = bs4.BeautifulSoup(html, "html.parser")
    return soup


def get_data():
    html = get_html(url)
    soup = parse_html(html)
    lists = [i for i in soup.findAll("li")]
    bounty_ecosys = [
        i.findAll("p", {"class": "font-semibold"})[0].text
        if len(i.findAll("p", {"class": "font-semibold"})) > 0
        else None
        for i in lists
    ]
    bounty_amount = [
        i.findAll("p", {"class": "font-semibold"})[1].text
        if len(i.findAll("p", {"class": "font-semibold"})) > 0
        else None
        for i in lists
    ]
    live_or_not = [
        i.findAll("p", {"class": "text-sm text-right"})[0].text
        if len(i.findAll("p", {"class": "text-sm text-right"})) > 0
        else None
        for i in lists
    ]
    claims_status = [
        i.findAll("p", {"class": "text-sm"})[0].text
        if len(i.findAll("p", {"class": "text-sm"})) > 0
        else None
        for i in lists
    ]
    claims = [
        i.findAll("span", {"class": "font-semibold text-sm text-zinc-400"})[0].text
        if len(i.findAll("span", {"class": "font-semibold text-sm text-zinc-400"})) > 0
        else None
        for i in lists
    ]
    date = [
        i.findAll(
            "span",
            {"class": "text-sm text-white font-bold font-inter"},
        )[0].text
        if len(
            i.findAll(
                "span",
                {"class": "text-sm text-white font-bold font-inter"},
            )
        )
        > 0
        else i.findAll(
            "span",
            {
                "class": (
                    "text-sm text-white font-bold text-transparent bg-clip-text bg-gradient-to-r"
                    " from-[#03FFFF] via-[#7449F3] to-[#9A0EEF] font-inter"
                )
            },
        )[0].text
        if len(
            i.findAll(
                "span",
                {
                    "class": (
                        "text-sm text-white font-bold text-transparent bg-clip-text"
                        " bg-gradient-to-r from-[#03FFFF] via-[#7449F3] to-[#9A0EEF] font-inter"
                    )
                },
            )
        )
        > 0
        else None
        for i in lists
    ]
    #

    hrefs = [i.findAll("a", href=True) if len(i) > 0 else None for i in lists]
    hrefs_ = []
    for i in hrefs:
        try:
            hrefs_.append(i[0].get("href"))
        except IndexError:
            hrefs_.append(None)
    hrefs = hrefs_
    df = pd.DataFrame(
        {
            "Date": date,
            "BountyEcosystem": bounty_ecosys,
            "BountyAmount": bounty_amount,
            "Live": live_or_not,
            "ClaimsStatus": claims_status,
            "Claims": claims,
            "URL": hrefs,
        }
    )
    df = df[~df.BountyEcosystem.isna()].reset_index(drop=True)
    return df


if __name__ == "__main__":
    df = get_data()
