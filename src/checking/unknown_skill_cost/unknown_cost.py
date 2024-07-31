# 간혹 이미지url 오류로 인해 기술의 코스트가 (?) 로 인코딩 된게 있다.
# 그런걸 리스팅한다.

# 로직을 잘못짜서, 피카츄, 로토무의 경우에는 pokemons에 두개 들어있는 경우가 있다.
# 이런게 발견되면 지우는 코드.

import json
import csv
import os
import io
import re
from collections import Counter
import pprint

CARDDATA_ROOT = '../../ptcg_kr_card_data/'
    
def is_double_pika_roto(item):
    supertype = item.get('supertype','?')
    if supertype == '?':
        print("ERROR : supertype")
        print(item['url'])
        return False
    elif supertype != '포켓몬':
        return False
    else:
        pokemons = item['pokemons']
        if len(pokemons) == 1:
            return False
        else:
            is_pika_roto = 'nobody'
            for pokemon in pokemons:
                if pokemon['name'] == '피카츄':
                    is_pika_roto = 'pika'
                elif pokemon['name'] == '로토무':
                    is_pika_roto = 'roto'

            if is_pika_roto == 'nobody':
                return False
            else:
                print('pika roto')
                if is_pika_roto == 'pika' and len(pokemons) == 2:
                    return pokemons[0]['name'] == pokemons[1]['name']
                elif is_pika_roto == 'roto' and len(pokemons) == 2:
                    return pokemons[0]['name'] == pokemons[1]['name']
                
def multi_pokemons(item):
    supertype = item.get('supertype','?')
    if supertype == '?':
        print("ERROR : supertype")
        print(item['url'])
        return False
    elif supertype != '포켓몬':
        return False
    else:
        pokemons = item['pokemons']
        if len(pokemons) != 1:
            if 'TAG TEAM' in item['subtypes']:
                return False
            else:
                if '피카츄' not in item['name'] and '로토무' not in item['name']:
                    print('not pika,roto')
                    #pprint.pprint(item)
                    return False
                #pprint.pprint(item)
                return True
        return False                
        
def do_pika_roto(item):
    if not multi_pokemons(item):
        print('not multi')
        return item['pokemons']
    else:
        pokemons = item['pokemons']
        if pokemons[0]['name'] == '피카츄':
            return [{'name': '피카츄', 'pokedexNumber': 25}]
        elif pokemons[0]['name'] == '로토무':
            return [{'name': '로토무', 'pokedexNumber': 479}]
        else:
            print('?????????')
            return item['pokemons']
        
def is_unknown_cost(item):
    supertype = item.get('supertype','?')
    if supertype == '?':
        print("ERROR : supertype")
        print(item['url'])
        return False
    elif supertype != '포켓몬':
        return False
    else:
        attacks = item['attacks']
        for attack in attacks:
            cost = attack['cost']
            if '(?)' in cost:
                return True
        return False
        
        
def remove_unknown_cost():
    # JSON 파일들이 저장된 디렉토리 경로
    base_directory = CARDDATA_ROOT
    unknown_cost_count = 0

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                #unknown_cost_count = 0
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        for item in data:
                            if is_unknown_cost(item):
                                #item['pokemons'] = do_pika_roto(item)
                                pprint.pprint(item)
                                unknown_cost_count += 1
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
                #if unknown_cost_count > 0:
                #    with open(file_path,'w',encoding='utf-8') as out_file:
                #        json.dump(data,out_file,ensure_ascii=False, indent =4) 
    
    print(unknown_cost_count)

if __name__ == "__main__":
    remove_unknown_cost()