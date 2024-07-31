import os
import json
from datetime import datetime
import pprint
import re

# 일단 세가지를 달성하고 싶다
# 1. product_info_1_647 의 기준에 따라서 pack, deck, special 으로 상품나누고, 상품별로 들어있는 카드를 모아둔다
#       결과적으론 card_data/[pack,deck,special]/[series]/[product_code].json
#       라는 폴더 구조를 가진다.
#       ?? 각각의 상품은 하나의 파일에서만 다루고 있나?
#       ?? 우선 이걸 체크해보자
#       !! 확인!! 
# 썬&문 강화 확장팩 「GX 배틀부스트 REMASTER」
# 썬&문 프로모 카드 키스틱 포켓몬 
############################################################
#       확인해서 넣을 내용
#           1. num_conti : item['number']이 1부터 끝까지 이어져 있는지
# 2. 상품정보를 카드리스트 포함해서 더 상세하게
#       product_info/[pack,deck,special]/[series]/[product_code].json
#       각각의 상품정보 넣기
#           1. num_max : 가장큰 item['number']
#           2. prod_num : 카드 종류
#           3. prod_code : bw2같은거
#           4. prod_smb_url : 문양이미지
#           5. name : 상품명
#           6. prod_info : 1_647 파일에 있는 정보
# 3. 포켓몬별 카드 파일 나누기->이건 다른파일로
#       product_info/[gen]/[dexnum_pokemon].json

ALL_CARD_DIR = './all_card_data.json'
PRODUCT_INFO_DIR = '../product_info/product_info_cards.json'

# dict_list의 원소중에서
# item[search_key] == search_ele 인 것의 item[target_key] 반환
EXCEPTION_PRODNAME_DICT={
    'BW 「플라스마단 덱」' : '포켓몬 카드 게임 BW 「플라스마단 스페셜 세트」',
    'BW 「케르디오 덱」' : '포켓몬 카드 게임 BW 트레이너 세트 「케르디오」'
}

def search_in_dict_list(dict_list,search_key,search_ele,target_key):
    if search_ele in EXCEPTION_PRODNAME_DICT:
        search_ele = EXCEPTION_PRODNAME_DICT[search_ele]
        
    result = [item[target_key] for item in dict_list if item.get(search_key) == search_ele]

    if result:
        return result[0]
    else:
        if 'DP' not in search_ele:
            print(search_key, search_ele,target_key)
        return target_key + " not found"
    
# DP의 경우, 제품 정보가 없다.
def get_type(product_info, item):
    type_ = search_in_dict_list(product_info,'name',item['prodName'].strip(),'type')
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
    else: #기본에너지의 BE만 남음
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

# card_list_detail = [objs] 포함된 카드의 상세정보(요약판)
#       num : 카드번호
#       prod_num : 카드 종류
#       name : 카드 이름
#       supertype : 카드 분류
#       subtypes : 카드 상세 분류
#       type : (포켓몬일때) 타입
#       pokemons : (포켓몬일때) 포켓몬 리스트
#       rarity : 레어리티
#       regulation : 레규레이션
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
    
def set_regu_list(item, empty=False, regu_list = []):
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
    
    # 불러오기
    with open(ALL_CARD_DIR, mode='r', encoding='utf-8') as file:
        all_card_data = json.load(file)
    with open(PRODUCT_INFO_DIR, mode='r', encoding='utf-8') as file:
        product_info = json.load(file)
        
    # 상품별 데이터 담기
    # code : 상품코드
    # name : 상품명
    # type : 상품 종류
    
    # printed_total : 카드 종류
    # total : 고레어등을 포함한 카드 종류
    
    # series : 팩에 포함된 카드들의 시리즈 정보
    # regulations : 팩에 포함된 카드의 레규정보
    # in_standard_regu : 현행레규인 FGH를 포함하는가?
    
    # release_date : 발매일
    # update_date : 갱신일
    
    # price : 가격정보
    # contents : 상품 내용물
    # caution : 주의
    
    # prod_url : 제품소개 페이지 url 
    # image_symbol_url : 제품 심볼이미지 url
    # image_cover_url : 제품 커버 이미지
    
    # card_list_index = [indexs] 포함된 카드의 all_card_data.json 에서의 리스트 인덱스
    # card_list_detail = [objs] 포함된 카드의 상세정보(요약판)
    #       num : 카드번호
    #       prod_num : 카드 종류
    #       name : 카드 이름
    #       supertype : 카드 분류
    #       subtypes : 카드 상세 분류
    #       type : (포켓몬일때) 타입
    #       pokemons : (포켓몬일때) 포켓몬 리스트
    #       rarity : 레어리티
    #       regulation : 레규레이션
    
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
                product_info_extended[code]['regulations'] = set_regu_list(item,regu_list=product_info_extended[code]['regulations'])
                product_info_extended[code]['in_standard_regu'] = product_info_extended[code]['in_standard_regu'] or is_stan_regu(item)

                product_info_extended[code]['card_list_index'].append(index)
                product_info_extended[code]['card_list_detail'].append(summary_card_data(item))
        else:
            if code not in product_info_extended:
                product_item = {}
                product_item['code'] = code
                product_item['name'] = item['prodName']
                product_item['type'] = get_type(product_info,item)

                product_item['printed_total'] = item['prodNumber']
                product_item['total'] = 1

                product_item['series'] = get_series(item)
                product_item['regulations'] = set_regu_list(item, empty=True)
                product_item['in_standard_regu'] = is_stan_regu(item)

                product_item['release_date'] = search_in_dict_list(product_info,'name',item['prodName'],'releaseDate')
                product_item['update_date'] = datetime.now().strftime("%Y-%m-%d")

                product_item['price'] = search_in_dict_list(product_info,'name',item['prodName'],'price')
                product_item['contents'] = search_in_dict_list(product_info,'name',item['prodName'],'contents')
                product_item['caution'] = search_in_dict_list(product_info,'name',item['prodName'],'caution')

                product_item['prod_url'] = search_in_dict_list(product_info,'name',item['prodName'],'url')
                product_item['image_symbol_url'] = item["prodSymbolURL"]
                product_item['image_cover_url'] = search_in_dict_list(product_info,'name',item['prodName'],"cover_url")

                product_item['card_list_index'] = [index]
                product_item['card_list_detail'] = [summary_card_data(item)]

                product_info_extended[code] = product_item
            else:
                product_info_extended[code]['total'] += 1

                product_info_extended[code]['series'] = list(set(product_info_extended[code]['series']) | set(get_series(item)))
                product_info_extended[code]['regulations'] = set_regu_list(item,regu_list=product_info_extended[code]['regulations'])
                product_info_extended[code]['in_standard_regu'] = product_info_extended[code]['in_standard_regu'] or is_stan_regu(item)

                product_info_extended[code]['card_list_index'].append(index)
                product_info_extended[code]['card_list_detail'].append(summary_card_data(item))
        
    return all_card_data, product_info_extended
    
# 카드 숫자가 맞는지 확인
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
    
# /card_data_product 채우기
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
    file_write_flag = True # 이게 False이면 파일작성 안한다
    
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
        
        ### 파일 내용 처리
        json_data = []
        indexs = product_info[key]['card_list_index']
        
        for i in indexs:
            json_data.append(all_card_data[i])
            
        json_data.sort(key=lambda x:int(x['number']))
        ######
        
        if file_path not in json_data_all:
            json_data_all[file_path] = json_data
        else:
            file_write_flag = False
            print('key duplicate : product_info')
            break
        
    if file_write_flag:
        for path in json_data_all:
            with open(path,'w',encoding='utf-8') as f:
                json.dump(json_data_all[path],f,ensure_ascii=False,indent=4)
        print("card_data_product done")
    else:
        print("something wrong?")
        
# /product_data 채우기
PRODUCT_DATA_DIR = '../../product_data/'

def is_valid_date_format(date_str):
    # YYYY-mm-dd 형식을 확인하는 정규 표현식
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    
    return bool(re.match(date_pattern, date_str))

def gen_product_data(all_card_data, product_info):
    json_data_all = {}
    file_write_flag = True # 이게 False이면 파일작성 안한다
    
    for key in product_info:
        product_type = product_info[key]['type']
        product_series = get_product_series(product_info[key]['series'])

        file_dir = PRODUCT_DATA_DIR + product_type + '/'
        file_name = product_series+ '.json'
        file_path = file_dir + file_name

        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            
        if file_path not in json_data_all:
            json_data_all[file_path] = [product_info[key]]
        else:
            json_data_all[file_path].append(product_info[key])
            
    for path in json_data_all:
        json_data = json_data_all[path]

        # 날짜 형식 체크
        for item in json_data:
            if not is_valid_date_format(item['release_date']):
                item['release_date'] = '1970-01-01'
                
        # 날짜순 정렬
        json_data = sorted(json_data, key = lambda x: datetime.strptime(x.get('release_date', '1970-01-01'), "%Y-%m-%d"))

        with open(path,'w',encoding='utf-8') as f:
            #json.dump(json_data_all[path],f,ensure_ascii=False,indent=4)
            json.dump(json_data,f,ensure_ascii=False,indent=4)

    print("product_data done")

if __name__ == "__main__":
    # 우선 오브젝트 만들기
    all_card_data, product_info = classify_cards_by_product()
    #count_card_num(all_card_data,product_info)
    
    # 그 오브젝트로 card_data_product 채우기
    gen_card_data_product(all_card_data, product_info)
    
    # 그 오브젝트로 product_data 채우기
    gen_product_data(all_card_data, product_info)