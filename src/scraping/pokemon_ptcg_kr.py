from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import re
import csv
import os
import pokedex_ptcg_kr

# 포켓몬의 경우 다음과 같은 룰을 가지는 것이 있다.
# 레벨업, EX, M진화, BREAK, GX, TAG TEAM, 프리즘스타, V, VMAX, V-UNION, VSTAR, 찬란한, ex
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

# 표시에 사용할 모범 룰텍스트
RULE_TEXT_SHOW = RULE_TEXT

def check_evo(subtypes,soup):
    evo_list = ['기본','1진화','2진화','V진화','복원','레벨업','M진화','BREAK진화','V-UNION']

    # 이럴때는 <div class="pokemon-info"> 보면 된다
    subtype_hint = soup.find('div', class_='pokemon-info').get_text()
    for subtype in evo_list:
        if subtype in subtype_hint:
            subtypes.append(subtype)
            return True
    
    # 진화 정보가 확인되지 않았다
    return False

def check_keyword(subtypes, soup):
    # 미래, 고대, 퓨전, 일격, 연격, 플라스마단, 태그팀
    # 미래, 고대는 div.pokemon-info 보면 있음
    ## 예외 : 각성의 드럼/ 고대
    ## 리부트 포드/ 미래
    # 퓨전, 일격, 연격은 1. div.pokemon-info에 
    ## 2. 이름에 퓨전, 일격, 연격
    # 플라스마단은 div.pokemon-info에 플라스마단 이 발견됨
    # 태그팀 1. div.pokemon-info에 TAG　있음
    keyword_list_info = ['미래','고대','퓨전','일격','연격','TAG','플라스마단']
    
    # 1. div.pokemon-info 확인
    keyword_candidate_info = soup.find('div', class_='pokemon-info').get_text()
    for keyword in keyword_list_info:
        if keyword in keyword_candidate_info:
            if keyword != 'TAG':
                subtypes.append(keyword)
            else:
                if 'TAG TEAM' not in subtypes:
                    subtypes.append('TAG TEAM')
    
    # 2. span.card-hp title 확인
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
    match = re.search(pattern,collectionInfo)
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
TYPES_DICT = dict(zip(TYPES_ORI,TYPES))
def type_format(type_):
    if type_ in TYPES_ORI:
        return TYPES_DICT[type_]
    else:
        return '(?)'
    
def check_ability(obj, abilities,url):
    if obj.find('span', id='skill_label'):
        ability_ = {}
        
        type_ = obj.find('span', id='skill_label').get_text()
        name = ''
        text_obj = obj.find('p')
        if text_obj:
            text = text_obj.get_text().replace('\n',' ').strip()
        else:
            text = ''
            log_error_message('ability text',url)
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
            text = obj.find('p').get_text().replace('\n',' ').strip()
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
            text = obj.find('p').get_text().replace('\n',' ').strip()
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
        # 프리즘스타의 룰 텍스트는 기술로 분류되버림
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
            # VSTAR 파워 제거해야하는데 홈페이지 문제로 없다
        if 'GX' in name:
            special = 'GX'
            
        # 룰인데 기술로 분리될때가 있다. 홈페이지 문제로.
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
    # 'area-parent' 클래스 안에 img 태그가 없고, 특정 텍스트가 span 태그에 포함된 경우, 혹은 프리즘스타 포켓몬
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
        
        #V는 VMAX, V-UNION, VSTAR에 모두 있기에 따로 처리
        if 'V가' in rule:
            subtypes.append('V')
            
        #M진화, BREAK진화는 이미 추가됨 
        subtype_exceptions=['V','M진화','BREAK','V-UNION']     
            
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

    # 디렉토리가 존재하지 않으면 생성
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

# POKEDEX['포켓몬이름'] = 도감범호
def check_pokemons(pokemons, name):
    # 접두사
    prefixs = ['찬란한','빛나는','M','오리진','원시','연격','일격','블랙','화이트','마그마단의','아쿠아단의','백마','흑마','지우','EX','로켓단의','V','울트라','GX','아머드']
    for prefix in prefixs:
        name = name.replace(prefix,'')
    name = name.strip()

    # 리전폼 접두사
    regions = ['가라르','팔데아','알로라','히스이']
    region = ''
    for item in regions:
        if item in name:
            name = name.replace(item,'').strip()
            region = item
    
    # 접미사, TAG 
    poke_names = name.split(' ')[0].split('&')
    
    # 포켓몬의 이름이 카드의 이름에서 검출 되었는가
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
            
    # 로토무는 예외처리
    if '로토무' in name:
        pokemon = {}
        pokemon['name'] = '로토무'
        pokemon['pokedexNumber'] = pokedex_ptcg_kr.POKEDEX['로토무']
        pokemons.append(pokemon)
        result = True
        
    # 피카츄는 예외처리
    if '피카츄' in name:
        pokemon = {}
        pokemon['name'] = '피카츄'
        pokemon['pokedexNumber'] = pokedex_ptcg_kr.POKEDEX['피카츄']
        pokemons.append(pokemon)
        result = True
        
    # 코코 예외처리
    if '코코' in name:
        pokemon = {}
        pokemon['name'] = '코코'
        pokemon['pokedexNumber'] = -1
        pokemons.append(pokemon)
        result = True
            
    return result

# 포켓몬 카드 id부여
# 재록, 고레어 등의 이유로 인해 
# 같은 성능이지만, 다른 카드인 경우가 있다.
# id : 물리적 카드의 고유번호
# cardID : 추상적 카드의 고유번호
# 포켓몬이름앞두글자+타입첫글자+체력(3자리로 포멧)+첫기술이름두글자+데미지(0도 포함)(3자리로포멧)(곱하기등생략)
def make_cardID(pokemons,type_,hp,attacks):
    cardID = ''
    
    def to_three_digit(x):
        if x >= 100 :
            return str(x)
        elif x >= 10 :
            return "0" + str(x)
        else :
            return "00" + str(x)
    
    # 포켓몬 이름 앞 두글자
    # 만약 한글자라면, 그런경우가 뮤, 삐 밖에 없기에 직접 하드코딩
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
        
    # 타입 첫글자
    cardID += re.sub(r'\((.*?)\)', lambda m: m.group(1)[0], type_)
    
    # 체력 세글자
    cardID += to_three_digit(hp)
    
    # 첫기술 이름 앞 두글자
    # 데미지 세글자
    # 기술이 없을때도 예외처리
    if len(attacks) != 0:
        attack_name = attacks[0]['name']
        cardID += attack_name[:2]
        
        attack_damage = attacks[0]['damage']
        if attack_damage:
            cardID += to_three_digit(int(re.findall(r'\d+',attack_damage)[0]))
        else:
            cardID += to_three_digit(0)
    else:
        cardID += '없음'
        cardID += '000'
    
    return cardID

def parse(soup, url):    
    # 카드의 데이터 담는 사전
    data = {}
    
    # 모든카드 공통
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
    
    # 포켓몬 카드
    hp = 0
    pokemons = [] 
    type_ = ''
    attacks = [] 
    abilities = []
    weakness = {}
    resistance = {}
    retreatCost = 0
    flavorText = ''
    
    # 간단히 얻을수 있는 정보 먼저 
    supertype = '포켓몬'
    
    prodSymbolURL= soup.find('div', class_ = 'pre_info_wrap').find('img')['src']
    prodCode = unquote(urlparse(prodSymbolURL).path.split('/')[-1]).split('.')[0]
    
    prodNameObj = soup.find('a', class_ = 'search_href')
    if prodNameObj:
        prodName = prodNameObj.get_text()
    else:
        log_error_message('prod_name',url)
    
    artist_obj = soup.find('p', class_ = 'illustrator')
    if artist_obj:
        artist = artist_obj.get_text(separator=" ").strip().split(' ',1)[-1]
    else:
        artist = '정보없음'
        log_error_message('artist info',url)

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
    
    # 카드 이름 얻기. [이 안에] 있는거 괄호 포함해서 다 삭제
    name = soup.find('span', class_ = 'card-hp title').get_text().replace('(프리즘스타)',' ◇').replace('플라스마단','').replace('\n',' ')
    name = re.sub(r'\[.*?\]', '', name).strip()

    # 카드 번호 얻기
    number, prodNumber = check_card_number(soup)

    # id 만들기
    id_ = prodCode + "-" + number
    # 프로모의 경우 분류가 이상하게 되어있다. 
    # id_ = prodNumber+ "-" + number
    # prodCode = prodNumber 수정
    if is_promo(prodCode, prodName):
        id_ = prodNumber + "-" + number
        prodCode = prodNumber
    
    #진화 체크
    if not check_evo(subtypes,soup):
        log_error_message('check evo',url)
    
    # hp확인
    # 없는경우 예외처리
    hp_obj = soup.find('span', class_ = 'hp_num')
    if hp_obj:
        hp = int(hp_obj.get_text().replace('HP','').strip())
    else:
        log_error_message('no hp_num',url)
        hp = -1
    
    # 타입확인
    # 간혹 멀티타입도 있다
    type_objs = soup.find('div', class_='header').find('div', class_='txt_right').find('span', class_='card-hp').find_all('img', class_ = 'type_b')
    if len(type_objs) == 1:
        type_ = type_format(type_objs[0]['title'])
    elif len(type_objs) == 2:
        type_ = type_format(type_objs[0]['title']) + type_format(type_objs[1]['title'])
        
    # 약점, 저항력, 후퇴 확인
    pokemon_stat_objs = soup.find('div', class_='pokemon-stats').find_all('div', class_='stat')
    
    ## 약점이 있다면 해당 타입의 이미지가 있음
    if pokemon_stat_objs[0].find('img'):
        weakness['type'] = type_format(pokemon_stat_objs[0].find('img')['title'])
        weakness_value_obj = pokemon_stat_objs[0].find('span')
        if weakness_value_obj:
            weakness['value'] = weakness_value_obj.get_text()
        else:
            weakness['value'] = '정보없음'
            log_error_message('weak value',url)
    else:
        weakness['type'] = ''
        weakness['value'] = '--'
        
    ## 저항력이 있다면 해당 타입의 이미지가 있음
    if pokemon_stat_objs[1].find('img'):
        resistance['type'] = type_format(pokemon_stat_objs[1].find('img')['title'])
        resistance_value_obj = pokemon_stat_objs[1].find('span')
        if resistance_value_obj:
            resistance['value'] = resistance_value_obj.get_text()
        else:
            resistance['value'] = '정보없음'
            log_error_message('resi value',url)
    else:
        resistance['type'] = ''
        resistance ['value'] = '--'   
        
    retreatCost = len(pokemon_stat_objs[2].find('div', class_='card-energies').find_all('img'))
    
    # 특성, 기술, 룰 확인
    # 카드 텍스트 안에서 모두 확인 가능
    card_texts_objs = soup.find('div', class_='pokemon-abilities').find_all('div', class_='ability')
    for obj in card_texts_objs:
        # V-UNION카드들 처럼 안쪽이 비어있는 경우가 있으면 페스
        if len(obj.contents) < 3:
            continue

        if check_ability(obj, abilities,url):
            continue
        elif check_attack(obj, attacks):
            continue
        elif check_rule(obj, rules, subtypes):
            continue
        else:
            log_error_message('card text', url)
        
    # 플레이버 텍스트
    flavorTextObj = soup.find('div', class_='col-md-8 col-xs-7 colsit').find('p')
    if flavorTextObj:
        flavorText = flavorTextObj.get_text()
    ## 예외 처리
    if flavorText == 'n/a':
        flavorText = ''
        
    # 키워드 확인
    # 미래, 고대, 퓨전, 일격, 연격, 플라스마단, 태그팀
    check_keyword(subtypes, soup)
    
    # 포켓몬 확인
    # 확인이 되었으면 포켓몬 카드 id부여
    if not check_pokemons(pokemons, name):
        log_error_message('check pokemons',url)
    else:
        cardID = make_cardID(pokemons,type_,hp,attacks)

    # 데이터 사전에 넣고 리턴
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
    data['prodSymbolURL'] =prodSymbolURL
    data['prodName'] = prodName
    data['artist'] = artist
    data['rarity'] = rarity
    data['regulationMark'] = regulationMark
    data['cardImgURL'] = cardImgURL
    data['cardPageURL'] = url
    
    return data