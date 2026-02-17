import os
import json
from datetime import datetime
import pprint
import re

# Goals of this script:
# 1. Split products into pack, deck, and special categories based on product_info_cards.json,
#    and collect the cards contained in each product.
#    Result: card_data/[pack,deck,special]/[series]/[product_code].json
#    ?? Is each product only covered by one file?
#    ?? Let's check first.
#    !! Confirmed!!
# Exceptions:
# - Sun & Moon Reinforcement Expansion Pack "GX Battle Boost REMASTER"
# - Sun & Moon Promo Card Key Stick Pokémon
############################################################
# Fields to populate:
#   1. num_conti : whether item['number'] is continuous from 1 to end
# 2. More detailed product info including card list
#       product_info/[pack,deck,special]/[series]/[product_code].json
#           1. num_max : largest item['number']
#           2. prod_num : number of card types
#           3. prod_code : e.g. bw2
#           4. prod_smb_url : set symbol image
#           5. name : product name
#           6. prod_info : info from the product_info_cards.json file
# 3. Split card files by Pokémon -> handled in a separate file
#       product_info/[gen]/[dexnum_pokemon].json

ALL_CARD_DIR = './all_card_data.json'
PRODUCT_INFO_DIR = '../product_info/product_info_cards.json'

# From dict_list, return item[target_key] where item[search_key] == search_ele
EXCEPTION_PRODNAME_DICT = {
    'BW 「플라스마단 덱」' : '포켓몬 카드 게임 BW 「플라스마단 스페셜 세트」',
    'BW 「케르디오 덱」' : '포켓몬 카드 게임 BW 트레이너 세트 「케르디오」'
}

def search_in_dict_list(dict_list, search_key, search_ele, target_key):
    if search_ele in EXCEPTION_PRODNAME_DICT:
        search_ele = EXCEPTION_PRODNAME_DICT[search_ele]

    result = [item[target_key] for item in dict_list if item.get(search_key) == search_ele]

    if result:
        return result[0]
    else:
        if 'DP' not in search_ele:
            print(search_key, search_ele, target_key)
        return target_key + " not found"

# DP products have no product info
def get_type(product_info, item):
    type_ = search_in_dict_list(product_info, 'name', item['prodName'].strip(), 'type')
    if "not found" in type_:
        if "DP" in item['prodName']:
            if "확장팩" in item['prodName']:
                type_ = 'pack'
            elif "덱" in item['prodName']:
                type_ = 'deck'

    return type_

def get_series(item):
    SM_regus = ['A','B','C']
    S_regus = ['D','E','F']
    SV_regus = ['G','H']

    item_regu = item['regulationMark']

    if item_regu == 'DP':
        return ['DP']
    elif item_regu == 'BW':
        return ['BW']
    elif item_regu == 'XY':
        return ['XY']
    elif item_regu in SM_regus:
        return ['SM']
    elif item_regu in S_regus:
        return ['S']
    elif item_regu in SV_regus:
        return ['SV']
    else:  # Only BE (basic energy) remains
        return []

def is_promo(item):
    non_promo_keywords = ['BS','ST']
    if any(key in item["cardPageURL"] for key in non_promo_keywords):
        return False
    else:
        return True

def is_stan_regu(item):
    stan_regus = ['F','G','H']
    item_regu = item['regulationMark']

    if item_regu in stan_regus:
        return True
    else:
        return False

# card_list_detail = [objs] - Summary of cards included in the product:
#   num : card number
#   prod_num : number of card types in product
#   name : card name
#   supertype : card category
#   subtypes : card sub-categories
#   type : (for Pokémon) type
#   pokemons : (for Pokémon) list of Pokémon
#   rarity : rarity
#   regulation : regulation mark
def summary_card_data(item):
    card_item = {}

    card_item['num'] = item['number']
    card_item['prod_num'] = item["prodNumber"]
    card_item['name'] = item['name']
    card_item['supertype'] = item['supertype']
    card_item['subtypes'] = item['subtypes']

    if item['supertype'] == '포켓몬':
        card_item['type'] = item['type']
        card_item['pokemons'] = item['pokemons']

    card_item['rarity'] = item['rarity']
    card_item['regulation'] = item["regulationMark"]

    return card_item

def get_promo_code(item):
    series = get_series(item)
    if series:
        return get_series(item)[0] + '-P'
    else:
        return item["prodNumber"]

def set_regu_list(item, empty=False, regu_list=[]):
    regu = item['regulationMark']
    if empty:
        if regu != 'BE':
            return [item['regulationMark']]
        else:
            return []
    else:
        if regu != 'BE':
            return list(set(regu_list) | set([item['regulationMark']]))
        else:
            return regu_list


def classify_cards_by_product():
    product_info_extended = {}

    # Load data
    with open(ALL_CARD_DIR, mode='r', encoding='utf-8') as file:
        all_card_data = json.load(file)
    with open(PRODUCT_INFO_DIR, mode='r', encoding='utf-8') as file:
        product_info = json.load(file)

    # Fields per product:
    # code : product code
    # name : product name
    # type : product type

    # printed_total : number of card types (printed total)
    # total : total card types including high-rarity variants

    # series : series info for cards in this product
    # regulations : regulation marks for cards in this product
    # in_standard_regu : whether product contains any F/G/H regulation cards

    # release_date : release date
    # update_date : last updated date

    # price : pricing info
    # contents : product contents description
    # caution : purchase caution notes

    # prod_url : product page URL
    # image_symbol_url : product symbol image URL
    # image_cover_url : product cover image URL

    # card_list_index = [indexes] - indices of cards in all_card_data.json
    # card_list_detail = [objs] - summary of cards included in this product
    #   num : card number
    #   prod_num : number of card types in product
    #   name : card name
    #   supertype : card category
    #   subtypes : card sub-categories
    #   type : (for Pokémon) type
    #   pokemons : (for Pokémon) list of Pokémon
    #   rarity : rarity
    #   regulation : regulation mark

    for index in range(len(all_card_data)):
        item = all_card_data[index]
        code = item['prodCode']
        if is_promo(item):
            code = get_promo_code(item)
            if code not in product_info_extended:
                product_item = {}
                product_item['code'] = code
                product_item['name'] = item['prodName']
                product_item['type'] = 'promo'

                product_item['printed_total'] = item['prodNumber']
                product_item['total'] = 1

                product_item['series'] = get_series(item)
                product_item['regulations'] = set_regu_list(item, empty=True)
                product_item['in_standard_regu'] = is_stan_regu(item)

                product_item['release_date'] = ''
                product_item['update_date'] = datetime.now().strftime("%Y-%m-%d")

                product_item['image_symbol_url'] = item["prodSymbolURL"]

                product_item['card_list_index'] = [index]
                product_item['card_list_detail'] = [summary_card_data(item)]

                product_info_extended[code] = product_item
            else:
                product_info_extended[code]['total'] += 1

                product_info_extended[code]['series'] = list(set(product_info_extended[code]['series']) | set(get_series(item)))
                product_info_extended[code]['regulations'] = set_regu_list(item, regu_list=product_info_extended[code]['regulations'])
                product_info_extended[code]['in_standard_regu'] = product_info_extended[code]['in_standard_regu'] or is_stan_regu(item)

                product_info_extended[code]['card_list_index'].append(index)
                product_info_extended[code]['card_list_detail'].append(summary_card_data(item))
        else:
            if code not in product_info_extended:
                product_item = {}
                product_item['code'] = code
                product_item['name'] = item['prodName']
                product_item['type'] = get_type(product_info, item)

                product_item['printed_total'] = item['prodNumber']
                product_item['total'] = 1

                product_item['series'] = get_series(item)
                product_item['regulations'] = set_regu_list(item, empty=True)
                product_item['in_standard_regu'] = is_stan_regu(item)

                product_item['release_date'] = search_in_dict_list(product_info, 'name', item['prodName'], 'releaseDate')
                product_item['update_date'] = datetime.now().strftime("%Y-%m-%d")

                product_item['price'] = search_in_dict_list(product_info, 'name', item['prodName'], 'price')
                product_item['contents'] = search_in_dict_list(product_info, 'name', item['prodName'], 'contents')
                product_item['caution'] = search_in_dict_list(product_info, 'name', item['prodName'], 'caution')

                product_item['prod_url'] = search_in_dict_list(product_info, 'name', item['prodName'], 'url')
                product_item['image_symbol_url'] = item["prodSymbolURL"]
                product_item['image_cover_url'] = search_in_dict_list(product_info, 'name', item['prodName'], "cover_url")

                product_item['card_list_index'] = [index]
                product_item['card_list_detail'] = [summary_card_data(item)]

                product_info_extended[code] = product_item
            else:
                product_info_extended[code]['total'] += 1

                product_info_extended[code]['series'] = list(set(product_info_extended[code]['series']) | set(get_series(item)))
                product_info_extended[code]['regulations'] = set_regu_list(item, regu_list=product_info_extended[code]['regulations'])
                product_info_extended[code]['in_standard_regu'] = product_info_extended[code]['in_standard_regu'] or is_stan_regu(item)

                product_info_extended[code]['card_list_index'].append(index)
                product_info_extended[code]['card_list_detail'].append(summary_card_data(item))

    return all_card_data, product_info_extended

# Verify card counts are correct
def count_card_num(all_card_data, product_info):
    all_card_num = len(all_card_data)
    promo_num = 0

    pack_num = 0
    deck_num = 0
    special_num = 0
    etc_num = 0
    etc_names = []

    regus_set = set()

    for key in product_info:
        regus_set.add(' '.join(product_info[key]['regulations']))

        if product_info[key]['type'] == 'pack':
            pack_num += len(product_info[key]['card_list_index'])
        elif product_info[key]['type'] == 'deck':
            deck_num += len(product_info[key]['card_list_index'])
        elif product_info[key]['type'] == 'special':
            special_num += len(product_info[key]['card_list_index'])
        elif product_info[key]['type'] == 'promo':
            promo_num += len(product_info[key]['card_list_index'])
        else:
            etc_num += len(product_info[key]['card_list_index'])
            etc_names.append(product_info[key]['name'] + " : " + product_info[key]['type'])

    print(f"all card : {all_card_num}")
    print(f"promo : {promo_num}")

    print("###")
    print(f"sum: {pack_num + deck_num + special_num + promo_num}")
    print(f"pack : {pack_num}")
    print(f"deck : {deck_num}")
    print(f"special: {special_num}")
    print(f"etc: {etc_num}")

    print("###")
    for name in etc_names:
        print(name)

    pprint.pprint(sorted(list(regus_set)))

# Populate /card_data_product
def get_product_series(series_list):
    if len(series_list) == 1:
        return series_list[0]
    elif len(series_list) == 2:
        if set(series_list) == set(['S','SM']):
            return 'S'
        elif set(series_list) == set(['S','SV']):
            return 'SV'
    return 'no series'

CARD_DATA_PRODUCT_DIR = '../../card_data_product/'

def gen_card_data_product(all_card_data, product_info):
    json_data_all = {}
    file_write_flag = True  # If False, skip file writing

    for key in product_info:
        product_type = product_info[key]['type']
        product_series = get_product_series(product_info[key]['series'])
        product_code = product_info[key]['code']

        file_dir = CARD_DATA_PRODUCT_DIR + product_type + '/' + product_series + '/'
        if product_type == 'promo':
            file_dir = CARD_DATA_PRODUCT_DIR + product_type + '/'
        file_name = product_code + '.json'
        file_path = file_dir + file_name

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        # Build file contents
        json_data = []
        indexs = product_info[key]['card_list_index']

        for i in indexs:
            json_data.append(all_card_data[i])

        json_data.sort(key=lambda x: int(x['number']))

        if file_path not in json_data_all:
            json_data_all[file_path] = json_data
        else:
            file_write_flag = False
            print('key duplicate : product_info')
            break

    if file_write_flag:
        for path in json_data_all:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(json_data_all[path], f, ensure_ascii=False, indent=4)
        print("card_data_product done")
    else:
        print("something wrong?")

# Populate /product_data
PRODUCT_DATA_DIR = '../../product_data/'

def is_valid_date_format(date_str):
    # Validate YYYY-MM-DD format
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"

    return bool(re.match(date_pattern, date_str))

def gen_product_data(all_card_data, product_info):
    json_data_all = {}
    file_write_flag = True  # If False, skip file writing

    for key in product_info:
        product_type = product_info[key]['type']
        product_series = get_product_series(product_info[key]['series'])

        file_dir = PRODUCT_DATA_DIR + product_type + '/'
        file_name = product_series + '.json'
        file_path = file_dir + file_name

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        if file_path not in json_data_all:
            json_data_all[file_path] = [product_info[key]]
        else:
            json_data_all[file_path].append(product_info[key])

    for path in json_data_all:
        json_data = json_data_all[path]

        # Validate date format
        for item in json_data:
            if not is_valid_date_format(item['release_date']):
                item['release_date'] = '1970-01-01'

        # Sort by release date
        json_data = sorted(json_data, key=lambda x: datetime.strptime(x.get('release_date', '1970-01-01'), "%Y-%m-%d"))

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("product_data done")

if __name__ == "__main__":
    # Build the product info object
    all_card_data, product_info = classify_cards_by_product()
    #count_card_num(all_card_data, product_info)

    # Populate card_data_product from the object
    gen_card_data_product(all_card_data, product_info)

    # Populate product_data from the object
    gen_product_data(all_card_data, product_info)
