import json
import csv

error_text = '''
card text,https://pokemoncard.co.kr/cards/detail/BS2010001045
card text,https://pokemoncard.co.kr/cards/detail/BS2010002009
card text,https://pokemoncard.co.kr/cards/detail/BS2010002019
card text,https://pokemoncard.co.kr/cards/detail/BS2010002026
card text,https://pokemoncard.co.kr/cards/detail/BS2010002032
card text,https://pokemoncard.co.kr/cards/detail/BS2010002033
card text,https://pokemoncard.co.kr/cards/detail/BS2010003006
card text,https://pokemoncard.co.kr/cards/detail/BS2010004003
card text,https://pokemoncard.co.kr/cards/detail/BS2010004032
card text,https://pokemoncard.co.kr/cards/detail/BS2010004035
card text,https://pokemoncard.co.kr/cards/detail/BS2010005009
card text,https://pokemoncard.co.kr/cards/detail/BS2010005014
card text,https://pokemoncard.co.kr/cards/detail/BS2010005033
card text,https://pokemoncard.co.kr/cards/detail/BS2010006033
card text,https://pokemoncard.co.kr/cards/detail/BS2010006042
card text,https://pokemoncard.co.kr/cards/detail/BS2010007019
card text,https://pokemoncard.co.kr/cards/detail/BS2010007036
card text,https://pokemoncard.co.kr/cards/detail/BS2010009006
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002001
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002002
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002003
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002004
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002005
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002031
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002032
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002033
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002034
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002035
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002036
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002037
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002043
resi value,https://pokemoncard.co.kr/cards/detail/BS2013002044
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003004
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003005
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003006
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003028
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003031
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003032
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003033
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003034
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003035
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003036
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003037
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003043
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003044
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003045
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003046
resi value,https://pokemoncard.co.kr/cards/detail/BS2013003054
attack tool,https://pokemoncard.co.kr/cards/detail/BS2013005073
attack tool,https://pokemoncard.co.kr/cards/detail/BS2013005074
resi value,https://pokemoncard.co.kr/cards/detail/BS2013006087
card text,https://pokemoncard.co.kr/cards/detail/BS2014002001
card text,https://pokemoncard.co.kr/cards/detail/BS2014002002
card text,https://pokemoncard.co.kr/cards/detail/BS2014002007
card text,https://pokemoncard.co.kr/cards/detail/BS2014002015
card text,https://pokemoncard.co.kr/cards/detail/BS2014002016
card text,https://pokemoncard.co.kr/cards/detail/BS2014002018
card text,https://pokemoncard.co.kr/cards/detail/BS2014002035
card text,https://pokemoncard.co.kr/cards/detail/BS2014002049
card text,https://pokemoncard.co.kr/cards/detail/BS2014002052
card text,https://pokemoncard.co.kr/cards/detail/BS2014002055
card text,https://pokemoncard.co.kr/cards/detail/BS2014002057
card text,https://pokemoncard.co.kr/cards/detail/BS2014002060
card text,https://pokemoncard.co.kr/cards/detail/BS2014002065
card text,https://pokemoncard.co.kr/cards/detail/BS2014002066
card text,https://pokemoncard.co.kr/cards/detail/BS2014002071
card text,https://pokemoncard.co.kr/cards/detail/BS2014003003
card text,https://pokemoncard.co.kr/cards/detail/BS2014003005
card text,https://pokemoncard.co.kr/cards/detail/BS2014003018
card text,https://pokemoncard.co.kr/cards/detail/BS2014003026
card text,https://pokemoncard.co.kr/cards/detail/BS2014003035
card text,https://pokemoncard.co.kr/cards/detail/BS2014003039
card text,https://pokemoncard.co.kr/cards/detail/BS2014003044
card text,https://pokemoncard.co.kr/cards/detail/BS2014003050
card text,https://pokemoncard.co.kr/cards/detail/BS2014003060
card text,https://pokemoncard.co.kr/cards/detail/BS2014003068
card text,https://pokemoncard.co.kr/cards/detail/BS2014003069
card text,https://pokemoncard.co.kr/cards/detail/BS2014003072
card text,https://pokemoncard.co.kr/cards/detail/BS2014003075
card text,https://pokemoncard.co.kr/cards/detail/BS2016004023
card text,https://pokemoncard.co.kr/cards/detail/BS2016004025
card text,https://pokemoncard.co.kr/cards/detail/BS2016004028
card text,https://pokemoncard.co.kr/cards/detail/BS2016004071
card text,https://pokemoncard.co.kr/cards/detail/BS2016004071
card text,https://pokemoncard.co.kr/cards/detail/BS2016004085
card text,https://pokemoncard.co.kr/cards/detail/BS2016007044
card text,https://pokemoncard.co.kr/cards/detail/BS2016020012
artist info,https://pokemoncard.co.kr/cards/detail/BS2018003066
resi value,https://pokemoncard.co.kr/cards/detail/BS2018004032
resi value,https://pokemoncard.co.kr/cards/detail/BS2018004033
resi value,https://pokemoncard.co.kr/cards/detail/BS2018004034
resi value,https://pokemoncard.co.kr/cards/detail/BS2018004035
resi value,https://pokemoncard.co.kr/cards/detail/BS2018004047
weak value,https://pokemoncard.co.kr/cards/detail/BS2018009017
card text,https://pokemoncard.co.kr/cards/detail/BS2019010013
attack tool,https://pokemoncard.co.kr/cards/detail/BS2019011044
attack tool,https://pokemoncard.co.kr/cards/detail/BS2019011045
card text,https://pokemoncard.co.kr/cards/detail/BS2019012011
card text,https://pokemoncard.co.kr/cards/detail/BS2019016051
card text,https://pokemoncard.co.kr/cards/detail/BS2019017032
ability text,https://pokemoncard.co.kr/cards/detail/BS2019017033
prod_name,https://pokemoncard.co.kr/cards/detail/BS2020001054
check pokemons,https://pokemoncard.co.kr/cards/detail/BS2022014067
attack tool,https://pokemoncard.co.kr/cards/detail/BS2022017091
attack tool,https://pokemoncard.co.kr/cards/detail/BS2023020055
attack tool,https://pokemoncard.co.kr/cards/detail/BS2023020056
attack tool,https://pokemoncard.co.kr/cards/detail/BS2023021061
attack tool,https://pokemoncard.co.kr/cards/detail/BS2023022061
card text,https://pokemoncard.co.kr/cards/detail/ST2011005001
resi value,https://pokemoncard.co.kr/cards/detail/ST2013005005
card text,https://pokemoncard.co.kr/cards/detail/BS201707028
'''
import io
import re
from collections import Counter

def to_three_digit(x):
    if x >= 100 :
        return str(x)
    elif x >= 10 :
        return "0" + str(x)
    else :
        return "00" + str(x)
    
def make_error_edit():
    # error_text를 CSV 데이터로 변환
    csv_reader = csv.reader(io.StringIO(error_text.strip()))

    # CSV 데이터를 리스트로 변환
    error_data = list(csv_reader)
    json_data = []
    
    for item in error_data:
        json_item = {}
        json_item['type'] = item[0]
        
        id_part = item[1].split('/')[-1]
        letters = re.findall(r'[A-Za-z]+', id_part)
        numbers = re.findall(r'\d+', id_part)
        
        json_item['category'] = letters[0]
        
        numbers = numbers[0]
        if len(numbers) == 10:
            year = numbers[0:4]
            ver = numbers[4:7]
            num = numbers[7:10]
            json_item['year'] = year
            json_item['ver'] = ver
            json_item['num'] = num
            json_item['path'] = '../ptcg_kr_card_data/' + letters[0] +'/' +year + '/' + (letters[0]+'_'+year+'_'+ver+'_'+num+'.json')
        
        json_item['url'] = item[1]
        
        json_data.append(json_item)
        
    json_data = sorted(json_data,key = lambda x:x['url'])
    json_data = sorted(json_data,key = lambda x:x['type'])
    
    # 'type' 필드별로 개수 세기
    type_counts = Counter(item['type'] for item in json_data)

    # 결과 출력
    for type_value, count in type_counts.items():
        print(f"Type: {type_value}, Count: {count}")

    json_file_path = './error_edit.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent =4)
        
# 이미 에러가 발견되었는데, 코드의 개선으론 해결 안되는 것들을 모은 것.
# 사전이고, 키 : url 원소 : 이유

ERROR_URLS = {
'https://pokemoncard.co.kr/cards/detail/BS2024001006' : '특성마크 없음',
'https://pokemoncard.co.kr/cards/detail/BS2024001007' : '특성마크 없음',
'https://pokemoncard.co.kr/cards/detail/BS2024001196' : '특성마크 없음',
'https://pokemoncard.co.kr/cards/detail/BS2024001197' : '특성마크 없음',
'https://pokemoncard.co.kr/cards/detail/BS2015002033' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/BS2015002053' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/BS2015002056' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/BS2015002057' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/BS2015003025' : '공격하는 도구인데 기술 없음',
'https://pokemoncard.co.kr/cards/detail/BS2015003026' : '공격하는 도구인데 기술 없음',
'https://pokemoncard.co.kr/cards/detail/BS2018003060' : '일러레 정보 없음', 
'https://pokemoncard.co.kr/cards/detail/BS2021011061' : '공격하는 도구인데 기술 없음',
'https://pokemoncard.co.kr/cards/detail/BS2021012061' : '공격하는 도구인데 기술 없음',
'https://pokemoncard.co.kr/cards/detail/BS2021015025' : '일러레 정보 없음',
'https://pokemoncard.co.kr/cards/detail/BS2024009003' : '찬자몽 특성, 기술 에러',
'https://pokemoncard.co.kr/cards/detail/BS2024010003' : '찬개닌 특성, 기술 에러',
'https://pokemoncard.co.kr/cards/detail/ST2012001001' : '포켓몬인데 아이템 룰 있음',
'https://pokemoncard.co.kr/cards/detail/ST2012005001' : '포켓몬인데 아이템 룰 있음',
'https://pokemoncard.co.kr/cards/detail/PR2015001037' : '일러레 정보 없음',
'https://pokemoncard.co.kr/cards/detail/PR2015001038' : '일러레 정보 없음',
'https://pokemoncard.co.kr/cards/detail/PR2015001050' : '특성마크 없음',
'https://pokemoncard.co.kr/cards/detail/PR2015001063' : '특성마크 없음',
'https://pokemoncard.co.kr/cards/detail/ST2010001008' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/ST2010003003' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/ST2010001008' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/ST2011007001' : '포켓몬인데 아이템 룰 있음',
'https://pokemoncard.co.kr/cards/detail/ST2013001001' : '포켓몬인데 아이템 룰 있음',
'https://pokemoncard.co.kr/cards/detail/ST2016003006' : '루챠불 이라고 되어있음',
'https://pokemoncard.co.kr/cards/detail/ST2014001001' : '포켓몬인데 아이템 룰 있음',
'https://pokemoncard.co.kr/cards/detail/PR2010001005' : '기술 에너지,피해 없음',
'https://pokemoncard.co.kr/cards/detail/SVP000000061' : '기술 에너지,피해 없음', 
'https://pokemoncard.co.kr/cards/detail/SVP000000081' : '체력이 없음',
'https://pokemoncard.co.kr/cards/detail/SMP000000120' : '기술 에너지,피해 없음', 
'https://pokemoncard.co.kr/cards/detail/SMP000000130' : '상품정보 없음,승리의훈장',
'https://pokemoncard.co.kr/cards/detail/SMP000000131' : '상품정보 없음,승리의훈장',
'https://pokemoncard.co.kr/cards/detail/SMP000000132' : '상품정보 없음,승리의훈장',
'https://pokemoncard.co.kr/cards/detail/SMP000000133' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000134' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000135' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000136' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000137' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000138' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000139' : '상품정보 없음,보스피카츄',
'https://pokemoncard.co.kr/cards/detail/SMP000000141' : '상품정보 없음',
'https://pokemoncard.co.kr/cards/detail/SMP000000142' : '상품정보 없음, 기술도 이상',
'https://pokemoncard.co.kr/cards/detail/SMP000000157' : '상품정보 없음',
'https://pokemoncard.co.kr/cards/detail/SMP000000161' : '일러레 정보 없음',
'https://pokemoncard.co.kr/cards/detail/SMP000000194' : '일러레 정보 없음, 원래 없음'
}

def make_error_edit2():
    json_data = []
    
    for key_url in ERROR_URLS:
        json_item = {}
        json_item['type'] = ERROR_URLS[key_url]
        
        id_part = key_url.split('/')[-1]
        letters = re.findall(r'[A-Za-z]+', id_part)
        numbers = re.findall(r'\d+', id_part)
        
        json_item['category'] = letters[0]
        
        numbers = numbers[0]
        if len(numbers) == 10:
            year = numbers[0:4]
            ver = numbers[4:7]
            num = numbers[7:10]
            json_item['year'] = year
            json_item['ver'] = ver
            json_item['num'] = num
        
        json_item['url'] = key_url
        
        json_data.append(json_item)
        
    json_data = sorted(json_data,key = lambda x:x['url'])
    json_data = sorted(json_data,key = lambda x:x['type'])
    
    # 'type' 필드별로 개수 세기
    type_counts = Counter(item['type'] for item in json_data)

    # 결과 출력
    for type_value, count in type_counts.items():
        print(f"Type: {type_value}, Count: {count}")

    json_file_path = './error_edit2.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent =4)
        
# noATT :전체 훑어서 attack 없는 포켓몬 리스트 만들기, 다 확인",
# ATTcost : attack cost = '정보없음' 인거 리스트업",
# INFO : info 가 있는거 리스트업",
# CIDblank : cardID = blank 인거 리스트업",
# noARTI : artist = 정보없음 리스트업",
# ItemRU :공격 이름이 아이템 룰 인거 확인"]
CARDDATA_ROOT = '../ptcg_kr_card_data/'
import os

def noATT(item):
    if item.get('supertype') != '포켓몬':
        return False
    elif 'BREAK' in item['name']:
        return False
    elif len(item.get('attacks', [])) == 0:
        return True
    else:
        return False

def ATTcost(item):
    if item.get('supertype') != '포켓몬':
        return False
    elif any(attack.get('cost') == '정보없음' for attack in item.get('attacks', [{'cost': None}])):
        return True
    else:
        return False

def INFO(item):
    return item.get('info', 0) != 0

def CIDblank(item):
    return item.get('cardID',"") == ""

def noARTI(item):
    if item.get('supertype') == '에너지':
        return False
    else:
        return item.get('artist',"") == ""

def ItemRU(item):
    if item.get('supertype') != '포켓몬':
        return False
    elif any(attack.get('name') == '아이템 룰' for attack in item.get('attacks', [{'cost': None}])):
        return True
    else:
        return False
    
def write_err(item, err_list):
    url = item.get('cardPageURL',"")
    
    json_item = {}
    json_item['type'] = ', '.join(err_list)
    json_item['errNum'] = len(err_list)
    
    id_part = url.split('/')[-1]
    letters = re.findall(r'[A-Za-z]+', id_part)
    numbers = re.findall(r'\d+', id_part)

    json_item['category'] = letters[0]
    numbers = numbers[0]
    if len(numbers) == 10:
        year = numbers[0:4]
        ver = numbers[4:7]
        num = numbers[7:10]
        json_item['year'] = year
        json_item['ver'] = ver
        json_item['num'] = num
        
    json_item['url'] = url
    
    return json_item
  
def make_error_edit3():
    json_data = []
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            item_err_list = []
                            if noATT(item):
                                item_err_list.append('noATT')
                            if ATTcost(item):
                                item_err_list.append('ATTcost')
                            if INFO(item):
                                item_err_list.append('INFO')
                            if CIDblank(item):
                                item_err_list.append('CIDblank')
                            if noARTI(item):
                                item_err_list.append('noARTI')
                            if ItemRU(item):
                                item_err_list.append('ItemRU')
                            
                            if len(item_err_list) > 0:
                                json_data.append(write_err(item,item_err_list))
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
        
    json_data = sorted(json_data,key = lambda x:x['url'])
    json_data = sorted(json_data,key = lambda x:x['type'])
    
    # 'type' 필드별로 개수 세기
    type_counts = Counter(item['type'] for item in json_data)

    # 결과 출력
    for type_value, count in type_counts.items():
        print(f"Type: {type_value}, Count: {count}")

    json_file_path = './error_edit3.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent =4)        
        
# HPzero : HP = 0 인 포켓몬 찾기
# CIDform : cardID 가 단데풀070벌레030 같은 형식인가?
# Vstar : "VSTAR 파워\n파동스타" -> "파동스타"
# eptPOKE : 포켓몬이 비어있는? [] 이런게 있다

def HPzero(item):
    if item['supertype'] != '포켓몬':
        return False
    elif item['hp'] <= 0:
        return True
    else:
        return False
    
def CIDform(item):
    pattern = r'^\w{3,4}\d{3}\w{2}\d{3}$'
    isFormedCID = bool(re.match(pattern, item['cardID']))

    if item['supertype'] != '포켓몬':
        return False
    elif isFormedCID:
        return False
    else:
        return True
    
def Vstar(item):
    if item.get('supertype') != '포켓몬':
        return False
    elif any('VSTAR' in attack['name'] for attack in item.get('attacks', [{'name': None}])):
        return True
    else:
        return False
    
def eptPOKE(item):
    if item.get('supertype') != '포켓몬':
        return False
    elif len(item['pokemons']) == 0:
        return True
    else:
        return False
    
def make_error_edit4():
    json_data = []
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            item_err_list = []
                            if HPzero(item):
                                item_err_list.append('HPzero')
                            if CIDform(item):
                                item_err_list.append('CIDform')
                            if Vstar(item):
                                item_err_list.append('Vstar')
                            if eptPOKE(item):
                                item_err_list.append('eptPOKE')
                            if len(item_err_list) > 0:
                                json_data.append(write_err(item,item_err_list))
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
        
    json_data = sorted(json_data,key = lambda x:x['url'])
    json_data = sorted(json_data,key = lambda x:x['type'])
    
    # 'type' 필드별로 개수 세기
    type_counts = Counter(item['type'] for item in json_data)

    # 결과 출력
    for type_value, count in type_counts.items():
        print(f"Type: {type_value}, Count: {count}")

    json_file_path = './error_edit4.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent =4)    
    
# BS_2014_002_086, BS_2014_003_102 다틀림. 다 다시보기",
# BS_2013_002_054 기술 피해 싹 없음",
import requests

def download_BW_images():
    path_14_2 = '../ptcg_kr_card_data/BS/2014/BS_2014_002_086.json'
    path_14_3 = '../ptcg_kr_card_data/BS/2014/BS_2014_003_102.json'
    path_13_2 = '../ptcg_kr_card_data/BS/2013/BS_2013_002_054.json'
    
    img_14_2 = './img/img_14_2/'
    img_14_3 = './img/img_14_3/'
    img_13_2 = './img/img_13_2/'

    paths = [path_14_2,path_14_3,path_13_2]
    p_imgs = [img_14_2,img_14_3,img_13_2]
    
    for i in len(paths):
        path = paths[i]
        p_img = p_imgs[i]
        
        with open(path,mode='r',encoding='utf-8') as file:
            card_data = json.load(file)
            
        for item in card_data:
            img_url = item['cardImgURL']
            img_res = requests.get(img_url)
            img_res.raise_for_status()  # 요청이 성공했는지 확인
            
            img_file_name = str(item['number']) + '.jpg'
            
            with open(p_img + img_file_name,'wb') as img_f:
                img_f.write(img_res.content)
                
# 카드 id 내용 재대로 된건지 다시보기!!
# 기술명 한글자는 두번반복, 공백있으면 다 삭제
def gen_cardID(item):
    supertype = item.get('supertype','?')
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
        # 기술명 한글자는 두번반복, 공백있으면 다 삭제
        if len(attacks) != 0:
            attack_name = attacks[0]['name'].replace(' ','').strip()
            if len(attack_name) == 1:
                cardID += attack_name + attack_name
            else:
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
    
KNOWN_CID_ERRs = ["BS2014002","BS2014003","BS2013002"]

def make_error_edit5():
    json_data = []
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            item_err_list = []
                            if item['cardID'] != gen_cardID(item):
                                if any(err_key in item['cardPageURL'] for err_key in KNOWN_CID_ERRs):
                                    item_err_list.append('CID_known')
                                item_err_list.append('CID_bad')
                            if len(item_err_list) > 0:
                                json_data.append(write_err(item,item_err_list))
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
        
    json_data = sorted(json_data,key = lambda x:x['url'])
    json_data = sorted(json_data,key = lambda x:x['type'])
    
    # 'type' 필드별로 개수 세기
    type_counts = Counter(item['type'] for item in json_data)

    # 결과 출력
    for type_value, count in type_counts.items():
        print(f"Type: {type_value}, Count: {count}")

    json_file_path = './error_edit5.json'
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent =4)  
        
def fix_cardID():
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT
    test_out_directory = './test/'

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                err_count = 0
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            if item['cardID'] != gen_cardID(item):
                                item['cardID'] = gen_cardID(item)
                                err_count += 1
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
                if err_count > 0:
                    #output_file_path = os.path.join(test_out_directory, file)
                    with open(file_path,'w',encoding='utf-8') as out_file:
                        json.dump(data,out_file,ensure_ascii=False, indent =4) 

def download_SUN_images():
    path_sun = '../../../ptcg_kr_card_data/BS/2017/BS_2017_001_066.json'
    
    img_sun = './img/img_sun/'

    paths = [path_sun]
    p_imgs = [img_sun]
    
    for i in range(len(paths)):
        path = paths[i]
        p_img = p_imgs[i]
        
        with open(path,mode='r',encoding='utf-8') as file:
            card_data = json.load(file)
            
        for item in card_data:
            img_url = item['cardImgURL']
            img_res = requests.get(img_url)
            img_res.raise_for_status()  # 요청이 성공했는지 확인
            
            img_file_name = str(item['number']) + '.jpg'
            
            with open(p_img + img_file_name,'wb') as img_f:
                img_f.write(img_res.content)

if __name__ == "__main__":
    #make_error_edit()
    #make_error_edit2()
    #make_error_edit3()
    
    #make_error_edit4()
    #download_BW_images()
    
    #make_error_edit5()
    #fix_cardID()
    
    download_SUN_images()

    