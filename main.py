#!/usr/bin/env python3

import configparser
import csv
import pandas as pd
from pathlib import Path
import re

config = configparser.ConfigParser()

config.read("default.ini")
if Path("config.ini").is_file():
    config.read("config.ini")

MISSING_CARD_QUANTITY = 99

df = pd.read_csv(config.get("global", "collection_path")).sort_values(by=["cardcode"])
df.dropna(inplace=True)
df = df.astype({"cardq": int, "cardid": int})
missing_cards_list = []
available_card_list = []
if Path("missing.txt").is_file():
    missing_cards_string = open("missing.txt").read().replace("\n", " ").split()
    missing_cards_list = "|".join([f"{int(x):03d}" for x in missing_cards_string])
if Path("available.txt").is_file():
    available_card_string = open("available.txt").read().replace("\n", " ").split()
    available_card_list = "|".join([f"{int(x):03d}" for x in available_card_string])
if missing_cards_list:
    df.loc[
        df["cardcode"].str.contains(missing_cards_list), "cardq"
    ] = MISSING_CARD_QUANTITY
    print(df[df["cardq"] == MISSING_CARD_QUANTITY])
if available_card_list:
    df["cardq"] = MISSING_CARD_QUANTITY
    df.loc[df["cardcode"].str.contains(available_card_list), "cardq"] = 1
    print(df[df["cardq"] != MISSING_CARD_QUANTITY])
df.to_csv("output.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
Path(config.get("global", "collection_path")).rename(
    re.sub(".csv", "_old.csv", config.get("global", "collection_path"))
)
