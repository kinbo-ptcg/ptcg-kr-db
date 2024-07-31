# 지금 3가지 상품정보 파일이 있다.
# 1. ./every_prodname.json : 카드에 적힌 prodName 기반으로 생성한 상품리스트
# 2. ../../product_list_edit.csv : 카드검색의 텍트스트 기반으로 생성한 상품리스트
# 3. ../../product_info_1_647_edit.json : 상품정보 페이지 기반으로 생성된 상품리스트
# 이들을 병합하고 싶다!!
# 우선, 1,2,3 이 가지는 상품명의 상관관계를 조사하자
import json
import csv

FILE_ONE = '../check_products/every_prodname.csv'
FILE_TWO = '../../raw_datas/product_list_edit.csv'
FILE_THREE = '../../product_info/product_info_cards.json'

def read_one():
    set_rst = set()
    with open(FILE_ONE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # 빈 줄 체크
                set_rst.add(row[0].strip())
    return set_rst

def read_two():
    set_rst = set()
    with open(FILE_TWO, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:  # 빈 줄 체크
                set_rst.add(row[1].strip())
    return set_rst

def read_three():
    set_rst = set()
    with open(FILE_THREE, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    for item in data:
        if 'name' in item:
            if item['type'] == 'special':
                set_rst.add(item['name'].strip())
            else:
                set_rst.add(item['name'].strip())
    return set_rst

if __name__ == "__main__":
    # 세가지 파일의 상품명 정보를 집합으로 반환
    set_one = read_one()
    set_two = read_two()
    set_three = read_three()
    
    # 집합이 3개니까 7개의 영역이 생긴다
    # 1,2,3 : set_i (i=1,2,3) : i 에만 있는거
    # 4,5,6 : set_ij (ij = 12, 13, 23) : ij 에 모두 있고 not ij 에는 없는것.
    # 7 : set_123 : 123에 모두 있는것
    
    set_only_1 = set_one - set_two - set_three
    set_only_2 = set_two - set_one - set_three
    set_only_3 = set_three - set_one - set_two

    set_12 = (set_one & set_two) - set_three
    set_13 = (set_one & set_three) - set_two
    set_23 = (set_two & set_three) - set_one
    
    set_123 = set_one & set_two & set_three


    # 결과를 JSON 형식으로 저장
    result = {
        "set_only_1": sorted(list(set_only_1)),
        "set_only_2": sorted(list(set_only_2)),
        "set_only_3": sorted(list(set_only_3)),
        "set_12": sorted(list(set_12)),
        "set_13": sorted(list(set_13)),
        "set_23": sorted(list(set_23)),
        "set_123": sorted(list(set_123))
    }
    
    for key, ele in enumerate(result):
        print(ele, len(result[ele]))

    with open('prod_set_relationships.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)

    # 같은건데 표현이 다른게 다수 있다
    # 이런걸 찾아서 고쳐주기
    # 결과적으로는 모든 표기를 1. 에 맞추기
    # 경우에따라 2,3에 맞추기
    # 그리고 결과적으로는 최대한 123 을 크게
    
    #FILE_ONE = './every_prodname.csv'
    #FILE_TWO = '../../product_list_edit.csv'
    #FILE_THREE = '../../product_info_1_647_edit.json'
    
    # modify_prodName.py 에서 따로 실행
    
