import json
import copy
import os

CARDDATA_ROOT = '../../ptcg_kr_card_data/'
CHECK_REGUS = ['a','none','']

def is_promo(item):
    non_promo_keywords = ['BS','ST','GX']
    if any(key in item['cardPageURL'] for key in non_promo_keywords):
        return False
    else:
        return True
    
def check_regu():
    base_directory = CARDDATA_ROOT

    json_data = []
    json_data_a = []
    json_data_none = []
    json_data_empty = []
    json_data_baseEN = []
    
    set_a = set()
    set_none = set()
    set_empty = set()
    set_ene = set()
    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        for item in data:
                            if is_promo(item):
                                continue
                            else:
                                regu = item['regulationMark']
                                if regu == 'a':
                                    #if '기본' in item['name'] and '에너지' in item['name']:
                                        #json_data_baseEN.append(item)
                                        #set_ene.add(item['prodName'])
                                    #else:
                                        #json_data_a.append(item)
                                    set_a.add(item['cardPageURL'])
                                elif regu == 'none':
                                    if '기본' in item['name'] and '에너지' in item['name']:
                                        #json_data_baseEN.append(item)
                                        set_ene.add(item['prodName'])
                                    else:
                                        #json_data_none.append(item)
                                        set_none.add(item['prodName'])
                                elif regu == '':
                                    if '기본' in item['name'] and '에너지' in item['name']:
                                        #json_data_baseEN.append(item)
                                        set_ene.add(item['prodName'])
                                    else:
                                        #json_data_empty.append(item)
                                        set_empty.add(item['prodName'])
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    # 각각의 확인할 레규의 카드정보 출력                        
    #json_data_a = sorted(json_data_a, key = lambda x:x['prodName'])
    json_data_a = sorted(list(set_a))
    OUTPUT_FILE = 'regu_a.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data_a, out_file, ensure_ascii=False, indent=4)  
        
    #json_data_none = sorted(json_data_none, key = lambda x:x['prodName'])
    json_data_none = sorted(list(set_none))
    OUTPUT_FILE = 'regu_none.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data_none, out_file, ensure_ascii=False, indent=4)
        
    #json_data_empty = sorted(json_data_empty, key = lambda x:x['prodName'])
    json_data_empty = sorted(list(set_empty))
    OUTPUT_FILE = 'regu_empty.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data_empty, out_file, ensure_ascii=False, indent=4)
        
def is_basic_energy(item):
    name = item['name']
    return '기본' in name and '에너지' in name
def check_basic_energy_regu():
    base_directory = CARDDATA_ROOT
    basic_energy_regu = set()

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        
                        for item in data:
                            if is_basic_energy(item):
                                basic_energy_regu.add(item['regulationMark'])
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    # 각각의 확인할 레규의 카드정보 출력                        
    json_data = sorted(list(basic_energy_regu))
    OUTPUT_FILE = 'ene_regus.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False, indent=4)  

def check_basic_energy_AXY():
    base_directory = CARDDATA_ROOT
    basic_energy_regu = set()

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        
                        for item in data:
                            if is_basic_energy(item):
                                if item['regulationMark'] == 'A' or item['regulationMark'] == 'XY':
                                    basic_energy_regu.add(item['regulationMark'] + " : " + item['prodName'] + " : " + item['cardPageURL'].split('/')[-1])
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    # 각각의 확인할 레규의 카드정보 출력                        
    json_data = sorted(list(basic_energy_regu))
    OUTPUT_FILE = 'ene_regu_A_XY.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False, indent=4)  
        
def check_all_regu():
    base_directory = CARDDATA_ROOT
    all_regus = set()

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        for item in data:
                            all_regus.add(item['regulationMark'])
                            if item['regulationMark'] == '':
                                print(item['name'], file_path )
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
    # 각각의 확인할 레규의 카드정보 출력                        
    print(sorted(list(all_regus)))
        
if __name__ == "__main__":
    #check_regu()
    #check_basic_energy_regu()
    #check_basic_energy_AXY()
    
    check_all_regu()
    