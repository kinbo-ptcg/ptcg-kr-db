# C 상품정보 이어서
#  11. 홈페이지의 상세 제품 페이지 스크래핑
#  이것으로 한국 발매일을 알수 있다!

import os
from bs4 import BeautifulSoup # type: ignore
import requests
import json

#상품 상세정보에서 키워드 지우는데 사용
def remove_first_occurrence(A, B):
    # 문자열 B가 문자열 A에 있는지 확인
    index = A.find(B)
    # 문자열 B가 발견되면 이를 C로 교체
    if index != -1:
        A = A[:index] + A[index + len(B):]
    return A

url_head = "https://pokemoncard.co.kr/card/"
FIRST_PROD_ID = 1
LAST_PROD_ID = 647
prod_data = []

for prod_id in range(FIRST_PROD_ID,LAST_PROD_ID+1):
    url_prod = url_head + str(prod_id)
    res = requests.get(url_prod)
    
    data = {}
    
    data['id'] = prod_id
    
    soup = BeautifulSoup(res.text,'lxml')
    
    #응답 확인
    if not soup.select('h3.medium-title'):
        data['name'] = "Null"
        print(f'id : {prod_id}  name : Null')
        
        prod_data.append(data)
        continue
    
    # 상품명
    prod_name = soup.select('h3.medium-title')[0].text
    data['name'] = prod_name
    
    print(f'id : {prod_id}  name : {prod_name}')
    
    # 제품 URL
    prod_cover_url = soup.find('div', class_='poster_wrap post_shadw').find('img')['src']
    data['cover_url'] = prod_cover_url

    # 상세정보
    prod_detail_obj = soup.select('div.col-md-8.margin-top-30.margin-bottom-30 ul li')
    prod_info = []
    for item in prod_detail_obj:
        text_parts = [str(part) for part in item.stripped_strings]
        text_with_br = '\n'.join(text_parts)
        prod_info.append(text_with_br)

    if len(prod_info) == 0:
        data['type'] = "event"
    elif len(prod_info) == 4:
        keywords = ['발매일','가격','구성물','주의']
        
        for i in range(4):
            prod_info[i] = remove_first_occurrence(prod_info[i],keywords[i])
            prod_info[i] = remove_first_occurrence(prod_info[i],'\n')
        
        data['release-date'] = prod_info[0]
        data['price'] = prod_info[1]
        data['contents'] = prod_info[2]
        data['caution'] = prod_info[3]
    else:
        data['type'] = "unknown"
        data['info'] = prod_info
    
    data['prod_url'] = url_prod
    prod_data.append(data)

# json으로 저장
json_file_name = "product_info_ori.json"
with open(json_file_name, 'w', encoding='utf-8') as f:
    json.dump(prod_data, f, ensure_ascii=False, indent =4)