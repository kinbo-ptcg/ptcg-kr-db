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

# 표시에 사용할 모범 룰텍스트
RULE_TEXT_SHOW = {
    'ACE SPEC' : ['ACE SPEC 카드는 덱에 1장만 넣을 수 있다'],
    '프리즘스타' : [
        "같은 이름의 ◇ (프리즘스타) 의 카드는 덱에 1장만 넣을 수 있다.", 
        "트래쉬가 아닌 로스트존에 둔다."]
}

def check_subtype(soup):
    subtype_list = ['특수 에너지','기본 에너지']
        
    # texts 에 효과만 있는 경우가 이렇다.
    # 이럴때는 <div class="pokemon-info"> 보면 된다
    subtype_hint = soup.find('div', class_='pokemon-info').get_text()
    for subtype in subtype_list:
        if subtype in subtype_hint:
            return subtype
    
    # 이렇게 해도 걸러지지 않으면 기본 에너지이다
    return '기본 에너지'

def check_keyword(subtypes, soup):
    # 미래, 고대, 퓨전, 일격, 연격, 플라스마단, 태그팀
    # 미래, 고대는 div.pokemon-info 보면 있음
    ## 예외 : 각성의 드럼/ 고대
    ## 리부트 포드/ 미래
    # 퓨전, 일격, 연격은 1. div.pokemon-info에 
    ## 2. 이름에 퓨전, 일격, 연격
    # 플라스마단은 div.pokemon-info에 플라스마단 이 발견됨
    # 어떤 플라스마 에너지는 '플라스마단' 이 없음
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
    
    # 3. 예외
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
    # 간혹 번호가 아예 없는 경우도 있다
    # case0: none -> ['000','000']
    if not collectionInfoObj:
        number = '000'
        prodNumber = '000'
    else:
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

def parse(soup,url):    
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
    rarity = ''
    regulationMark = ''
    cardImgURL = ''
    
    # 트레이너즈 카드
    texts = [] #
    
    # 간단히 얻을수 있는 정보 먼저 
    name = soup.find('span', class_ = 'card-hp title').get_text().replace('(프리즘스타)','◇').replace('플라스마단','')
    cardID = name #트레이너즈는 cardID = name
    supertype = '에너지'
    
    prodNameObj = soup.find('a', class_ = 'search_href')
    if prodNameObj:
        prodName = prodNameObj.get_text()
    else:
        log_error_message('prod_name',url)  
      
    rare_text = soup.find('span', id="no_wrap_by_admin").get_text()
    if rare_text.strip() == "":
        rarity = 'N'
    else:
        rarity = rare_text.strip()

    cardImgURL = soup.find('img', class_ = 'feature_image')['src']
    
    # 카드 번호 얻기
    number, prodNumber = check_card_number(soup)
    
    # 상품번호 얻기. 기본에너지는 이것조차 없을때가 있다
    prodSymbolUrlObj= soup.find('div', class_ = 'pre_info_wrap').find('img')
    if prodSymbolUrlObj:
        prodSymbolURL = prodSymbolUrlObj['src']
        prodCode = unquote(urlparse(prodSymbolURL).path.split('/')[-1]).split('.')[0]

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
    subtypes.append(check_subtype(soup))
        
    # 레규가 없는카드도 있다. 특히 BW쪽은
    regulationMarkUrlObj = soup.find('div', class_ = 'pre_info_wrap').find_all('img')
    if len(regulationMarkUrlObj) > 1:
        regulationMarkURL = regulationMarkUrlObj[1]['src']
        regulationMark = unquote(urlparse(regulationMarkURL).path.split('/')[-1]).split('.')[0]
    else:
        pass
    
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
    data['number'] = number
    data['prodNumber'] = prodNumber
    data['prodCode'] = prodCode
    data['prodSymbolURL'] =prodSymbolURL
    data['prodName'] = prodName
    data['rarity'] = rarity
    data['regulationMark'] = regulationMark
    data['cardImgURL'] = cardImgURL
    data['cardPageURL'] = url
    
    return data

