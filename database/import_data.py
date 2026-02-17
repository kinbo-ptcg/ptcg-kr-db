"""
import_data.py
=============
Imports all existing Korean PTCG JSON data into a SQLite database.

Usage:
    python import_data.py [--db PATH] [--reset]

    --db PATH   Path to the SQLite database file (default: ptcg_kr.db)
    --reset     Drop and recreate all tables before importing

Data sources read:
    ../product_data/           - Set/product metadata (release dates, prices, etc.)
    ../card_data_product/      - Per-set card lists (one card per entry)
    ../supply_data/product_info_supp.json  - Supply product info
"""

import os
import sys
import json
import sqlite3
import argparse
from pathlib import Path

# Allow importing pokemon_names_en from the same directory as this script
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pokemon_names_en import POKEDEX_EN, REGION_PREFIX_EN, NAME_PREFIX_EN, NAME_SUFFIX_EN

# ── paths ──────────────────────────────────────────────────────────────────────
REPO_ROOT        = Path(__file__).resolve().parent.parent
SCHEMA_FILE      = Path(__file__).resolve().parent / "schema.sql"
PRODUCT_DATA_DIR = REPO_ROOT / "product_data"
CARD_DATA_DIR    = REPO_ROOT / "card_data_product"
SUPPLY_DATA_FILE = REPO_ROOT / "supply_data" / "product_info_supp.json"

DEFAULT_DB_PATH  = Path(__file__).resolve().parent / "ptcg_kr.db"


# ── helpers ────────────────────────────────────────────────────────────────────

def json_dumps(obj):
    """Serialize a Python object to a compact JSON string, or return None."""
    if obj is None:
        return None
    return json.dumps(obj, ensure_ascii=False)


def build_english_card_name(card: dict) -> "str | None":
    """
    Reconstruct an English card name for Pokémon cards using the Pokédex
    number → English name mapping and known prefix/suffix tokens.
    Returns None for Trainer and Energy cards.

    Examples:
      "리자몽 EX"        → "Charizard EX"
      "M 리자몽 EX"      → "Mega Charizard EX"
      "원시 가이오가 EX"  → "Primal Kyogre EX"
      "히스이 조로아크 V" → "Hisuian Zoroark V"
      "피카츄 & 꼬부기 GX" → "Pikachu & Squirtle GX"
    """
    if card.get("supertype") != "포켓몬":
        return None

    pokemons = card.get("pokemons") or []
    if not pokemons:
        return None

    kr_name = card.get("name", "")
    kr_tokens = kr_name.split()

    # Build the per-species English name (with regional prefix if present)
    species_parts = []
    for poke in pokemons:
        dex_num = poke.get("pokedexNumber", -1)
        species_en = POKEDEX_EN.get(dex_num)
        if not species_en:
            # Dex number unknown — fall back to the Korean name verbatim
            species_parts.append(poke.get("name", ""))
            continue

        region = poke.get("region")
        if region and region in REGION_PREFIX_EN:
            species_parts.append(f"{REGION_PREFIX_EN[region]} {species_en}")
        else:
            species_parts.append(species_en)

    # TAG TEAM and multi-Pokémon cards use " & " between species
    base_name = " & ".join(species_parts)

    # Find a non-regional card-name prefix token (e.g. "M", "원시", "찬란한")
    prefix = ""
    for token in kr_tokens:
        if token in NAME_PREFIX_EN:
            prefix = NAME_PREFIX_EN[token]
            break

    # Find the mechanic suffix (e.g. "EX", "GX", "VMAX") from the end
    suffix = ""
    for token in reversed(kr_tokens):
        if token in NAME_SUFFIX_EN:
            suffix = NAME_SUFFIX_EN[token]
            break

    parts = []
    if prefix:
        parts.append(prefix)
    parts.append(base_name)
    if suffix:
        parts.append(suffix)

    return " ".join(parts)


def open_db(db_path: Path, reset: bool = False) -> sqlite3.Connection:
    """Open (or create) the SQLite database, apply the schema, and return the connection."""
    if reset and db_path.exists():
        print(f"Resetting database: deleting {db_path}")
        db_path.unlink()

    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys=ON;")

    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
    conn.executescript(schema_sql)
    conn.commit()
    return conn


# ── set import ─────────────────────────────────────────────────────────────────

def import_sets(conn: sqlite3.Connection) -> int:
    """
    Load all product metadata from product_data/ subdirectories and insert into the
    'sets' table. Returns the total number of sets imported.
    """
    count = 0
    cur = conn.cursor()

    for subdir in PRODUCT_DATA_DIR.iterdir():
        if not subdir.is_dir():
            continue
        for json_file in subdir.glob("*.json"):
            with open(json_file, encoding="utf-8") as f:
                products = json.load(f)

            for p in products:
                # card_list_index and card_list_detail are not stored in the sets table
                cur.execute("""
                    INSERT OR REPLACE INTO sets
                        (code, name, type, series, regulations, in_standard_regu,
                         printed_total, total, release_date, update_date,
                         price, contents, caution, prod_url,
                         image_symbol_url, image_cover_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.get("code"),
                    p.get("name"),
                    p.get("type"),
                    json_dumps(p.get("series")),
                    json_dumps(p.get("regulations")),
                    1 if p.get("in_standard_regu") else 0,
                    p.get("printed_total"),
                    p.get("total"),
                    p.get("release_date"),
                    p.get("update_date"),
                    p.get("price"),
                    p.get("contents"),
                    p.get("caution"),
                    p.get("prod_url"),
                    p.get("image_symbol_url"),
                    p.get("image_cover_url"),
                ))
                count += 1

    conn.commit()
    return count


# ── supply import ──────────────────────────────────────────────────────────────

def import_supply_products(conn: sqlite3.Connection) -> int:
    """
    Load official supply product data and insert into the 'supply_products' table.
    Returns the number of supply products imported.
    """
    if not SUPPLY_DATA_FILE.exists():
        print(f"Supply data file not found: {SUPPLY_DATA_FILE}")
        return 0

    with open(SUPPLY_DATA_FILE, encoding="utf-8") as f:
        supplies = json.load(f)

    cur = conn.cursor()
    count = 0
    for s in supplies:
        cur.execute("""
            INSERT OR REPLACE INTO supply_products
                (id, name, type, price, contents, release_date, cover_url, url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s.get("id"),
            s.get("name"),
            s.get("type"),
            s.get("price"),
            s.get("contents"),
            s.get("releaseDate"),
            s.get("cover_url"),
            s.get("url"),
        ))
        count += 1

    conn.commit()
    return count


# ── card import ────────────────────────────────────────────────────────────────

def import_card(conn: sqlite3.Connection, card: dict, set_code: str) -> None:
    """
    Insert a single card JSON object into the cards, card_pokemons, card_attacks,
    card_abilities, card_prints, and set_cards tables.
    """
    cur = conn.cursor()

    card_id  = card.get("cardID") or card.get("id", "")
    name     = card.get("name", "")
    supertype = card.get("supertype", "")

    # ── cards table ────────────────────────────────────────────────────────────
    weakness   = card.get("weakness", {}) or {}
    resistance = card.get("resistance", {}) or {}

    # regulation_marks is a list in card_data but a single string in raw card data
    regu_marks = card.get("regulationMark")
    if isinstance(regu_marks, list):
        regu_marks_json = json_dumps(regu_marks)
    elif isinstance(regu_marks, str):
        regu_marks_json = json_dumps([regu_marks]) if regu_marks else json_dumps([])
    else:
        regu_marks_json = json_dumps([])

    english_name = build_english_card_name(card)

    cur.execute("""
        INSERT OR IGNORE INTO cards
            (card_id, name, english_name, supertype, subtypes, rules, regulation_marks,
             hp, type, weakness_type, weakness_value, resistance_type, resistance_value,
             retreat_cost, flavor_text, texts)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        card_id,
        name,
        english_name,
        supertype,
        json_dumps(card.get("subtypes")),
        json_dumps(card.get("rules")),
        regu_marks_json,
        card.get("hp"),
        card.get("type"),
        weakness.get("type") or None,
        weakness.get("value") or None,
        resistance.get("type") or None,
        resistance.get("value") or None,
        card.get("retreatCost"),
        card.get("flavorText") or None,
        json_dumps(card.get("texts")),
    ))

    # ── card_pokemons ──────────────────────────────────────────────────────────
    pokemons = card.get("pokemons") or []
    for idx, poke in enumerate(pokemons):
        dex_num = poke.get("pokedexNumber", -1)
        poke_en = POKEDEX_EN.get(dex_num)
        cur.execute("""
            INSERT OR IGNORE INTO card_pokemons
                (card_id, sort_order, name, english_name, pokedex_number, region)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            card_id,
            idx,
            poke.get("name", ""),
            poke_en,
            dex_num,
            poke.get("region"),
        ))

    # ── card_attacks ───────────────────────────────────────────────────────────
    attacks = card.get("attacks") or []
    for idx, atk in enumerate(attacks):
        cur.execute("""
            INSERT OR IGNORE INTO card_attacks
                (card_id, sort_order, name, cost, damage, text, special)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            card_id,
            idx,
            atk.get("name", ""),
            atk.get("cost", ""),
            atk.get("damage", ""),
            atk.get("text", ""),
            atk.get("special"),
        ))

    # Single attack on attack-tool Trainer cards (stored under 'attack' key)
    attack_single = card.get("attack")
    if attack_single and not attacks:
        cur.execute("""
            INSERT OR IGNORE INTO card_attacks
                (card_id, sort_order, name, cost, damage, text, special)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            card_id,
            0,
            attack_single.get("name", ""),
            attack_single.get("cost", ""),
            attack_single.get("damage", ""),
            attack_single.get("text", ""),
            attack_single.get("special"),
        ))

    # ── card_abilities ─────────────────────────────────────────────────────────
    abilities = card.get("abilities") or []
    for idx, abi in enumerate(abilities):
        cur.execute("""
            INSERT OR IGNORE INTO card_abilities
                (card_id, sort_order, name, text, type, special)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            card_id,
            idx,
            abi.get("name", ""),
            abi.get("text", ""),
            abi.get("type", ""),
            abi.get("special"),
        ))

    # ── card_prints ────────────────────────────────────────────────────────────
    print_id = card.get("id", "")
    regu_mark_single = card.get("regulationMark")
    if isinstance(regu_mark_single, list):
        regu_mark_single = regu_mark_single[0] if regu_mark_single else None

    cur.execute("""
        INSERT OR IGNORE INTO card_prints
            (print_id, card_id, set_code, number, prod_number, artist,
             rarity, regulation_mark, card_img_url, card_page_url, prod_symbol_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        print_id,
        card_id,
        set_code,
        card.get("number", ""),
        card.get("prodNumber"),
        card.get("artist"),
        card.get("rarity"),
        regu_mark_single,
        card.get("cardImgURL"),
        card.get("cardPageURL"),
        card.get("prodSymbolURL"),
    ))

    # ── set_cards ──────────────────────────────────────────────────────────────
    try:
        sort_order = int(card.get("number", "0"))
    except (ValueError, TypeError):
        sort_order = 0

    cur.execute("""
        INSERT OR IGNORE INTO set_cards (set_code, print_id, sort_order)
        VALUES (?, ?, ?)
    """, (set_code, print_id, sort_order))


def import_cards(conn: sqlite3.Connection) -> int:
    """
    Walk all card_data_product/ subdirectories, load each set's card JSON file,
    and insert all cards into the database.
    Returns the total number of card prints imported.
    """
    total = 0

    for subdir in sorted(CARD_DATA_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        product_type = subdir.name  # "pack", "deck", "special", "promo", etc.

        for item in sorted(subdir.iterdir()):
            if item.is_dir():
                # Has a series subdirectory (e.g. pack/SV/)
                series_dir = item
                for json_file in sorted(series_dir.glob("*.json")):
                    set_code = json_file.stem  # filename without extension = set code
                    with open(json_file, encoding="utf-8") as f:
                        cards = json.load(f)
                    for card in cards:
                        import_card(conn, card, set_code)
                        total += 1
            elif item.suffix == ".json":
                # Flat JSON file directly under product_type (e.g. promo/SV-P.json)
                set_code = item.stem
                with open(item, encoding="utf-8") as f:
                    cards = json.load(f)
                for card in cards:
                    import_card(conn, card, set_code)
                    total += 1

    conn.commit()
    return total


# ── main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Import Korean PTCG JSON data into a SQLite database."
    )
    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB_PATH),
        help=f"Path to the SQLite database file (default: {DEFAULT_DB_PATH})",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Drop and recreate all tables before importing",
    )
    args = parser.parse_args()

    db_path = Path(args.db)
    print(f"Database: {db_path}")
    print(f"Reset:    {args.reset}")
    print()

    conn = open_db(db_path, reset=args.reset)

    print("Importing sets...")
    n_sets = import_sets(conn)
    print(f"  → {n_sets} sets imported")

    print("Importing supply products...")
    n_supply = import_supply_products(conn)
    print(f"  → {n_supply} supply products imported")

    print("Importing cards...")
    n_cards = import_cards(conn)
    print(f"  → {n_cards} card prints imported")

    # Summary
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sets;")
    print(f"\nDatabase summary:")
    print(f"  sets:             {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM cards;")
    print(f"  unique cards:     {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM card_prints;")
    print(f"  card prints:      {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM card_attacks;")
    print(f"  attacks:          {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM card_abilities;")
    print(f"  abilities:        {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM card_pokemons;")
    print(f"  pokémon entries:  {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM supply_products;")
    print(f"  supply products:  {cur.fetchone()[0]}")

    conn.close()
    print(f"\nDone. Database written to: {db_path}")


if __name__ == "__main__":
    main()
