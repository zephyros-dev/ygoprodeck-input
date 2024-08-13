#!/usr/bin/env python3

import configparser
import csv
import re
from pathlib import Path

import pandas as pd

config = configparser.ConfigParser()

config.read("default.ini")
if Path("config.ini").is_file():
    config.read("config.ini")

AVAILABLE_CARD_QUANTITY = 1
MISSING_CARD_QUANTITY = 99

df = pd.read_csv(config.get("global", "collection_path")).sort_values(by=["cardcode"])
df.dropna(inplace=True)
df = df.astype({"cardq": int, "cardid": int})

if Path("missing.txt").is_file() and Path("available.txt").is_file():
    print("Both missing and available card lists are present. Please remove one.")
    exit()
elif Path("missing.txt").is_file():
    action = "missing"
elif Path("available.txt").is_file():
    action = "available"
else:
    print("No missing or available card list found.")
    exit()

cards_raw_list = open(f"{action}.txt").read().replace("\n", " ").split()
cards_string_list = []
for card in cards_raw_list:
    if "-" in card:
        start, end = card.split("-")
        for i in range(int(start), int(end) + 1):
            cards_string_list.append(f"{int(i):03d}")
    else:
        cards_string_list.append(f"{int(card):03d}")
cards_df_string = "|".join([card for card in cards_string_list])

if action == "missing":
    quantity_init = AVAILABLE_CARD_QUANTITY
    quantity_to_change = MISSING_CARD_QUANTITY
if action == "available":
    quantity_init = MISSING_CARD_QUANTITY
    quantity_to_change = AVAILABLE_CARD_QUANTITY

df["cardq"] = quantity_init
df.loc[df["cardcode"].str.contains(cards_df_string), "cardq"] = quantity_to_change

print(df[df["cardq"] == quantity_to_change])
print("Total cards:", df.shape[0])
if len(cards_string_list) != df[df["cardq"] == quantity_to_change].shape[0]:
    print("Cards in the missing list but not in the collection:")
    missing_card_input = set(
        (df[df["cardq"] == quantity_to_change]["cardcode"]).transform(
            lambda x: re.search(r"\d\d\d", x).group(0)
        )
    )
    print(set(cards_string_list) - missing_card_input)
    print(
        "Seems like cards is missing from collection. Ask the ygoprodeck admin to check the import set function."
    )
else:
    print("All cards in the list were updated. Saving...")
    df.to_csv("output.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)
    Path(config.get("global", "collection_path")).rename(
        re.sub(".csv", "_old.csv", config.get("global", "collection_path"))
    )
    print("Saving completed")
