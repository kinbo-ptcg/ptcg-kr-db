# Overview

This repository scrapes the [card search page](https://pokemoncard.co.kr/cards) from the official Korean Pokémon Trading Card Game website and processes the collected data.
Feel free to use this for your services or application development.

If you find any errors in the data, please contact kinkyuboard@gmail.com.

## Changelog

(2024-07-29 ver0.0) Parsing completed from DP Adventure Start through SV Battle Master Deck Charizard ex, Ting-Lu ex

(2024-08-17 ver1.0) Added Night Wanderer card data, added missing data

(2024-08-22 ver1.1) Added missing high-rarity card data

(2024-09-26 ver2.0) Added Stellar Miracle card data, added Night Wanderer high-rarity cards, added missing data, added regulation info to each entry in versions_info in card_data, added code for viewing various statistics (./src/ptcg_kr_re_classify/stats/), and other updates for improved maintainability.

(2024-09-26 ver2.1) Introduced Ultra Beast subtype

# Directory Description

Each directory contains the following information:

- card_data : Detailed card information organized by Pokémon, Trainer type, and Energy
- card_data_product : Detailed card information organized by product/set
- product_data : Detailed product information (release dates, prices, card lists, etc.)
- supply_data : Detailed information on official supply products
- src : Source code and raw data used to generate the above

See the README in each directory root for more detailed explanations.

!!! Warning: Some scripts may not work correctly as the code has been reorganized.

# About cardID

To group cards that have different illustrations and set prints but are functionally identical, a `cardID` system has been introduced.

For non-Pokémon cards, the cardID is simply the card's name.

For Pokémon cards, the rule is:
`{first 2 chars of Pokémon name}{first char of type}{HP (3 digits)}{first 2 chars of first ability name}{first 2 chars of i-th attack name}{damage (3 digits)}` for i = 1 to len(attacks)

There are some cards that do not follow this rule, for the following reasons:
- If cards still cannot be distinguished using the above method, the first 3 characters of the first attack name are used instead.
- There are approximately 20 cards whose stats are completely identical but have different regulation marks in the A, B, and C regulations. For these, the regulation mark is appended at the end.
