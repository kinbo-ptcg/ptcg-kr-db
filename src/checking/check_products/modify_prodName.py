import json
import csv

def modify_changgong():
    file_name = '../../ptcg_kr_card_data/BS/2021/BS_2021_012_067.json'
    
    with open(file_name,mode='r',encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        if item['prodName'] == "소드 & 실드   확장팩   「창공스트림」":
            item['prodName'] = '소드&실드 확장팩 「창공스트림」'
            
    with open(file_name,mode='w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False, indent=4)
        
def modify_paradaim():
    file_name = '../../ptcg_kr_card_data/BS/2022/BS_2022_017_125.json'
    
    with open(file_name,mode='r',encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        if item['prodName'] == "소드 & 실드   확장팩   「패러다임트리거」":
            item['prodName'] = "소드&실드 확장팩 「패러다임트리거」"
            
    with open(file_name,mode='w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False, indent=4)
        
def modify_pikaeve():
    file_name = '../../ptcg_kr_card_data/BS/2022/BS_2022_009_025.json'
    
    with open(file_name,mode='r',encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        if item['prodName'] == "소드 & 실드   「스타트   덱  100  피카츄  V &  이브이  V 」":
            item['prodName'] = "소드&실드 「스타트 덱 100 피카츄 V & 이브이 V」"
            
    with open(file_name,mode='w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False, indent=4)

def modify_dragon_chal():
    file_name = '../../ptcg_kr_card_data/SP/0/SP_0_000_191.json'
    
    with open(file_name,mode='r',encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        if item['prodName'] == "드래곤   포켓몬  V GET  챌린지   프로모   카드   팩":
            item['prodName'] = "드래곤 포켓몬 V GET 챌린지 프로모 카드 팩"
            
    with open(file_name,mode='w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False, indent=4)
        
def modify_prodname(dir,before,after):
    with open(dir,mode='r',encoding='utf-8') as file:
        data = json.load(file)
        
    for item in data:
        if item['prodName'] == before:
            item['prodName'] = after
    
    with open(dir,mode='w',encoding='utf-8') as file:
        json.dump(data,file,ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    # 1의 창공스트림 이름이
    # "소드 & 실드   확장팩   「창공스트림」"
    # 이걸
    # 소드&실드 확장팩 「창공스트림」
    # 이렇게 고치기
    # 패러다임트리거도
    #modify_changgong()
    #modify_paradaim()
    
    # 카드 정보에 있는 이것을
    # "소드 & 실드   「스타트   덱  100  피카츄  V &  이브이  V 」"
    # 이걸로
    # "소드&실드 「스타트 덱 100 피카츄 V & 이브이 V」"
    # modify_pikaeve()
    
    # 드래곤 챌린지
    # "드래곤   포켓몬  V GET  챌린지   프로모   카드   팩"
    # 를
    # "드래곤 포켓몬 V GET 챌린지 프로모 카드 팩"
    # modify_dragon_chal()
    
    # ../../ptcg_kr_card_data/BS/2022/BS_2022_006_021.json
    # "소드 & 실드   스타터   세트  VSTAR  「다크라이」" -> "소드&실드 스타터 세트 VSTAR 「다크라이」"
    # modify_prodname('../../ptcg_kr_card_data/BS/2022/BS_2022_006_021.json',"소드 & 실드   스타터   세트  VSTAR  「다크라이」","소드&실드 스타터 세트 VSTAR 「다크라이」")
    
    # ../../ptcg_kr_card_data/BS/2022/BS_2022_005_022.json
    # "소드 & 실드   스타터   세트  VSTAR  「루카리오」" -> "소드&실드 스타터 세트 VSTAR 「루카리오」"
    # modify_prodname('../../ptcg_kr_card_data/BS/2022/BS_2022_005_022.json',"소드 & 실드   스타터   세트  VSTAR  「루카리오」", "소드&실드 스타터 세트 VSTAR 「루카리오」")
    
    # '../../ptcg_kr_card_data/BS/2021/BS_2021_009_023.json', "소드 & 실드   하이클래스   덱   「인텔리레온  VMAX 」", "소드&실드 하이클래스 덱 「인텔리레온  VMAX 」"
    modify_prodname('../../ptcg_kr_card_data/BS/2021/BS_2021_009_023.json', "소드 & 실드   하이클래스   덱   「인텔리레온  VMAX 」", "소드&실드 하이클래스 덱 「인텔리레온  VMAX 」")
    # '../../ptcg_kr_card_data/BS/2021/BS_2021_008_020.json', "소드 & 실드   하이클래스   덱   「팬텀  VMAX 」" , "소드&실드 하이클래스 덱  「팬텀  VMAX 」"
    modify_prodname('../../ptcg_kr_card_data/BS/2021/BS_2021_008_020.json', "소드 & 실드   하이클래스   덱   「팬텀  VMAX 」" , "소드&실드 하이클래스 덱  「팬텀  VMAX 」")
    
    # '' , "스타터   세트  VMAX  구입특전", "스타터 세트  VMAX  구입특전"

