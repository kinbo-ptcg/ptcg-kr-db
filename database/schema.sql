-- ============================================================
-- Korean Pokémon TCG Database Schema
-- ============================================================
-- This schema stores all data for Pokémon card sets released
-- in Korea, scraped from https://pokemoncard.co.kr/cards
-- ============================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- SETS
-- Stores product/set-level information for all Korean releases.
-- Each row represents one product (expansion pack, deck,
-- special set, promo set, etc.)
-- ============================================================
CREATE TABLE IF NOT EXISTS sets (
    code                TEXT    PRIMARY KEY,  -- Product code (e.g. "SV1S", "SM8")
    name                TEXT    NOT NULL,     -- Full Korean product name
    type                TEXT    NOT NULL,     -- "pack" | "deck" | "special" | "promo"
    series              TEXT,                 -- JSON array of series codes, e.g. ["SV"]
    regulations         TEXT,                 -- JSON array of regulation marks, e.g. ["G"]
    in_standard_regu    INTEGER DEFAULT 0,    -- 1 if contains F/G/H regulation cards
    printed_total       TEXT,                 -- Number of cards in base set (string as on card)
    total               INTEGER,             -- Total unique cards including high-rarity variants
    release_date        TEXT,                 -- "YYYY-MM-DD"
    update_date         TEXT,                 -- "YYYY-MM-DD" (last data update)
    price               TEXT,                 -- Korean price text (e.g. "1,000원(1팩)")
    contents            TEXT,                 -- Pack contents description
    caution             TEXT,                 -- Purchase caution text
    prod_url            TEXT,                 -- Official product page URL
    image_symbol_url    TEXT,                 -- Set symbol image URL
    image_cover_url     TEXT                  -- Set box art / cover image URL
);

-- ============================================================
-- CARDS
-- Stores the abstract card definition — the unique combination
-- of stats and effects, regardless of how many times the card
-- has been reprinted.
-- One row = one unique card effect (identified by cardID).
-- ============================================================
CREATE TABLE IF NOT EXISTS cards (
    card_id             TEXT    PRIMARY KEY,  -- Unique card effect ID (cardID field)
    name                TEXT    NOT NULL,     -- Card name (Korean)
    english_name        TEXT,                 -- Card name reconstructed in English (null for Trainers/Energy)
    supertype           TEXT    NOT NULL,     -- "포켓몬" | "트레이너스" | "에너지"
    subtypes            TEXT,                 -- JSON array (e.g. ["기본", "EX"])
    rules               TEXT,                 -- JSON array of rule box texts
    regulation_marks    TEXT,                 -- JSON array of all regulation marks this card has appeared in

    -- Pokémon-only fields
    hp                  INTEGER,             -- Hit Points (null for non-Pokémon)
    type                TEXT,                 -- Energy type notation, e.g. "(풀)" (null for non-Pokémon)
    weakness_type       TEXT,                 -- Weakness energy type (null if none)
    weakness_value      TEXT,                 -- Weakness multiplier (e.g. "×2")
    resistance_type     TEXT,                 -- Resistance energy type (null if none)
    resistance_value    TEXT,                 -- Resistance modifier (e.g. "-20")
    retreat_cost        INTEGER,             -- Number of energies to retreat (null for non-Pokémon)
    flavor_text         TEXT,                 -- Pokédex flavor text (null or empty if not present)

    -- Trainer/Energy-only field
    texts               TEXT                  -- JSON array of card effect text lines (null for Pokémon)
);

-- ============================================================
-- CARD_POKEMONS
-- Pokémon species that appear on a card.
-- One row per Pokémon per card (TAG TEAM cards have 2+ rows).
-- ============================================================
CREATE TABLE IF NOT EXISTS card_pokemons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id         TEXT    NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
    sort_order      INTEGER NOT NULL DEFAULT 0,  -- 0-indexed position on card
    name            TEXT    NOT NULL,            -- Pokémon species name (Korean)
    english_name    TEXT,                        -- Pokémon species name (English), looked up by Pokédex number
    pokedex_number  INTEGER NOT NULL,            -- National Pokédex number (-1 for unknowns)
    region          TEXT,                        -- Regional form prefix, e.g. "가라르" (null if none)
    UNIQUE (card_id, sort_order)
);

-- ============================================================
-- CARD_ATTACKS
-- Attacks listed on a card.
-- One row per attack per card.
-- Unique on (card_id, sort_order) to prevent duplicates when the same
-- abstract card appears in multiple product files.
-- ============================================================
CREATE TABLE IF NOT EXISTS card_attacks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id     TEXT    NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
    sort_order  INTEGER NOT NULL DEFAULT 0,  -- 0-indexed attack order on card
    name        TEXT    NOT NULL,            -- Attack name (Korean)
    cost        TEXT    NOT NULL DEFAULT '', -- Energy cost notation, e.g. "(풀)(무색)"
    damage      TEXT    NOT NULL DEFAULT '', -- Damage value (e.g. "30", "60+", "")
    text        TEXT    NOT NULL DEFAULT '', -- Attack effect text (Korean)
    special     TEXT,                        -- "GX" | "VSTAR" (null if not a special move)
    UNIQUE (card_id, sort_order)
);

-- ============================================================
-- CARD_ABILITIES
-- Abilities / Poké-Powers / Poké-Bodies / Ancient Traits
-- listed on a card.
-- One row per ability per card.
-- Unique on (card_id, sort_order) to prevent duplicates when the same
-- abstract card appears in multiple product files.
-- ============================================================
CREATE TABLE IF NOT EXISTS card_abilities (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id     TEXT    NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
    sort_order  INTEGER NOT NULL DEFAULT 0,  -- 0-indexed ability order on card
    name        TEXT    NOT NULL,            -- Ability name (Korean)
    text        TEXT    NOT NULL DEFAULT '', -- Ability effect text (Korean)
    type        TEXT    NOT NULL,            -- "특성" | "포켓파워" | "포켓바디" | "고대능력" | "테라스탈"
    special     TEXT,                        -- "VSTAR" (null if not special)
    UNIQUE (card_id, sort_order)
);

-- ============================================================
-- CARD_PRINTS
-- Physical print records — one row per unique physical card
-- (i.e. each appearance in a set is a separate print).
-- Multiple prints can share the same card_id (reprints).
-- ============================================================
CREATE TABLE IF NOT EXISTS card_prints (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    print_id        TEXT    NOT NULL UNIQUE,  -- Full print ID, e.g. "SV1S-001"
    card_id         TEXT    NOT NULL REFERENCES cards(card_id) ON DELETE CASCADE,
    set_code        TEXT    REFERENCES sets(code) ON DELETE SET NULL,
    number          TEXT    NOT NULL,         -- Card number within the set, e.g. "001"
    prod_number     TEXT,                     -- Set size printed on card, e.g. "078"
    artist          TEXT,                     -- Illustrator name
    rarity          TEXT,                     -- Rarity code: "C", "U", "R", "RR", "SR", "HR", etc.
    regulation_mark TEXT,                     -- Single regulation mark for this print (e.g. "G")
    card_img_url    TEXT,                     -- Card image URL
    card_page_url   TEXT,                     -- Official card page URL on pokemoncard.co.kr
    prod_symbol_url TEXT                      -- Set symbol image URL for this print
);

-- ============================================================
-- SET_CARDS  (many-to-many join for ordered card list)
-- Associates cards with sets in order, linking the abstract
-- card to its set. Useful for generating set card lists.
-- ============================================================
CREATE TABLE IF NOT EXISTS set_cards (
    set_code    TEXT    NOT NULL REFERENCES sets(code) ON DELETE CASCADE,
    print_id    TEXT    NOT NULL REFERENCES card_prints(print_id) ON DELETE CASCADE,
    sort_order  INTEGER NOT NULL DEFAULT 0,  -- Position in set card list
    PRIMARY KEY (set_code, print_id)
);

-- ============================================================
-- SUPPLY_PRODUCTS
-- Official Pokémon TCG supply products (sleeves, deck boxes,
-- playmats, etc.) released in Korea.
-- ============================================================
CREATE TABLE IF NOT EXISTS supply_products (
    id              INTEGER PRIMARY KEY,
    name            TEXT    NOT NULL,    -- Product name (Korean)
    type            TEXT,                -- Product category (e.g. "supply")
    price           TEXT,                -- Price text in Korean Won
    contents        TEXT,                -- Contents description
    release_date    TEXT,                -- "YYYY-MM-DD"
    cover_url       TEXT,                -- Cover/box image URL
    url             TEXT                 -- Official product page URL
);

-- ============================================================
-- INDEXES for common query patterns
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_cards_supertype       ON cards(supertype);
CREATE INDEX IF NOT EXISTS idx_card_prints_set_code  ON card_prints(set_code);
CREATE INDEX IF NOT EXISTS idx_card_prints_card_id   ON card_prints(card_id);
CREATE INDEX IF NOT EXISTS idx_card_pokemons_card_id ON card_pokemons(card_id);
CREATE INDEX IF NOT EXISTS idx_card_attacks_card_id  ON card_attacks(card_id);
CREATE INDEX IF NOT EXISTS idx_card_abilities_card_id ON card_abilities(card_id);
CREATE INDEX IF NOT EXISTS idx_sets_type             ON sets(type);
CREATE INDEX IF NOT EXISTS idx_sets_release_date     ON sets(release_date);
