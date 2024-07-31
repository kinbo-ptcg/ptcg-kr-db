# 지금까지는 cardID = {포켓몬이름2자}{타입1자}{체력3자}{첫기술이름2자}{데미지3자}
# 이렇게 하니까 다른카드사이의 중복이 많이 발생한다
# 시험으로 {첫기술이름2자} -> {마지막기술이름2자} 로 바꾸어보자

import json
import csv
import os
import io
import re
from collections import Counter

CARDDATA_ROOT = '../../ptcg_kr_card_data_test/'

def to_three_digit(x):
    if x >= 100 :
        return str(x)
    elif x >= 10 :
        return "0" + str(x)
    else :
        return "00" + str(x)

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
            attack_name = attacks[-1]['name'].replace(' ','').strip()
            if len(attack_name) == 1:
                cardID += attack_name + attack_name
            else:
                cardID += attack_name[:2]

            attack_damage = attacks[-1]['damage']
            if attack_damage:
                cardID += to_three_digit(int(re.findall(r'\d+',attack_damage)[0]))
            else:
                cardID += to_three_digit(0)
        else:
            cardID += '없음'
            cardID += '000'

        return cardID
        
def fix_cardID():
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                id_count = 0
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            if item['cardID'] != gen_cardID(item):
                                item['cardID'] = gen_cardID(item)
                                id_count += 1
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
                if id_count > 0:
                    with open(file_path,'w',encoding='utf-8') as out_file:
                        json.dump(data,out_file,ensure_ascii=False, indent =4) 
                       
# 마지막기술으로는 오히려 문제가 악화 
# -1: cardID = {포켓몬이름2자}{타입1자}{체력3자}{첫기술이름2자}{데미지3자}
# 0: cardID = {포켓몬이름2자}{타입1자}{체력3자}{마지막기술이름2자}{데미지3자}
# 1: cardID = {포켓몬이름2자}{타입1자}{체력3자}({i번째기술이름2자}{데미지3자})_{i=1~len}
# 2: cardID = {포켓몬이름2자}{타입1자}{체력3자}(첫번째특수능력이름2자)({i번째기술이름2자}{데미지3자})_{i=1~len}
def gen_cardID_ver1(item):
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
            for i in range(len(attacks)):
                attack_name = attacks[i]['name'].replace(' ','').strip()
                if len(attack_name) == 1:
                    cardID += attack_name + attack_name
                else:
                    cardID += attack_name[:2]

                attack_damage = attacks[i]['damage']
                if attack_damage:
                    cardID += to_three_digit(int(re.findall(r'\d+',attack_damage)[0]))
                else:
                    cardID += to_three_digit(0)
        else:
            cardID += '없음'
            cardID += '000'

        return cardID
        
def fix_cardID_ver1():
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                id_count = 0
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            if item['cardID'] != gen_cardID_ver1(item):
                                item['cardID'] = gen_cardID_ver1(item)
                                id_count += 1
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
                if id_count > 0:
                    with open(file_path,'w',encoding='utf-8') as out_file:
                        json.dump(data,out_file,ensure_ascii=False, indent =4) 
                        
# 2: cardID = {포켓몬이름2자}{타입1자}{체력3자}(첫번째특수능력이름2자)({i번째기술이름2자}{데미지3자})_{i=1~len}
def gen_cardID_ver2(item):
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
        abilitites = item['abilities']
    
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
        
        # 특수능력 있으면 첫번째것 두글자
        if len(abilitites) != 0:
            abil_name = abilitites[0]['name'].replace(' ','').strip()
            if len(abil_name) == 1:
                cardID += abil_name + abil_name
            else:
                cardID += abil_name[:2]
    
        # 첫기술 이름 앞 두글자
        # 데미지 세글자
        # 기술이 없을때도 예외처리
        # 기술명 한글자는 두번반복, 공백있으면 다 삭제
        if len(attacks) != 0:
            for i in range(len(attacks)):
                attack_name = attacks[i]['name'].replace(' ','').strip()
                if len(attack_name) == 1:
                    cardID += attack_name + attack_name
                else:
                    cardID += attack_name[:2]

                attack_damage = attacks[i]['damage']
                if attack_damage:
                    cardID += to_three_digit(int(re.findall(r'\d+',attack_damage)[0]))
                else:
                    cardID += to_three_digit(0)
        else:
            cardID += '없음'
            cardID += '000'

        return cardID
        
def fix_cardID_ver2():
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                id_count = 0
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            if item['cardID'] != gen_cardID_ver2(item):
                                item['cardID'] = gen_cardID_ver2(item)
                                id_count += 1
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
                if id_count > 0:
                    with open(file_path,'w',encoding='utf-8') as out_file:
                        json.dump(data,out_file,ensure_ascii=False, indent =4) 

if __name__ == "__main__":
    #fix_cardID()
    #fix_cardID_ver1()
    fix_cardID_ver2()