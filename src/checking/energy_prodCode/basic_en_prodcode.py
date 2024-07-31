import json
import copy
import os

CARDDATA_ROOT = '../../ptcg_kr_card_data/'

def is_promo(data):
    non_promo_keywords = ['BS','ST']
    for item in data:
        if any(key in item['cardPageURL'] for key in non_promo_keywords):
            return False
    else:
        return True
        
def is_basic_energy(item):
    name = item['name']
    regu = item['regulationMark']
    return ('기본' in name) and ('에너지' in name) and (regu == 'BE')

def find_BE(data):
    have_BE = False
    for item in data:
        if is_basic_energy(item):
            have_BE = True
    
    return have_BE

def get_prod_code(data):
    for item in data:
        if is_basic_energy(item):
            pass
        else:
            return item['prodCode']
    
    return 'no prodCode'
            
def  basic_energy_prodcode():
    base_directory = CARDDATA_ROOT

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        json_data = []
                        if find_BE(data) and not is_promo(data):
                            prod_code = get_prod_code(data)
                            for item in data:
                                if is_basic_energy(item):
                                    if item['prodCode'] == "":
                                        item['prodCode'] = prod_code
                                json_data.append(item)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
                if len(json_data) > 0:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        json.dump(json_data, file, ensure_ascii=False, indent=4)
                        
                        
if __name__ == "__main__":
    basic_energy_prodcode()
        