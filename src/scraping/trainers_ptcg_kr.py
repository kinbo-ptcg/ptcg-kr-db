from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
import re
import os

# 카드 페이지마다 쓰인 방식이 완전 제각각이다!
# 일단 모아본 것들
# 이것이 카드텍스트에서 발견되는걸로 subtype 판정한다
RULE_TEXT = {
    '아이템' : ["아이템은 자신의 차례에 몇 장이라도 사용할 수 있다."],
    '포켓몬의 도구' : [
        "포켓몬의 도구는 자신의 포켓몬에게 붙여서 사용한다.",
        "포켓몬 1마리에게 1장만 붙일 수 있고 붙인 채로 둔다.",
        "포켓몬의 도구는 자신의 차례에 몇 장이라도 자신의 포켓몬에게 붙일 수 있다.",
        "포켓몬은 이 카드에 적혀 있는 기술을 사용할 수 있다",
        "이 카드를 붙이고 있는"
    ],
    '서포트' : ["서포트는 자신의 차례에 1장만 사용할 수 있다."],
    '스타디움' : [
        "스타디움은 자신의 차례에 1장 배틀필드 옆에 내놓을 수 있다.",
        "다른 스타디움이 필드에 나오면 이 카드를 트래쉬한다.",
        "같은 이름의 스타디움은 필드에 내보낼 수 없다.",
        "다른 이름의 스타디움이 필드에 나오면 이 카드를 트래쉬한다.",
        "스타디움은 자신의 차례에 1장만 배틀필드 옆에 내놓을 수 있다."],
    'ACE SPEC' : ['ACE SPEC 카드는 덱에 1장만 넣을 수 있다.'],
    '프리즘스타' : [
        "같은 이름의 (프리즘스타) (프리즘스타)의 카드는 덱에 1장만 넣을 수 있다.", 
        "트래쉬가 아닌 로스트존에 둔다."]
}

# 표시에 사용할 모범 룰텍스트
RULE_TEXT_SHOW = {
    '아이템' : ["아이템은 자신의 차례에 몇 장이라도 사용할 수 있다."],
    '포켓몬의 도구' : [
        "포켓몬의 도구는 자신의 포켓몬에게 붙여서 사용한다.",
        "포켓몬 1마리에게 1장만 붙일 수 있고 붙인 채로 둔다.",
    ],
    '서포트' : ["서포트는 자신의 차례에 1장만 사용할 수 있다."],
    '스타디움' : [
        "스타디움은 자신의 차례에 1장 배틀필드 옆에 내놓을 수 있다.",
        "다른 스타디움이 필드에 나오면 이 카드를 트래쉬한다.",
        "같은 이름의 스타디움은 필드에 내보낼 수 없다.",
    ],
    'ACE SPEC' : ['ACE SPEC 카드는 덱에 1장만 넣을 수 있다'],
    '프리즘스타' : [
        "같은 이름의 ◇ (프리즘스타) 의 카드는 덱에 1장만 넣을 수 있다.", 
        "트래쉬가 아닌 로스트존에 둔다."]
}

TYPES_ORI = ['풀','불꽃','물','번개','초','격투','악','강철','드래곤','페어리','무색','0코스트','플러스']
TYPES = ['(풀)','(불꽃)','(물)','(번개)','(초)','(격투)','(악)','(강철)','(드래곤)','(페어리)','(무색)','(0코)','(플러스)']
TYPES_DICT = dict(zip(TYPES_ORI,TYPES))
def type_format(type_):
    if type_ in TYPES_ORI:
        return TYPES_DICT[type_]
    else:
        return '(?)'
    
def is_attack_tool(subtypes, texts, name):
    if subtypes[0] != '포켓몬의 도구':
        return False
        
    ATTACK_KEYPHRASE = '이 카드에 적혀 있는 기술을 사용할 수 있다'
    SEAL = '봉인석'
    Z_CRYS = 'Z'
    
    for text in texts:
        if ATTACK_KEYPHRASE in text:
            return True
        
    if SEAL in name:
        return True
    elif Z_CRYS in name:
        return True
    
    return False

def get_attack_tool(texts,soup):
    attack = {}
    attack['name'] = ''
    attack['cost'] = ''
    attack['damage'] = ''
    attack['text'] = ''
    
    attack_title_candidates = soup.find('div', class_='pokemon-abilities').find_all('div', class_='ability')
    result = False
    
    for obj in attack_title_candidates:
        if obj.find('h4', class_='left label').find('img'):
            name = obj.find('h4', class_='left label').get_text().strip().split(' ')[-2]
            cost = ''
            damage = ''
            text = ''
            special = ''
                
            cost_objs = obj.find('h4', class_='left label').find_all('img')
            for cost_obj in cost_objs:
                cost += type_format(cost_obj['title'])
            
            damage = obj.find('h4', class_='left label').get_text().strip().split(' ')[-1]

            if obj.find('p'):
                text = obj.find('p').get_text()
            
            if 'VSTAR' in name:
                special = 'VSTAR'
                # VSTAR 파워 제거해야하는데 홈페이지 문제로 없다
        
            attack['name'] = name
            attack['cost'] = cost
            attack['damage'] = damage
            attack['text'] = text
            if special:
                attack['special'] = special
            
            result = True
            
    # 봉인석 처리
    card_name_obj = soup.find('span', class_='card-hp title')
    if card_name_obj:
        card_name = card_name_obj.get_text()
        if card_name == '숲의 봉인석':
            attack['name'] = '스타알케미'
            attack['text'] = '자신의 차례에 사용할 수 있다. 자신의 덱에서 원하는 카드를 1장 선택해서 패로 가져온다. 그리고 덱을 섞는다. (대전 중 자신은 VSTAR 파워를 1번만 사용할 수 있다.)'
            attack['special'] = 'VSTAR'
            texts = ['이 카드를 붙이고 있는 「포켓몬 V」는 이 VSTAR 파워를 사용할 수 있다.']
            result = True
        elif card_name == '하늘의 봉인석':
            attack['name'] = '스타오더'
            attack['text'] = '자신의 차례에 사용할 수 있다. 이 차례에 자신의 기본 포켓몬인 「포켓몬 V」가 사용하는 기술의 데미지로 상대 배틀필드의 「포켓몬 VSTAR ・ VMAX」가 기절했다면 프라이즈를 1장 더 가져온다. (대전 중 자신은 VSTAR 파워를 1번만 사용할 수 있다.)'
            attack['special'] = 'VSTAR'
            texts = ['이 카드를 붙이고 있는 「포켓몬 V」는 이 VSTAR 파워를 사용할 수 있다.']
            result = True
                    
    return attack, result, texts

def check_subtype(texts, soup):
    subtype_list = ['포켓몬의 도구','서포트','스타디움','아이템']
    
    for text in texts:
        for subtype in subtype_list:
            for keyphrase in RULE_TEXT[subtype]:
                if keyphrase in text:
                    return subtype
        
    # texts 에 효과만 있는 경우가 이렇다.
    # 이럴때는 <div class="pokemon-info"> 보면 된다
    subtype_hint = soup.find('div', class_='pokemon-info').get_text()
    for subtype in subtype_list:
        if subtype in subtype_hint:
            return subtype
    
    # 이렇게 해도 걸러지지 않으면 보통 아이템이다
    return '아이템'

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
                subtypes.append('TAG TEAM')
    
    # 2. span.card-hp title 확인
    keyword_list_name = ['퓨전','일격','연격','플라스마단']
    keyword_candidate_name = soup.find('span', class_ = 'card-hp title').get_text()
    for keyword in keyword_list_name:
        if keyword in keyword_candidate_name:
            if keyword not in subtypes:
                subtypes.append(keyword)
    
    # 3. 두장의 예외 확인
    keyword_name_exception = ['각성의 드럼', '리부트 포드']
    if keyword_name_exception[0] in keyword_candidate_name:
        subtypes.append('고대')
    elif keyword_name_exception[1] in keyword_candidate_name:
        subtypes.append('미래')

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

def texts_and_rules(texts,rules,subtypes):
    #texts 에서 RULE_TEXT[subtypes[0]] 지우기
    texts = [item for item in texts if item not in RULE_TEXT[subtypes[0]]]
    rules.extend(RULE_TEXT_SHOW[subtypes[0]])
    
    #포켓몬의 도구라면 '아이템' 도 지우기
    if subtypes[0] == '포켓몬의 도구':
        texts= [item for item in texts if item not in RULE_TEXT['아이템']]
        rules.extend(RULE_TEXT_SHOW['아이템'])

    #texts 에서 RULE_TEXT['ACE SPEC'], RULE_TEXT['프리즘스타'] 확인하고 지우기
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

    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(error_csv_dir):
        os.makedirs(error_csv_dir)
        
    with open(error_csv_path, mode='a', encoding='utf-8') as f:
        f.write(where + ',' + url + '\n')

def parse(soup, url):    
    # 카드의 데이터 담는 사전
    data = {}
    
    # 모든카드 공통
    id_ = '' 
    cardID = '' 
    name = ''
    supertype = '' 
    subtypes = [] #
    rules = [] #
    number = ''
    prodNumber = ''
    prodCode = ''
    prodSymbolURL = ''
    prodName = ''
    artist = ''
    rarity = ''
    regulationMark = ''
    cardImgURL = ''
    
    # 트레이너즈 카드
    texts = [] #
    
    # 간단히 얻을수 있는 정보 먼저 
    name = soup.find('span', class_ = 'card-hp title').get_text().replace('(프리즘스타)','◇').replace('플라스마단','')
    cardID = name #트레이너즈는 cardID = name
    supertype = '트레이너스'
    
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
    
    # 카드텍스트 모두 획득해서 리스트로
    # 괄호로 끝나는거 이어주기
    # 예 : "(안녕하세요.)" -> "(안녕하세요",")" -> "(안녕하세요)"
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

    # subtypes 획득
    subtypes.append(check_subtype(texts,soup))
    
    # texts 정리 및 rules 기재
    texts,rules,subtypes = texts_and_rules(texts,rules,subtypes)
        
    # 키워드 확인
    # 미래, 고대, 퓨전, 일격, 연격, 플라스마단, 태그팀
    check_keyword(subtypes, soup)

    # 데이터 사전에 넣고 리턴
    data['id'] = id_
    data['cardID'] = cardID
    data['name'] = name
    data['supertype'] = supertype
    data['subtypes'] = subtypes
    data['rules'] = rules
    data['texts'] = texts
    ## 기술 사용하게 해주는 포켓몬의 도구 처리
    if is_attack_tool(subtypes,texts,name):
        attack, result, data['texts']= get_attack_tool(texts,soup)
        if not result:
            log_error_message('attack tool',url)
        data['attack'] = attack
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

