import json
import copy
import os

CARDDATA_ROOT = '../../ptcg_kr_card_data/'

def is_promo(item):
    non_promo_keywords = ['BS','ST']
    if any(key in item['cardPageURL'] for key in non_promo_keywords):
        return False
    else:
        return True
        
def is_basic_energy(item):
    name = item['name']
    return '기본' in name and '에너지' in name

def find_BE(data):
    have_BE = False
    for item in data:
        if is_basic_energy(item):
            have_BE = True
    
    return have_BE

# 기본에너지는 레귤레이션 불문하고 사용가능한 물건
# 그러므로 regulationMark 를 Basic Energy 의 약자인 BE로 통일한다.
def basic_energy_regu():
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        have_BE = find_BE(data)
                        json_data = []
                        if have_BE:
                            for item in data:
                                if is_basic_energy(item):
                                    item["regulationMark"] = 'BE'
                                json_data.append(item)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
                if len(json_data) > 0:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(json_data, file, ensure_ascii=False, indent=4)
                        
#유일하게 레규레이션 정보가 공란인 상품  
CARDDATA_ROOT = '../../ptcg_kr_card_data/'
ME_GE_DIR = 'ST/2013/ST_2013_006_034.json'
  
def mewtwo_geno_regu(): 
    PATH = CARDDATA_ROOT + ME_GE_DIR
    
    with open(PATH, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        json_data = []
        for item in data:
            if item['prodName'] == "포켓몬 카드 게임 BW 「30장 덱 대전 set 뮤츠VS게노세크트」":
                item["regulationMark"] = 'BW'
            json_data.append(item)
            
    if len(json_data) > 0:
        with open(PATH, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        print('done')
        
#DP, BW 레규레이션 부여하기

# 하나라도 상품명에 DP가지는지 확인.
# 물론 미래의 프로모도 여기서 걸리낟.
def is_DP(data):
    for item in data:
        if "DP" in item['prodName']:
            return True
    return False

def check_conti(lst):
    if not lst:
        return False, False
    
    min_value = min(lst)
    max_value = max(lst)
    
    # 최소값이 0,1인지 체크
    min_is_one = (min_value in [0,1])

    # 최솟값부터 최댓값까지의 모든 숫자가 리스트에 있는지 확인
    return min_is_one, set(lst) == set(range(min_value, max_value + 1))

def DP_regu():
    base_directory = CARDDATA_ROOT
    DP_prod_set = set()

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        if is_DP(data):
                            # DP상품은 2010년에만 발매 되었다.
                            if '2010' in file_path:
                                json_data = []
                                for item in data:
                                    if not is_basic_energy(item):
                                        item["regulationMark"] = 'DP'
                                    json_data.append(item)
                                with open(file_path,'w', encoding='utf-8') as file:
                                    json.dump(json_data,file,ensure_ascii=False, indent=4)
                                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
               
def is_BW(data):
    for item in data:
        if "BW" in item['prodName']:
            return True
    return False
     
def BW_regu():
    base_directory = CARDDATA_ROOT
    bw_prod_names = set()

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        if is_BW(data):
                            json_data = []
                            for item in data:
                                bw_prod_names.add(file_path.split('/')[-1] + " : " + item['prodName'] + " : " + item['regulationMark'])
                                if not is_basic_energy(item):
                                    item["regulationMark"] = 'BW'
                                json_data.append(item)
                                
                                with open(file_path,'w', encoding='utf-8') as file:
                                    json.dump(json_data,file,ensure_ascii=False, indent=4)
                                    
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
        
if __name__ == "__main__":
    #basic_energy_regu()
    #mewtwo_geno_regu()
    #DP_regu()
    #BW_regu()
    
    print('hello')
    