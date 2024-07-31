import json
import copy
import os

# num_conti : item['number']이 1부터 끝까지 이어져 있는지

CARDDATA_ROOT = '../ptcg_kr_card_data/'

def check_conti(lst):
    if not lst:
        return False, False
    
    min_value = min(lst)
    max_value = max(lst)
    
    # 최소값이 0,1인지 체크
    min_is_one = (min_value in [0,1])

    # 최솟값부터 최댓값까지의 모든 숫자가 리스트에 있는지 확인
    return min_is_one, set(lst) == set(range(min_value, max_value + 1))

def check_prod_conti():
    base_directory = CARDDATA_ROOT

    json_data = []
    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        file_data = []
                        prod_list = []
                        
                        for item in data:
                            prod_name = item['prodName']
                            num = int(item['number'])
                            code = item['prodCode']
                            if prod_name not in prod_list:
                                prod_list.append(prod_name)
                                file_item = {}
                                file_item['prodName'] = prod_name
                                file_item['duplicate'] = []
                                file_item['num_set'] = set([num])
                                file_item['num_list'] = [num]
                                file_item['prodCodes'] = set([code])
                                file_item['file_name'] = file_path.split('/')[-1]
                                file_data.append(file_item)
                            else:
                                for file_item in file_data:
                                    if file_item['prodName'] == prod_name:
                                        if num in file_item['num_set']:
                                            if num == 0 and '기본' in item['name'] and '에너지' in item['name']: 
                                                pass
                                            else:
                                                file_item['duplicate'].append(item['name'])
                                        else:
                                            file_item['num_set'].add(num)
                                            file_item['num_list'].append(num)
                                        file_item['prodCodes'].add(code)
                                            
                        for file_item in file_data:
                            min_is_one, conti = check_conti(file_item['num_list'])
                            file_item['min_is_one'] = min_is_one
                            file_item['conti'] = conti
                            del file_item['num_set']
                            file_item['prodCodes'] = list(file_item['prodCodes'])

                        json_data.extend(file_data)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
                        
    # 어떻게 연속되었는지 파일에 저장
    json_data = sorted(json_data, key = lambda x:x['file_name'])
    OUTPUT_FILE = 'prod_conti.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False, indent=4)
        
    conti_prods = []
    not_conti_prods = []
    for item in json_data:
        item_cp = copy.deepcopy(item)
        item_cp['num_list'].sort()
        if not item['duplicate'] and item['min_is_one'] and item['conti'] and len(item['prodCodes']) == 1:
            item_cp['num_list'] = [min(item_cp['num_list']),max(item_cp['num_list'])]
            del item_cp['duplicate']
            del item_cp['min_is_one']
            del item_cp['conti']
            conti_prods.append(item_cp)
        else:            
            error_m = ''
            if item_cp['duplicate']:
                error_m += 'DUP '
            if not item_cp['min_is_one']:
                error_m += 'MINONE '
            if not item['conti']:
                error_m += 'CONTI '
                blanked_num = sorted(list(set(range(min(item_cp['num_list']), max(item_cp['num_list']) + 1)) - set(item_cp['num_list'])))
                item_cp['blank_num'] = " ".join(map(str, blanked_num))
            if len(item['prodCodes']) != 1:
                error_m += 'CODES '
                
            item_cp['num_list'] = " ".join(map(str, item_cp['num_list']))
            del item_cp['min_is_one']
            del item_cp['conti']
            item_cp['err_m'] = error_m.strip()
            
            not_conti_prods.append(item_cp)
            
    # 어떤게 연속되었는지
    conti_prods = sorted(conti_prods, key = lambda x:x['file_name'])
    OUTPUT_FILE = 'conti_prods.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(conti_prods, out_file, ensure_ascii=False, indent=4)
        
    # 어떤게 문제있는지
    not_conti_prods = sorted(not_conti_prods, key = lambda x:x['file_name'])
    not_conti_prods = sorted(not_conti_prods, key = lambda x:x['err_m'])
    OUTPUT_FILE = 'not_conti_prods.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(not_conti_prods, out_file, ensure_ascii=False, indent=4)
        
# 결과json을 읽고, 문제가 되는 상품명과 문제 없는 상품명 구분해서 출력
# 아마 프로모가 문제인데, 프로모인데도 문제 없는 경우 있다?
def is_promo(item):
    non_promo_keywords = ['BS','ST','GX']
    if any(key in item['file_name'] for key in non_promo_keywords):
        return False
    else:
        return True

def conti_orNot_list():
    CONTI_FILE = 'conti_prods.json'
    NOTCONTI_FILE = 'not_conti_prods.json'
    
    # conti check
    json_data = {}
    json_data['need_check'] = []
    json_data['okay'] = []

    with open(CONTI_FILE, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        for item in data:
            item_info = item['file_name'] + ' : ' + item['prodName']
            if is_promo(item):
                json_data['need_check'].append(item_info)
            else:
                json_data['okay'].append(item_info)
            
    
    OUTPUT_FILE = 'conti_prods_names.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False, indent=4)
    
    # notconti check
    json_data = {}
    json_data['need_check'] = []
    json_data['okay'] = []
    
    with open(NOTCONTI_FILE, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        for item in data:
            item_info = item['file_name'] + ' : ' + item['prodName'] + ' : ' + item['err_m']
            if is_promo(item):
                json_data['okay'].append(item_info)
            else:
                json_data['need_check'].append(item_info)
        
    OUTPUT_FILE = 'not_conti_prods_names.json'
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(json_data, out_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    #check_prod_conti()
    conti_orNot_list()