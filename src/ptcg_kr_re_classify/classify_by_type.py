import os
import json
from datetime import datetime
import pprint
import re
import difflib
import bisect

ALL_CARD_DIR = './all_card_data.json'
PRODUCT_INFO_DIR = '../product_info/product_info_cards.json'

def to_four_digit(x):
    if x >= 1000 :
        return str(x)
    elif x >= 100 :
        return "0" + str(x)
    elif x >= 10 :
        return "00" + str(x)
    else :
        return "000" + str(x)

# {4-digit Pokedex number}_{Pokémon name} is called a poke_code
# For TAG TEAM cards, there are multiple Pokémon, so return a list
def get_poke_codes(item):
    pokemons = item['pokemons']
    poke_codes = []

    for pokemon in pokemons:
        poke_codes.append(to_four_digit(pokemon['pokedexNumber']) + '_' + pokemon['name'])

    return poke_codes

def get_pokemon_common(item):
    data = {}

    data['id'] = item['id']
    data['cardID'] = item['cardID']
    data['name'] = item['name']
    data['supertype'] = item['supertype']
    data['subtypes'] = item['subtypes']
    data['rules'] = item['rules']
    data['hp'] = item['hp']
    data['pokemons'] = item['pokemons']
    data['type'] = item['type']
    data['attacks'] = item['attacks']
    data['abilities'] = item['abilities']
    data['weakness'] = item['weakness']
    data['resistance'] = item['resistance']
    data['retreatCost'] = item['retreatCost']
    data['flavorText'] = item['flavorText']  # Updated when a new flavor text version appears
    data['regulationMark'] = [item['regulationMark']]

    return data

def get_pokemon_version(item, debug=3):
    data = {}

    data['number'] = item['number']
    data['prodNumber'] = item['prodNumber']
    data['prodCode'] = item['prodCode']
    data['prodSymbolURL'] = item['prodSymbolURL']
    data['prodName'] = item['prodName']
    data['artist'] = item['artist']
    data['rarity'] = item['rarity']
    data['cardImgURL'] = item['cardImgURL']
    data['cardPageURL'] = item['cardPageURL']
    data['regu'] = item['regulationMark']

    if debug:
        data['debug'] = str(debug)

    return data

def damage_filter(dam):
    return dam.replace('×','').replace('x','').replace('＋','').replace('+','').strip()

def check_same_card(new_item, card_data):
    new_common = get_pokemon_common(new_item)

    is_same_card = True
    diff_key_list = []

    if new_common['name'].replace(' ','') != card_data['name'].replace(' ',''):
        diff_key_list.append('name')
        is_same_card = False
    if new_common['subtypes'] != card_data['subtypes']:
        diff_key_list.append('subtypes')
        is_same_card = False
    if new_common['rules'] != card_data['rules']:
        rule_flag = False
        if len(new_common['rules']) != len(card_data['rules']):
            rule_flag = True
        else:
            for i in range(len(new_common['rules'])):
                if new_common['rules'][i].replace('[','').replace(']','').strip() != card_data['rules'][i].replace('[','').replace(']','').strip():
                    rule_flag = True
        if rule_flag:
            diff_key_list.append('rules')
            is_same_card = False
    if new_common['attacks'] != card_data['attacks']:
        attack_memo = ''
        if len(new_common['attacks']) != len(card_data['attacks']):
            attack_memo += 'len, '
        else:
            for i in range(len(new_common['attacks'])):
                if new_common['attacks'][i]['cost'].strip() != card_data['attacks'][i]['cost'].strip():
                    attack_memo += 'cost, '
                if damage_filter(new_common['attacks'][i]['damage']) != damage_filter(card_data['attacks'][i]['damage']):
                    attack_memo += 'dam, '
                if new_common['attacks'][i]['name'].replace(' ','').strip() != card_data['attacks'][i]['name'].replace(' ','').strip():
                    attack_memo += 'name, '
                if new_common['attacks'][i]['text'].replace(' ','') != card_data['attacks'][i]['text'].replace(' ',''):
                    similarity = difflib.SequenceMatcher(None, new_common['attacks'][i]['text'].replace(' ',''), card_data['attacks'][i]['text'].replace(' ','')).ratio()
                    if similarity < 0.80:
                        attack_memo += 'text' + str(round(similarity, 2)) + ', '
        if attack_memo != '':
            print('att memo : ', attack_memo)
            diff_key_list.append('attacks')
            is_same_card = False
    if new_common['abilities'] != card_data['abilities']:
        abil_memo = ''
        if len(new_common['abilities']) != len(card_data['abilities']):
            abil_memo += 'len, '
        else:
            for i in range(len(new_common['abilities'])):
                if new_common['abilities'][i]['name'].strip() != card_data['abilities'][i]['name'].strip():
                    abil_memo += 'name, '
                if new_common['abilities'][i]['text'].replace(' ','') != card_data['abilities'][i]['text'].replace(' ',''):
                    similarity = difflib.SequenceMatcher(None, new_common['abilities'][i]['text'].replace(' ',''), card_data['abilities'][i]['text'].replace(' ','')).ratio()
                    if similarity < 0.80:
                        abil_memo += 'text' + str(round(similarity, 2)) + ', '
                if new_common['abilities'][i]['type'].strip() != card_data['abilities'][i]['type'].strip():
                    abil_memo += 'type, '
        if abil_memo != '':
            print('abi_memo : ', abil_memo)
            diff_key_list.append('abilities')
            is_same_card = False
    if new_common['weakness'] != card_data['weakness']:
        diff_key_list.append('weakness')
        is_same_card = False
    if new_common['resistance'] != card_data['resistance']:
        diff_key_list.append('resistance')
        is_same_card = False
    if new_common['retreatCost'] != card_data['retreatCost']:
        diff_key_list.append('retreatCost')
        is_same_card = False
    if new_common['regulationMark'] != card_data['regulationMark']:
        diff_key_list.append('regulationMark')
        is_same_card = False

    if not is_same_card:
        new_item_dict = {}
        card_data_dict = {}
        for key in diff_key_list:
            new_item_dict[key] = new_item[key]
            card_data_dict[key] = card_data[key]

        print(diff_key_list)
        print('NEW :: ' + new_item['name'] + ' : ' + new_item['prodName'] + ' : ' + new_item['cardPageURL'])
        pprint.pprint(new_item_dict)
        print(card_data['name'])
        for info in card_data['version_infos']:
            print(info['prodName'] + ' : ' + info['cardPageURL'])
        pprint.pprint(card_data_dict)
        print('============================')

    return is_same_card

def multi_pokemons(item):
    pokemons = item['pokemons']
    if len(pokemons) != 1:
        if 'TAG TEAM' in item['subtypes']:
            return False
        else:
            if pokemons[0]['name'] != '피카츄' and pokemons[0]['name'] != '로토무':
                print('not pika,roto')
                return False
            pprint.pprint(item)
            return True
    return False

def get_trainers_type(item):
    subtypes = item['subtypes']

    if '아이템' in subtypes:
        return '아이템'
    elif '포켓몬의 도구' in subtypes:
        return '포켓몬의_도구'
    elif '스타디움' in subtypes:
        return '스타디움'
    elif ('서포트' in subtypes) or ('서포터' in subtypes):
        return '서포트'
    else:
        print('unknown trainers type')
        return 'unknown'

def get_trainers_common(item):
    data = {}

    data['id'] = item['id']
    data['cardID'] = item['cardID']
    data['name'] = item['name']
    data['supertype'] = item['supertype']
    data['subtypes'] = item['subtypes']
    data['rules'] = item['rules']
    data['texts'] = item['texts']
    if 'attacks' in item:
        data['attacks'] = item['attacks']
    data['regulationMark'] = [item['regulationMark']]

    return data

def get_trainers_version(item):
    return get_pokemon_version(item)

def get_energy_type(item):
    subtypes = item['subtypes']

    if '기본 에너지' in subtypes:
        return '기본_에너지'
    elif '특수 에너지' in subtypes:
        return '특수_에너지'
    else:
        print('unknown energy type')
        return 'unknown'

def get_energy_common(item):
    data = {}

    data['id'] = item['id']
    data['cardID'] = item['cardID']
    data['name'] = item['name']
    data['supertype'] = item['supertype']
    data['subtypes'] = item['subtypes']
    data['rules'] = item['rules']
    data['texts'] = item['texts']
    data['regulationMark'] = [item['regulationMark']]

    return data

def get_energy_version(item):
    data = {}

    data['number'] = item['number']
    data['prodNumber'] = item['prodNumber']
    data['prodCode'] = item['prodCode']
    data['prodSymbolURL'] = item['prodSymbolURL']
    data['prodName'] = item['prodName']
    data['rarity'] = item['rarity']
    data['cardImgURL'] = item['cardImgURL']
    data['cardPageURL'] = item['cardPageURL']

    return data

REGU_DICT = {
    'BE' : 0,
    'DP' : 1,
    'BW' : 2,
    'XY' : 3,
    'A' : 4,
    'B' : 5,
    'C' : 6,
    'D' : 7,
    'E' : 8,
    'F' : 9,
    'G' : 10,
    'H' : 11
}
def add_in_regu_list(regu_list, new_regu):
    if new_regu not in regu_list:
        # Sort regu_list using REGU_DICT values
        key_func = lambda x: REGU_DICT.get(x, float('inf'))
        # Find the sort value of new_regu
        new_regu_value = REGU_DICT.get(new_regu, float('inf'))
        # Find the correct insertion position
        position = bisect.bisect_left([key_func(r) for r in regu_list], new_regu_value)
        # Insert new_regu at that position
        regu_list.insert(position, new_regu)

def classify_cards_by_type():
    pokemon_data, trainers_data, energy_data = {}, {}, {}
    tmp_diff_poke = 0
    multi_pokes = 0

    # Load data
    with open(ALL_CARD_DIR, mode='r', encoding='utf-8') as file:
        all_card_data = json.load(file)

    for item in all_card_data:
        supertype = item['supertype']
        card_id = item['cardID']
        if supertype == '포켓몬':
            poke_codes = get_poke_codes(item)
            for poke_code in poke_codes:
                # Is this Pokémon already stored?
                if poke_code not in pokemon_data:
                    pokemon_item = {}

                    # Common card data
                    pokemon_item[card_id] = get_pokemon_common(item)

                    # Version-specific data; the same card effect may exist in multiple prints (reprints, etc.)
                    # Distinguished by cardID
                    pokemon_item[card_id]['version_infos'] = [get_pokemon_version(item)]

                    pokemon_data[poke_code] = pokemon_item
                else:
                    # Is this cardID already stored for this Pokémon?
                    if card_id not in pokemon_data[poke_code]:
                        # First time seeing this cardID for this Pokémon
                        card_data = get_pokemon_common(item)
                        card_data['version_infos'] = [get_pokemon_version(item, debug=1)]

                        pokemon_data[poke_code][card_id] = card_data

                    else:
                        # Both this Pokémon and cardID have been seen before
                        if pokemon_data[poke_code][card_id]['flavorText'] == "" and item['flavorText'] != "":
                            pokemon_data[poke_code][card_id]['flavorText'] = item['flavorText']

                        # Add new regulation mark if it's new
                        add_in_regu_list(pokemon_data[poke_code][card_id]['regulationMark'], item['regulationMark'])

                        pokemon_data[poke_code][card_id]['version_infos'].append(get_pokemon_version(item, debug=2))

        elif supertype == '트레이너스':
            trainers_type = get_trainers_type(item)
            if trainers_type not in trainers_data:
                trainers_item = {}

                # Common card data
                trainers_item[card_id] = get_trainers_common(item)

                # Version-specific data; the same card effect may exist in multiple prints
                # Distinguished by cardID
                trainers_item[card_id]['version_infos'] = [get_trainers_version(item)]

                trainers_data[trainers_type] = trainers_item
            else:
                if card_id not in trainers_data[trainers_type]:
                    card_data = get_trainers_common(item)
                    card_data['version_infos'] = [get_trainers_version(item)]

                    trainers_data[trainers_type][card_id] = card_data
                else:
                    trainers_data[trainers_type][card_id]['version_infos'].append(get_trainers_version(item))
                    # Add new regulation mark if it's new
                    add_in_regu_list(trainers_data[trainers_type][card_id]['regulationMark'], item['regulationMark'])

        elif supertype == '에너지':
            energy_type = get_energy_type(item)
            if energy_type not in energy_data:
                energy_item = {}

                # Common card data
                energy_item[card_id] = get_energy_common(item)

                # Version-specific data; the same card effect may exist in multiple prints
                # Distinguished by cardID
                energy_item[card_id]['version_infos'] = [get_energy_version(item)]

                energy_data[energy_type] = energy_item
            else:
                if card_id not in energy_data[energy_type]:
                    card_data = get_energy_common(item)
                    card_data['version_infos'] = [get_energy_version(item)]

                    energy_data[energy_type][card_id] = card_data
                else:
                    energy_data[energy_type][card_id]['version_infos'].append(get_energy_version(item))
                    # Add new regulation mark if it's new
                    add_in_regu_list(energy_data[energy_type][card_id]['regulationMark'], item['regulationMark'])

        else:
            print('unknown supertype')

    # Sort version_infos for each cardID by card number and release date
    # e.g. [[num,date]] = [[3,10],[6,5],[1,10]] -> [[6,5],[1,10],[3,10]]

    # Load release date info from product info
    PRODUCT_INFO_DIR = '../product_info/product_info_cards.json'
    with open(PRODUCT_INFO_DIR, mode='r', encoding='utf-8') as file:
        product_info = json.load(file)

    release_date_dict = {}
    for product_item in product_info:
        release_date_dict[product_item['name']] = product_item['releaseDate']

    # Sort Pokémon version_infos
    # pokemon_data[poke_code][card_id]['version_infos']
    for poke_code in pokemon_data:
        for card_id in pokemon_data[poke_code]:
            pokemon_data[poke_code][card_id]['version_infos'] = sorted(pokemon_data[poke_code][card_id]['version_infos'], key=lambda x: datetime.strptime(release_date_dict.get(x['prodName'], '2099-12-31'), "%Y-%m-%d"))

    # Sort Trainer version_infos
    # trainers_data[trainers_type][card_id]['version_infos']
    for trainers_type in trainers_data:
        for card_id in trainers_data[trainers_type]:
            trainers_data[trainers_type][card_id]['version_infos'] = sorted(trainers_data[trainers_type][card_id]['version_infos'], key=lambda x: datetime.strptime(release_date_dict.get(x['prodName'], '2099-12-31'), "%Y-%m-%d"))

    # Sort Energy version_infos
    # energy_data[energy_type][card_id]['version_infos']
    for energy_type in energy_data:
        for card_id in energy_data[energy_type]:
            energy_data[energy_type][card_id]['version_infos'] = sorted(energy_data[energy_type][card_id]['version_infos'], key=lambda x: datetime.strptime(release_date_dict.get(x['prodName'], '2099-12-31'), "%Y-%m-%d"))

    print('object generation done')
    return pokemon_data, trainers_data, energy_data

# Determine generation from Pokedex number
# Meltan and Melmetal are classified as Gen 7
GEN1 = 151   # Mew
GEN2 = 251   # Celebi
GEN3 = 386   # Deoxys
GEN4 = 493   # Arceus
GEN5 = 649   # Genesect
GEN6 = 721   # Volcanion
GEN7 = 809   # Melmetal
GEN8 = 905   # Enamorus
GEN9 = 1025  # Pecharunt
def get_pokedex_gen(num):
    GEN_NUMS = [0, GEN1, GEN2, GEN3, GEN4, GEN5, GEN6, GEN7, GEN8, GEN9]
    for gen in range(1, len(GEN_NUMS)):
        if num <= GEN_NUMS[gen]:
            return gen
    print('Invalid Pokedex number')
    return 0

# Populate card_data/pokemon
POKEMON_DIR = '../../card_data/pokemon/'
def gen_card_data_pokemon(data):
    # Path: POKEMON_DIR/{generation}/{pokedex_number}_{pokemon_name}.json
    with open(PRODUCT_INFO_DIR, mode='r', encoding='utf-8') as file:
        product_info = json.load(file)

    release_date_dict = {}
    for product_item in product_info:
        release_date_dict[product_item['name']] = product_item['releaseDate']

    for poke_code in data:
        # Build file path
        pokedex_num = int(poke_code.split('_')[0])
        pokedex_gen = get_pokedex_gen(pokedex_num)
        file_path = POKEMON_DIR + 'gen' + str(pokedex_gen) + '/' + poke_code + '.json'

        # Save as list in JSON; track first release date for each cardID
        json_data = []
        cid_date_dict = {}
        for card_id in data[poke_code]:
            json_data.append(data[poke_code][card_id])
            cid_date_dict[data[poke_code][card_id]['cardID']] = release_date_dict.get(data[poke_code][card_id]['version_infos'][0]['prodName'], '2099-12-31')

        # Sort by first release date
        json_data = sorted(json_data, key=lambda x: datetime.strptime(release_date_dict.get(x['version_infos'][0]['prodName'], '2099-12-31'), "%Y-%m-%d"))

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    print('pokemon data done')

# Populate card_data/trainers
TRAINERS_DIR = '../../card_data/trainers/'
def gen_card_data_trainers(data):
    # Path: TRAINERS_DIR/{type}.json
    with open(PRODUCT_INFO_DIR, mode='r', encoding='utf-8') as file:
        product_info = json.load(file)

    release_date_dict = {}
    for product_item in product_info:
        release_date_dict[product_item['name']] = product_item['releaseDate']

    for trainers_type in data:
        # Build file path
        file_path = TRAINERS_DIR + trainers_type + '.json'

        # Save as list in JSON; track first release date for each cardID
        json_data = []
        cid_date_dict = {}
        for card_id in data[trainers_type]:
            json_data.append(data[trainers_type][card_id])
            cid_date_dict[data[trainers_type][card_id]['cardID']] = release_date_dict.get(data[trainers_type][card_id]['version_infos'][0]['prodName'], '2099-12-31')

        # Sort by first release date
        json_data = sorted(json_data, key=lambda x: datetime.strptime(release_date_dict.get(x['version_infos'][0]['prodName'], '2099-12-31'), "%Y-%m-%d"))

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    print('trainers done')

# Populate card_data/energy
ENERGY_DIR = '../../card_data/energy/'
def gen_card_data_energy(data):
    # Path: ENERGY_DIR/{type}.json
    with open(PRODUCT_INFO_DIR, mode='r', encoding='utf-8') as file:
        product_info = json.load(file)

    release_date_dict = {}
    for product_item in product_info:
        release_date_dict[product_item['name']] = product_item['releaseDate']

    for energy_type in data:
        # Build file path
        file_path = ENERGY_DIR + energy_type + '.json'

        # Save as list in JSON; track first release date for each cardID
        json_data = []
        cid_date_dict = {}
        for card_id in data[energy_type]:
            json_data.append(data[energy_type][card_id])
            cid_date_dict[data[energy_type][card_id]['cardID']] = release_date_dict.get(data[energy_type][card_id]['version_infos'][0]['prodName'], '2099-12-31')

        # Sort by first release date
        json_data = sorted(json_data, key=lambda x: datetime.strptime(release_date_dict.get(x['version_infos'][0]['prodName'], '2099-12-31'), "%Y-%m-%d"))

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
    print('energy done')

if __name__ == "__main__":
    # Build data objects
    pokemon_data, trainers_data, energy_data = classify_cards_by_type()

    # Populate card_data/pokemon
    gen_card_data_pokemon(pokemon_data)

    # Populate card_data/trainers
    gen_card_data_trainers(trainers_data)

    # Populate card_data/energy
    gen_card_data_energy(energy_data)
