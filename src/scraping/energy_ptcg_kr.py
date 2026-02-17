from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import re
import os

RULE_TEXT = {
    'ACE SPEC' : ['ACE SPEC 카드는 덱에 1장만 넣을 수 있다.'],
    '프리즘스타' : [
        "같은 이름의 (프리즘스타) (프리즘스타)의 카드는 덱에 1장만 넣을 수 있다.",
        "트래쉬가 아닌 로스트존에 둔다."]
}

# Canonical rule text used for display
RULE_TEXT_SHOW = {
    'ACE SPEC' : ['ACE SPEC 카드는 덱에 1장만 넣을 수 있다'],
    '프리즘스타' : [
        "같은 이름의 ◇ (프리즘스타) 의 카드는 덱에 1장만 넣을 수 있다.",
        "트래쉬가 아닌 로스트존에 둔다."]
}

def check_subtype(soup):
    subtype_list = ['특수 에너지','기본 에너지']

    # Check <div class="pokemon-info"> for subtype
    subtype_hint = soup.find('div', class_='pokemon-info').get_text()
    for subtype in subtype_list:
        if subtype in subtype_hint:
            return subtype

    # Default to Basic Energy if not found
    return '기본 에너지'

def check_keyword(subtypes, soup):
    # Keywords: Future, Ancient, Fusion, Single Strike, Rapid Strike, Team Plasma, TAG TEAM
    # Future and Ancient appear in div.pokemon-info
    ## Exceptions: Awakened Drum / Ancient, Reboot Pod / Future
    # Fusion, Single Strike, Rapid Strike appear in:
    ## 1. div.pokemon-info
    ## 2. Card name
    # Team Plasma appears in div.pokemon-info
    # Some Plasma energy cards do not contain '플라스마단'
    # TAG TEAM: 1. div.pokemon-info contains "TAG"
    keyword_list_info = ['미래','고대','퓨전','일격','연격','TAG','플라스마단']

    # 1. Check div.pokemon-info
    keyword_candidate_info = soup.find('div', class_='pokemon-info').get_text()
    for keyword in keyword_list_info:
        if keyword in keyword_candidate_info:
            if keyword != 'TAG':
                subtypes.append(keyword)
            else:
                subtypes.append('TAG TEAM')

    # 2. Check span.card-hp title
    keyword_list_name = ['퓨전','일격','연격','플라스마단']
    keyword_candidate_name = soup.find('span', class_ = 'card-hp title').get_text()
    for keyword in keyword_list_name:
        if keyword in keyword_candidate_name:
            if keyword not in subtypes:
                subtypes.append(keyword)

    # 3. Edge cases
    if '플라스마단' not in subtypes:
        if '플라스마 에너지' in keyword_candidate_name:
            subtypes.append('플라스마단')
    if '일격' not in subtypes:
        if '임팩트 에너지' in keyword_candidate_name:
            subtypes.append('일격')

def check_card_number(soup):
    # case1: 011/034 -> ['011','034']
    # case2: 011/SV-P -> ['011','SV-P']
    # case3: SV-P -> ['000','SV-P']

    collectionInfoObj = soup.find('span', class_ = 'p_num')
    # Some cards have no number at all
    # case0: none -> ['000','000']
    if not collectionInfoObj:
        number = '000'
        prodNumber = '000'
    else:
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

def texts_and_rules(texts, rules, subtypes):
    # Check for ACE SPEC and Prism Star rule text and remove from texts
    for key in ['ACE SPEC','프리즘스타']:
        if RULE_TEXT[key][0] in texts:
            subtypes.append(key)
            texts = [item for item in texts if item not in RULE_TEXT[key]]
            rules.extend(RULE_TEXT_SHOW[key])

    return texts, rules, subtypes

def is_promo(prodCode, prodName):
    if 'promo' in prodCode:
        return True
    elif '프로모' in prodName:
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
    rarity = ''
    regulationMark = ''
    cardImgURL = ''

    # Energy card specific fields
    texts = []

    # Gather simple fields first
    name = soup.find('span', class_ = 'card-hp title').get_text().replace('(프리즘스타)','◇').replace('플라스마단','')
    cardID = name  # For Energy cards, cardID == card name
    supertype = '에너지'

    prodNameObj = soup.find('a', class_ = 'search_href')
    if prodNameObj:
        prodName = prodNameObj.get_text()
    else:
        log_error_message('prod_name', url)

    rare_text = soup.find('span', id="no_wrap_by_admin").get_text()
    if rare_text.strip() == "":
        rarity = 'N'
    else:
        rarity = rare_text.strip()

    cardImgURL = soup.find('img', class_ = 'feature_image')['src']

    # Get card number
    number, prodNumber = check_card_number(soup)

    # Get product symbol URL; basic energy cards may not have one
    prodSymbolUrlObj = soup.find('div', class_ = 'pre_info_wrap').find('img')
    if prodSymbolUrlObj:
        prodSymbolURL = prodSymbolUrlObj['src']
        prodCode = unquote(urlparse(prodSymbolURL).path.split('/')[-1]).split('.')[0]

    # Build id
    id_ = prodCode + "-" + number
    # Promo cards have a different classification on the website
    # id_ = prodNumber + "-" + number
    # prodCode = prodNumber fix
    if is_promo(prodCode, prodName):
        id_ = prodNumber + "-" + number
        prodCode = prodNumber

    # Collect all card text as a list
    # Join split lines that end with ')'
    # e.g. "(Hello.)" -> "(Hello", ")" -> "(Hello)"
    card_text_objs = soup.find('div', class_ = 'pokemon-abilities').find_all('p')

    for obj in card_text_objs:
        lines = obj.get_text().split('.')
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith(')'):
                line = line.lstrip(')')
                texts[-1] = texts[-1] + ')'
            if line.strip():
                texts.append(line.strip() + '.')

    # Get subtype
    subtypes.append(check_subtype(soup))

    # Some cards (especially BW-era) have no regulation mark
    regulationMarkUrlObj = soup.find('div', class_ = 'pre_info_wrap').find_all('img')
    if len(regulationMarkUrlObj) > 1:
        regulationMarkURL = regulationMarkUrlObj[1]['src']
        regulationMark = unquote(urlparse(regulationMarkURL).path.split('/')[-1]).split('.')[0]
    else:
        pass

    # Clean up texts and populate rules
    texts, rules, subtypes = texts_and_rules(texts, rules, subtypes)

    # Check keywords: Future, Ancient, Fusion, Single Strike, Rapid Strike, Team Plasma, TAG TEAM
    check_keyword(subtypes, soup)

    # Store data and return
    data['id'] = id_
    data['cardID'] = cardID
    data['name'] = name
    data['supertype'] = supertype
    data['subtypes'] = subtypes
    data['rules'] = rules
    data['texts'] = texts
    data['number'] = number
    data['prodNumber'] = prodNumber
    data['prodCode'] = prodCode
    data['prodSymbolURL'] = prodSymbolURL
    data['prodName'] = prodName
    data['rarity'] = rarity
    data['regulationMark'] = regulationMark
    data['cardImgURL'] = cardImgURL
    data['cardPageURL'] = url

    return data
