from src.helpers.bsoup import get_data
from src.config import PARAMS
import re
import pandas as pd
import logging
import time


def _wait_util(seconds: int) -> None:
    time.sleep(seconds)


def _check_time_left(hours: int, minutes: int, seconds: int) -> bool:
    date_now = pd.to_datetime("now")
    offset = pd.tseries.offsets.DateOffset(hours=hours, minutes=minutes, seconds=seconds)
    deadline = date_now + offset
    seconds = (deadline - date_now).total_seconds()
    return seconds


def check_time_left(data: pd.DataFrame):
    dates = data[data.Live == "Drops"].Date
    if all(dates == dates.iloc[0]):
        date1 = dates.iloc[0]
        res = [int(s) for s in re.findall(r"-?\d+\.?\d*", date1)]
        seconds = _check_time_left(*res)
        return int(seconds)


def _which_strategy(strategy: str, **kwargs) -> str:
    if strategy == "yield":
        return get_highest_yield_drops(**kwargs)
    elif strategy == "first":
        return get_first_four_drops(**kwargs)
    else:
        raise ValueError(
            f"Strategy {strategy} not recognized\nPlease choose from 'yield' or 'first'"
        )


def get_drops(strategy="yield", **kwargs):
    sub_df = _get_terra_bounties_in_asset(get_data())
    seconds = check_time_left(data=sub_df)
    any_live = (sub_df.Live == "Live").any()
    logging.info(f"Time left: {seconds} seconds")
    if seconds > 60 * 5:
        _wait_util(seconds=60)
        get_drops(strategy=strategy, **kwargs)
    elif seconds <= 60 * 5:
        if seconds <= 60:
            if any_live:  # Needs handling
                logging.info(f"Time left: {seconds} seconds, all Live, returning drops...")
                return _which_strategy(strategy)
            else:
                _wait_util(seconds=0.5)
                get_drops(strategy=strategy, **kwargs)
        else:
            _wait_util(seconds=5)
            get_drops(strategy=strategy, **kwargs)
    else:
        raise ValueError("This should have not occured, please check the code")


def _get_terra_bounties_in_asset(data: pd.DataFrame, asset="LUNA") -> pd.DataFrame:
    sub_df = data[
        (data.BountyEcosystem.str.contains("Terra|Anchor", flags=re.IGNORECASE, regex=True))
        & (data.BountyAmount.str.contains(asset))
    ].reset_index(drop=True)
    return sub_df


def get_first_four_drops(**kwargs) -> list:
    df = get_data()
    sub_df = _get_terra_bounties_in_asset(df, **kwargs)
    return [f"{PARAMS.FLIPSIDE_BASE_URL}{i}" for i in sub_df.URL.tolist()]


def get_highest_yield_drops(**kwargs) -> str:
    df = get_data()
    sub_df = _get_terra_bounties_in_asset(df, **kwargs)
    sub_df["Reward"] = sub_df.BountyAmount.apply(lambda x: x[0:4]).astype(float)  # Specific to Luna
    sub_df.sort_values(by=["Reward"], ascending=True, inplace=True)
    subset = sub_df.iloc[sub_df.shape[0] - 4 :]
    return [f"{PARAMS.FLIPSIDE_BASE_URL}{i}" for i in subset.URL.tolist()]


if __name__ == "__main__":
    pass
