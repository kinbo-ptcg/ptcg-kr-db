import re
from urllib.parse import urlparse
import requests
import os
from bs4 import BeautifulSoup # type: ignore

# url : 카드페이지 url
# 이미지 url이 아니다!!
def get_card_img(url):
    # url 에서 파일 경로 생성
    pattern = r'/(\w+)(\d{4})(\d{3})(\d{3})'
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
        
    match = re.search(pattern, url)
    category = match.group(1)
    year = match.group(2)
    ver = match.group(3)
        
    card_img_path = './img/' + category + '/' + str(year) + '/' + str(ver) + '/'
        
    # 카드이미지 url 찾고, 파일명 정하기
    card_img_url = soup.find('img', class_ = 'feature_image').get('src')
    card_img_file_name = urlparse(card_img_url).path.split('/')[-1]
        
    # 이미지 저장
    img_res = requests.get(card_img_url)
    img_res.raise_for_status()  # 요청이 성공했는지 확인
        
    card_img_file_path = card_img_path + card_img_file_name
                
    if not os.path.exists(card_img_path):
        os.makedirs(card_img_path)

    with open(card_img_file_path, 'wb') as f:
        f.write(img_res.content)
        
    print("Image downloaded and saved successfully.")
    
# 변환의 가면의 4가지 RR 오거폰 ex의 이미지를 다운로드하는 예
if __name__ == "__main__":
    urls = ["https://pokemoncard.co.kr/cards/detail/BS2024008016",
            "https://pokemoncard.co.kr/cards/detail/BS2024008022",
            "https://pokemoncard.co.kr/cards/detail/BS2024008038",
            "https://pokemoncard.co.kr/cards/detail/BS2024008065"]
    
    for url in urls:
        get_card_img(url)
        
        