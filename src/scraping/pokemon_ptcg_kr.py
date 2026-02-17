from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import re
import csv
import os
import pokedex_ptcg_kr

# Pokémon cards may have the following rules:
# Level-Up, EX, Mega Evolution, BREAK, GX, TAG TEAM, Prism Star, V, VMAX, V-UNION, VSTAR, Radiant, ex
RULE_TEXT = {
    '레벨업' : [
        "이 카드는 배틀필드의 포켓몬에 겹쳐서 레벨업시킨다.",
        "레벨업 전의 기술 포켓파워도 사용할 수 있고 포켓바디도 작용한다."],
    'EX' : ["포켓몬 EX가 기절한 경우 상대는 프라이즈를 2장 가져간다."],
    'M진화' : ["M진화 포켓몬으로 진화하면 자신의 차례는 끝난다."],
    'BREAK' : ["BREAK진화 전의 제르네아스가 가진 「기술 ･ 특성 ･ 약점 ･ 저항력 ･ 후퇴」를 이어받는다."],
    'GX' : ["포켓몬 GX가 기절한 경우 상대는 프라이즈를 2장 가져간다."],
    'TAG' : ["TAG TEAM이 기절한 경우 상대는 프라이즈를 3장 가져간다."],
    '프리즘스타' : [
        "같은 이름의 (프리즘스타) (프리즘스타)의 카드는 덱에 1장만 넣을 수 있다.",
        "트래쉬가 아닌 로스트존에 둔다."],
    'V' : ["포켓몬 V가 기절한 경우 상대는 프라이즈를 2장 가져간다."],
    'VMAX' : ["포켓몬 VMAX가 기절한 경우 상대는 프라이즈를 3장 가져간다."],
    'V-UNION' : [
        "포켓몬 [V-UNION]이 기절한 경우 상대는 프라이즈를 3장 가져간다.",
        "대전 중에 1번 자신의 차례에 자신의 트래쉬에 있는 4종류의 V-UNION 포켓몬을 조합하여 벤치로 내보낸다."],
    'VSTAR' : ["포켓몬 VSTAR가 기절한 경우 상대는 프라이즈를 2장 가져간다."],
    '찬란한' : ["찬란한 포켓몬은 덱에 1장만 넣을 수 있다."],
    'ex' : ["포켓몬 ex가 기절한 경우 상대는 프라이즈를 2장 가져간다."]
}

# Canonical rule text used for display
RULE_TEXT_SHOW = RULE_TEXT

def check_evo(subtypes, soup):
    evo_list = ['기본','1진화','2진화','V진화','복원','레벨업','M진화','BREAK진화','V-UNION']

    # Check <div class="pokemon-info"> for evolution stage info
    subtype_hint = soup.find('div', class_='pokemon-info').get_text()
    for subtype in evo_list:
        if subtype in subtype_hint:
            subtypes.append(subtype)
            return True

    # Evolution info not found
    return False

def check_keyword(subtypes, soup):
    # Keywords: Future, Ancient, Fusion, Single Strike, Rapid Strike, Team Plasma, TAG TEAM
    # Future and Ancient appear in div.pokemon-info
    ## Exceptions: Awakened Drum / Ancient, Reboot Pod / Future
    # Fusion, Single Strike, Rapid Strike appear in:
    ## 1. div.pokemon-info
    ## 2. Card name
    # Team Plasma appears in div.pokemon-info
    # TAG TEAM: 1. div.pokemon-info contains "TAG"
    keyword_list_info = ['미래','고대','퓨전','일격','연격','TAG','플라스마단']

    # 1. Check div.pokemon-info
    keyword_candidate_info = soup.find('div', class_='pokemon-info').get_text()
    for keyword in keyword_list_info:
        if keyword in keyword_candidate_info:
            if keyword != 'TAG':
                subtypes.append(keyword)
            else:
                if 'TAG TEAM' not in subtypes:
                    subtypes.append('TAG TEAM')

    # 2. Check span.card-hp title
    keyword_list_name = ['퓨전','일격','연격','플라스마단']
    keyword_candidate_name = soup.find('span', class_ = 'card-hp title').get_text()
    for keyword in keyword_list_name:
        if keyword in keyword_candidate_name:
            if keyword not in subtypes:
                subtypes.append(keyword)


def check_card_number(soup):
    # case1: 011/034 -> ['011','034']
    # case2: 011/SV-P -> ['011','SV-P']
    # case3: SV-P -> ['000','SV-P']

    collectionInfo = soup.find('span', class_ = 'p_num').get_text()
    pattern = r'(\d+)/(\d+)'
    match = re.search(pattern, collectionInfo)
    if match:
        number = match.group(1)
        prodNumber = match.group(2)
    else:
        collectionInfo_list = collectionInfo.split('/')
        if len(collectionInfo_list) == 2:
            number = collectionInfo_list[0].strip()
            prodNumber = collectionInfo_list[1].strip().split()[0]
        else:
            number = '000'
            prodNumber = collectionInfo_list[0].strip().split()[0]

    return number, prodNumber

TYPES_ORI = ['풀','불꽃','물','번개','초','격투','악','강철','드래곤','페어리','무색','0코스트','플러스']
TYPES = ['(풀)','(불꽃)','(물)','(번개)','(초)','(격투)','(악)','(강철)','(드래곤)','(페어리)','(무색)','(0코)','(플러스)']
TYPES_DICT = dict(zip(TYPES_ORI, TYPES))
def type_format(type_):
    if type_ in TYPES_ORI:
        return TYPES_DICT[type_]
    else:
        return '(?)'

def check_ability(obj, abilities, url):
    if obj.find('span', id='skill_label'):
        ability_ = {}

        type_ = obj.find('span', id='skill_label').get_text()
        name = ''
        text_obj = obj.find('p')
        if text_obj:
            text = text_obj.get_text().replace('\n', ' ').strip()
        else:
            text = ''
            log_error_message('ability text', url)
        special = ''

        if type_ == '포켓파워' or type_ == '포켓바디':
            name = obj.find('span', id='skill_label').next_sibling.strip()
        elif type_ == '특성':
            name = obj.find('span', class_='skil_name').get_text().replace('[특성]','').strip()
            if 'VSTAR' in name:
                name = name.split('\n')[1].strip()
                special = 'VSTAR'

        ability_['name'] = name
        ability_['text'] = text
        ability_['type'] = type_
        if special:
            ability_['special'] = special

        abilities.append(ability_)

        return True
    elif obj.find('span', class_='skil_name'):
        if '고대능력' in obj.find('span', class_='skil_name').get_text():
            ability_ = {}

            type_ = '고대능력'
            name = obj.find('span', class_='skil_name').get_text().replace('[고대능력]','').strip()
            text = obj.find('p').get_text().replace('\n', ' ').strip()
            special = ''

            ability_['name'] = name
            ability_['text'] = text
            ability_['type'] = type_
            if special:
                ability_['special'] = special

            abilities.append(ability_)

            return True
        elif '테라스탈' in obj.find('span', class_='skil_name').get_text():
            ability_ = {}

            type_ = '테라스탈'
            name = '테라스탈'
            text = obj.find('p').get_text().replace('\n', ' ').strip()
            special = ''

            ability_['name'] = name
            ability_['text'] = text
            ability_['type'] = type_
            if special:
                ability_['special'] = special

            abilities.append(ability_)

            return True
    else:
        return False

def check_attack(obj, attacks):
    if obj.find('div', class_='area-parent').find('img') or obj.find('div', class_='area-parent').find('span', class_='plus'):
        # Prism Star rule text gets categorized as an attack on the website
        if '프리즘스타' in obj.find('span', class_='skil_name').get_text():
            return False

        attack = {}

        name = obj.find('span', class_='skil_name').get_text().strip()
        cost = ''
        damage = ''
        text = ''
        special = ''

        if obj.find('p'):
            text = obj.find('p').get_text()

        cost_objs = obj.find('div', class_ = 'area-parent').find_all('img')
        if not cost_objs:
            cost += '정보없음'
        else:
            for cost_obj in cost_objs:
                cost += type_format(cost_obj['title'])

        damage_obj = obj.find('span', class_ = 'plus')
        if damage_obj:
            damage = damage_obj.get_text().strip()

        if 'VSTAR' in name:
            special = 'VSTAR'
            # VSTAR Power removal needed but not possible due to website issue
        if 'GX' in name:
            special = 'GX'

        # Sometimes rules get parsed as attacks due to website issues
        for RULE_KEY in RULE_KEYWORDS:
            if RULE_KEY in name:
                if text == RULE_TEXT[RULE_KEY][0]:
                    return False

        attack['name'] = name
        attack['cost'] = cost
        attack['damage'] = damage
        attack['text'] = text
        if special:
            attack['special'] = special

        attacks.append(attack)

        return True
    else:
        return False

RULE_KEYWORDS = ['레벨업', 'EX', 'M진화', 'BREAK', 'GX', 'TAG TEAM', '프리즘스타', 'V', 'VMAX', 'V-UNION', 'VSTAR', '찬란한', 'ex']
def check_rule(obj, rules, subtypes):
    # No img in 'area-parent' and certain text found in span tag, or Prism Star Pokémon
    rule_name = obj.find('span', class_='skil_name').get_text().strip()
    rule_shortpath = False
    for RULE_KEY in RULE_KEYWORDS:
        if RULE_KEY in rule_name:
            rule_shortpath = True

    if rule_shortpath or (not obj.find('div', class_='area-parent').find('img') and (
        '룰' in rule_name or
        'V-UNION' in rule_name
    )) or '프리즘스타' in rule_name:
        rule = 'not found'
        if obj.find('p'):
            rule = obj.find('p').get_text().replace('\n', ' ')
        else:
            for keyword in RULE_KEYWORDS:
                if keyword in rule_name:
                    rule_list = RULE_TEXT[keyword]
                    rule = ' '.join(rule_list)

        if rule == 'not found':
            return False
        else:
            rules.append(rule)

        # 'V' appears in VMAX, V-UNION, and VSTAR, so handle separately
        if 'V가' in rule:
            subtypes.append('V')

        # M-Evolution and BREAK Evolution are already added
        subtype_exceptions = ['V','M진화','BREAK','V-UNION']

        for KEYWORD in RULE_KEYWORDS:
            if KEYWORD in subtype_exceptions:
                continue
            elif KEYWORD in rule:
                if KEYWORD not in subtypes:
                    subtypes.append(KEYWORD)

        return True
    else:
        return False

def log_error_message(where, url):
    print(f'ERROR! {where}')
    print(f'URL : {url}')

    error_csv_dir = './data_cleansing/error/'
    error_csv_path = './data_cleansing/error/error_m.csv'

    # Create directory if it does not exist
    if not os.path.exists(error_csv_dir):
        os.makedirs(error_csv_dir)

    with open(error_csv_path, mode='a', encoding='utf-8') as f:
        f.write(where + ',' + url + '\n')

def is_promo(prodCode, prodName):
    if 'promo' in prodCode:
        return True
    elif '프로모' in prodName:
        return True
    else:
        return False

# POKEDEX['pokemon_name'] = pokedex_number
def check_pokemons(pokemons, name):
    # Prefixes
    prefixs = ['찬란한','빛나는','M','오리진','원시','연격','일격','블랙','화이트','마그마단의','아쿠아단의','백마','흑마','지우','EX','로켓단의','V','울트라','GX','아머드']
    for prefix in prefixs:
        name = name.replace(prefix, '')
    name = name.strip()

    # Regional form prefixes
    regions = ['가라르','팔데아','알로라','히스이']
    region = ''
    for item in regions:
        if item in name:
            name = name.replace(item, '').strip()
            region = item

    # Suffixes, TAG TEAM
    poke_names = name.split(' ')[0].split('&')

    # Whether a Pokémon name was found in the card name
    result = False

    for poke_name in poke_names:
        if poke_name in pokedex_ptcg_kr.POKEDEX:
            pokemon = {}
            pokemon['name'] = poke_name
            pokemon['pokedexNumber'] = pokedex_ptcg_kr.POKEDEX[poke_name]
            if region:
                pokemon['region'] = region
            pokemons.append(pokemon)
            result = True

    # Special handling for Rotom
    if '로토무' in name:
        pokemon = {}
        pokemon['name'] = '로토무'
        pokemon['pokedexNumber'] = pokedex_ptcg_kr.POKEDEX['로토무']
        pokemons.append(pokemon)
        result = True

    # Special handling for Pikachu
    if '피카츄' in name:
        pokemon = {}
        pokemon['name'] = '피카츄'
        pokemon['pokedexNumber'] = pokedex_ptcg_kr.POKEDEX['피카츄']
        pokemons.append(pokemon)
        result = True

    # Special handling for Koko
    if '코코' in name:
        pokemon = {}
        pokemon['name'] = '코코'
        pokemon['pokedexNumber'] = -1
        pokemons.append(pokemon)
        result = True

    return result

# Assign Pokémon card ID
# Cards may be reprints or high-rarity variants with the same stats but different physical prints.
# id : unique identifier for a physical card print
# cardID : unique identifier for a card's abstract stats/effect
# Format: first 2 chars of Pokémon name + first char of type + HP (3 digits) + first 2 chars of first attack + damage (3 digits, including 0)
def make_cardID_old(pokemons, type_, hp, attacks):
    cardID = ''

    def to_three_digit(x):
        if x >= 100 :
            return str(x)
        elif x >= 10 :
            return "0" + str(x)
        else :
            return "00" + str(x)

    # First 2 chars of Pokémon name
    # Special cases for 1-character names (Mew and Togepi only)
    pokemon_name = pokemons[0]['name']
    if len(pokemon_name) == 1:
        if pokemon_name == '뮤':
            cardID += '뮤우'
        elif pokemon_name == '삐':
            cardID += '삐이'
        else:
            cardID += pokemon_name + pokemon_name
    else:
        cardID += pokemon_name[:2]

    # First char of type
    cardID += re.sub(r'\((.*?)\)', lambda m: m.group(1)[0], type_)

    # HP as 3 digits
    cardID += to_three_digit(hp)

    # First 2 chars of first attack name + damage as 3 digits
    # Handle case of no attacks
    if len(attacks) != 0:
        attack_name = attacks[0]['name']
        cardID += attack_name[:2]

        attack_damage = attacks[0]['damage']
        if attack_damage:
            cardID += to_three_digit(int(re.findall(r'\d+', attack_damage)[0]))
        else:
            cardID += to_three_digit(0)
    else:
        cardID += '없음'
        cardID += '000'

    return cardID

def make_cardID(item):
    def to_three_digit(x):
        if x >= 100 :
            return str(x)
        elif x >= 10 :
            return "0" + str(x)
        else :
            return "00" + str(x)

    supertype = item.get('supertype', '?')
    if supertype == '?':
        print("ERROR : supertype")
        print(item['url'])
    elif supertype != '포켓몬':
        return item['name']
    else:
        cardID = ''
        pokemons = item['pokemons']
        type_ = item['type']
        hp = item['hp']
        attacks = item['attacks']
        abilitites = item['abilities']

        # First 2 chars of Pokémon name
        # Special cases for 1-character names (Mew and Togepi only)
        pokemon_name = pokemons[0]['name']
        if len(pokemon_name) == 1:
            if pokemon_name == '뮤':
                cardID += '뮤우'
            elif pokemon_name == '삐':
                cardID += '삐이'
            else:
                cardID += pokemon_name + pokemon_name
        else:
            cardID += pokemon_name[:2]

        # First char of type
        cardID += re.sub(r'\((.*?)\)', lambda m: m.group(1)[0], type_)

        # HP as 3 digits
        cardID += to_three_digit(hp)

        # If ability exists, first 2 chars of the first ability name
        if len(abilitites) != 0:
            abil_name = abilitites[0]['name'].replace(' ', '').strip()
            if len(abil_name) == 1:
                cardID += abil_name + abil_name
            else:
                cardID += abil_name[:2]

        # First 2 chars of each attack name + damage as 3 digits
        # Handle case of no attacks
        # Repeat 1-char attack names, strip spaces
        if len(attacks) != 0:
            for i in range(len(attacks)):
                attack_name = attacks[i]['name'].replace(' ', '').strip()
                if len(attack_name) == 1:
                    cardID += attack_name + attack_name
                else:
                    cardID += attack_name[:2]

                attack_damage = attacks[i]['damage']
                if attack_damage:
                    cardID += to_three_digit(int(re.findall(r'\d+', attack_damage)[0]))
                else:
                    cardID += to_three_digit(0)
        else:
            cardID += '없음'
            cardID += '000'

        return cardID

def parse(soup, url):
    # Dictionary to hold card data
    data = {}

    # Common fields for all card types
    id_ = ''
    cardID = ''
    name = ''
    supertype = ''
    subtypes = []
    rules = []
    number = ''
    prodNumber = ''
    prodCode = ''
    prodSymbolURL = ''
    prodName = ''
    artist = ''
    rarity = ''
    regulationMark = ''
    cardImgURL = ''

    # Pokémon card specific fields
    hp = 0
    pokemons = []
    type_ = ''
    attacks = []
    abilities = []
    weakness = {}
    resistance = {}
    retreatCost = 0
    flavorText = ''

    # Gather simple fields first
    supertype = '포켓몬'

    prodSymbolURL = soup.find('div', class_ = 'pre_info_wrap').find('img')['src']
    prodCode = unquote(urlparse(prodSymbolURL).path.split('/')[-1]).split('.')[0]

    prodNameObj = soup.find('a', class_ = 'search_href')
    if prodNameObj:
        prodName = prodNameObj.get_text()
    else:
        log_error_message('prod_name', url)

    artist_obj = soup.find('p', class_ = 'illustrator')
    if artist_obj:
        artist = artist_obj.get_text(separator=" ").strip().split(' ', 1)[-1]
    else:
        artist = '정보없음'
        log_error_message('artist info', url)

    rare_text = soup.find('span', id="no_wrap_by_admin").get_text()
    if rare_text.strip() == "":
        rarity = 'N'
    else:
        rarity = rare_text.strip()

    regulationMarkUrlObj = soup.find('div', class_ = 'pre_info_wrap').find_all('img')
    if len(regulationMarkUrlObj) > 1:
        regulationMarkURL = regulationMarkUrlObj[1]['src']
        regulationMark = unquote(urlparse(regulationMarkURL).path.split('/')[-1]).split('.')[0]
    else:
        pass

    cardImgURL = soup.find('img', class_ = 'feature_image')['src']

    # Get card name; remove anything in [brackets] including the brackets
    name = soup.find('span', class_ = 'card-hp title').get_text().replace('(프리즘스타)',' ◇').replace('플라스마단','').replace('\n',' ')
    name = re.sub(r'\[.*?\]', '', name).strip()

    # Get card number
    number, prodNumber = check_card_number(soup)

    # Build id
    id_ = prodCode + "-" + number
    # Promo cards have a different classification on the website
    # id_ = prodNumber + "-" + number
    # prodCode = prodNumber fix
    if is_promo(prodCode, prodName):
        id_ = prodNumber + "-" + number
        prodCode = prodNumber

    # Check evolution stage
    if not check_evo(subtypes, soup):
        log_error_message('check evo', url)

    # Check HP; handle missing HP case
    hp_obj = soup.find('span', class_ = 'hp_num')
    if hp_obj:
        hp = int(hp_obj.get_text().replace('HP', '').strip())
    else:
        log_error_message('no hp_num', url)
        hp = -1

    # Check type; some cards have dual types
    type_objs = soup.find('div', class_='header').find('div', class_='txt_right').find('span', class_='card-hp').find_all('img', class_ = 'type_b')
    if len(type_objs) == 1:
        type_ = type_format(type_objs[0]['title'])
    elif len(type_objs) == 2:
        type_ = type_format(type_objs[0]['title']) + type_format(type_objs[1]['title'])

    # Check weakness, resistance, retreat cost
    pokemon_stat_objs = soup.find('div', class_='pokemon-stats').find_all('div', class_='stat')

    ## Weakness has a type image if present
    if pokemon_stat_objs[0].find('img'):
        weakness['type'] = type_format(pokemon_stat_objs[0].find('img')['title'])
        weakness_value_obj = pokemon_stat_objs[0].find('span')
        if weakness_value_obj:
            weakness['value'] = weakness_value_obj.get_text()
        else:
            weakness['value'] = '정보없음'
            log_error_message('weak value', url)
    else:
        weakness['type'] = ''
        weakness['value'] = '--'

    ## Resistance has a type image if present
    if pokemon_stat_objs[1].find('img'):
        resistance['type'] = type_format(pokemon_stat_objs[1].find('img')['title'])
        resistance_value_obj = pokemon_stat_objs[1].find('span')
        if resistance_value_obj:
            resistance['value'] = resistance_value_obj.get_text()
        else:
            resistance['value'] = '정보없음'
            log_error_message('resi value', url)
    else:
        resistance['type'] = ''
        resistance['value'] = '--'

    retreatCost = len(pokemon_stat_objs[2].find('div', class_='card-energies').find_all('img'))

    # Check abilities, attacks, and rules
    # All can be found within the card text section
    card_texts_objs = soup.find('div', class_='pokemon-abilities').find_all('div', class_='ability')
    for obj in card_texts_objs:
        # Skip empty containers (e.g. V-UNION cards)
        if len(obj.contents) < 3:
            continue

        if check_ability(obj, abilities, url):
            continue
        elif check_attack(obj, attacks):
            continue
        elif check_rule(obj, rules, subtypes):
            continue
        else:
            log_error_message('card text', url)

    # Flavor text
    flavorTextObj = soup.find('div', class_='col-md-8 col-xs-7 colsit').find('p')
    if flavorTextObj:
        flavorText = flavorTextObj.get_text()
    ## Exception handling
    if flavorText == 'n/a':
        flavorText = ''

    # Check keywords: Future, Ancient, Fusion, Single Strike, Rapid Strike, Team Plasma, TAG TEAM
    check_keyword(subtypes, soup)

    # Check Pokémon and assign card ID
    if not check_pokemons(pokemons, name):
        log_error_message('check pokemons', url)
    else:
        cardID = make_cardID_old(pokemons, type_, hp, attacks)

    # Store data and return
    data['id'] = id_
    data['cardID'] = cardID
    data['name'] = name
    data['supertype'] = supertype
    data['subtypes'] = subtypes
    data['rules'] = rules

    data['hp'] = hp
    data['pokemons'] = pokemons
    data['type'] = type_
    data['attacks'] = attacks
    data['abilities'] = abilities
    data['weakness'] = weakness
    data['resistance'] = resistance
    data['retreatCost'] = retreatCost
    data['flavorText'] = flavorText

    data['number'] = number
    data['prodNumber'] = prodNumber
    data['prodCode'] = prodCode
    data['prodSymbolURL'] = prodSymbolURL
    data['prodName'] = prodName
    data['artist'] = artist
    data['rarity'] = rarity
    data['regulationMark'] = regulationMark
    data['cardImgURL'] = cardImgURL
    data['cardPageURL'] = url

    ## cardID assignment method updated 240926
    cardID = make_cardID(data)
    data['cardID'] = cardID

    return data
