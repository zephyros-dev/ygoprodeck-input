#!/usr/bin/env python3

import pandas as pd

MISSING_CARD_QUANTITY = 99

df = pd.read_csv("collection.csv").sort_values(by=["cardcode"])
missing_cards_string = open("missing.txt").read().replace("\n", " ").split()
missing_cards_list = [f"{int(x):03d}" for x in missing_cards_string]
for missing_card in missing_cards_list:
    df.loc[df["cardcode"].str.contains(missing_card), "cardq"] = MISSING_CARD_QUANTITY
print(df[df["cardq"] == MISSING_CARD_QUANTITY])
df.to_csv("output.csv", index=False)
