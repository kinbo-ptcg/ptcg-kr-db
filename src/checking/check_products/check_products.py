# 파싱한 카드 정보를 모두 읽고, 
# 그 안에 들어있는 Proname 을 모두 얻는다.
# 결과적으로 세가지 파일이 나와야한다
# 1. 모든 Prodname의 csv
# 2. (파일명, 그 파일에 포함된 모든 Prodname) 의 csv
# 3. (Prodname, 그 Prodname이 포함된 파일명) 의 csv
# 우선 전체 파일을 훑으면서 
# 0. (파일명, 새로 발견된 Prodname) 을 csv에 저장해간다.
# 이게 끝나면 이걸 1.2.3. 으로 전개하자
# 즉, 이 파일은 
# 0. 을 만드는 함수와
# 1.2.3. 을 만드는 함수를 구현한 것이 된다.
import json
import os
import csv

CARDDATA_ROOT = '../../ptcg_kr_card_data/'

def read_every_card_data():
    csv_data = []

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
                        s = set()
                        for item in data:
                            prodName = item.get('prodName',None)
                            if (prodName not in s) and (prodName is not None):
                                s.add(prodName)
                                csv_data.append([file_path,prodName])
                    except Exception as e:
                        print(f"Error inserting {file_path}: {e}")
    
    csv_data = sorted(csv_data, key = lambda x:x[0])
    # 0. 파일을 csv로 출력
    csv_file_name = 'file_and_prod.csv'
    with open(csv_file_name, mode = 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_data)
        
    return csv_data

# 1. 모든 Prodname의 csv
def gen_every_prodnamd_csv(prod_data):
    prod_all = []
    prod_all_set = set()
    
    for item in prod_data:
        if item[1] not in prod_all_set:
            prod_all_set.add(item[1])
            prod_all.append(item[1])
    
    prod_all = sorted(prod_all)
    
    csv_file_name = 'every_prodname.csv'
    with open(csv_file_name, mode = 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for item in prod_all:
            writer.writerow([item])

# 2. (파일명, 그 파일에 포함된 모든 Prodname) 의 json
def gen_file_prods_json(prod_data):
    file_prods = {}
    for item in prod_data:
        if file_prods.get(item[0],0) == 0:
            file_prods[item[0]] = [] 
            file_prods[item[0]].append(item[1])
        else:
            file_prods[item[0]].append(item[1])
        
    json_file_name = 'file_prods.json'
    with open(json_file_name,mode='w',encoding='utf-8') as f:
        json.dump(file_prods, f, ensure_ascii=False, indent =4)
        
    file_name_dict = {}
    #file_path,prodName
    
    #파일명은 고유한가?
    file_unique = []
    
    for item in prod_data:
        file_name = item[0].split('/')[-1]
        if file_name_dict.get(file_name,-1) == -1:
            file_name_dict[file_name] = 1
        else:
            file_name_dict[file_name] += 1
            
    
    for key in file_name_dict:
        if file_name_dict[key] > 1:
            file_unique.append([key,file_name_dict[key]])
            
    csv_file_name = 'not_unique.csv'
    with open(csv_file_name, mode = 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for item in file_unique:
            writer.writerow([item])
        
# 3. (Prodname, 그 Prodname이 포함된 파일명) 의 json
def gen_prod_files_json(prod_data):
    prod_files = {}
    
    for item in prod_data:
        file_name = item[0].split('/')[-1]
        if prod_files.get(item[1],-1) == -1:
            prod_files[item[1]] = [item[0]]
        else:
            prod_files[item[1]].append(item[0])
            
    json_file_name = 'prod_files.json'
    with open(json_file_name,mode='w',encoding='utf-8') as f:
        json.dump(prod_files, f, ensure_ascii=False, indent =4)
        
    for key in prod_files:
        if len(prod_files[key]) != 1:
            print(key)
                
        
def modify_file_BS2020011122():
    file_name = '../../ptcg_kr_card_data/BS/2020/BS_2020_001_122.json'
    
    with open(file_name, mode='r') as f:
        data = json.load(f)
        
    for item in data:
        if item['prodName'] == "":
            print(item)

def modify_file_BS2020007033():
    file_name = "../../ptcg_kr_card_data/BS/2020/BS_2020_007_033.json"
    
    with open(file_name, mode='r') as f:
        data = json.load(f)  
        
    for item in data:
        if item['prodName'] != "프리미엄 트레이너 박스 「소드&실드」":
            print(item['name'])
            
def modify_file_BS2020012085():
    file_name = "../../ptcg_kr_card_data/BS/2020/BS_2020_012_085.json"
    
    with open(file_name, mode='r') as f:
        data = json.load(f)  
        
    for item in data:
        if item['prodName'] != "소드&실드 강화 확장팩 「전설의 고동」":
            print(item['name'])
            
def modify_file_BS2021018109():
    file_name = "../../ptcg_kr_card_data/BS/2021/BS_2021_018_109.json"
    
    with open(file_name, mode='r') as f:
        data = json.load(f)  
        
    for item in data:
        if item['prodName'] != "소드&실드 확장팩 「퓨전아츠」":
            print(item['name'])
    
if __name__ == "__main__":
    prod_data = read_every_card_data()
    
    # 1. 모든 Prodname의 csv
    gen_every_prodnamd_csv(prod_data)
    # 2. (파일명, 그 파일에 포함된 모든 Prodname) 의 json
    gen_file_prods_json(prod_data)
    # 3. (Prodname, 그 Prodname이 포함된 파일명) 의 json
    gen_prod_files_json(prod_data)
    # 파일 단위 수정
    # 1. ../../ptcg_kr_card_data/BS/2020/BS_2020_001_122.json
    # Prodname = "" 인게 있다
    #modify_file_BS2020011122()
    
    # 2. "../../ptcg_kr_card_data/BS/2020/BS_2020_007_033.json"
    # Prodname 에 필요 없는 띄어쓰기가
    #modify_file_BS2020007033()
    
    # 3. "../../ptcg_kr_card_data/BS/2020/BS_2020_012_085.json"
    # Prodname 에 필요 없는 띄어쓰기가
    #modify_file_BS2020012085()

    # 4. "../../ptcg_kr_card_data/BS/2021/BS_2021_018_109.json"
    # Prodname 에 필요 없는 띄어쓰기가
    #modify_file_BS2021018109()
    
