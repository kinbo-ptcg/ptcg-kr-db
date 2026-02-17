import sys
import re
import requests
from urllib.parse import urlparse
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup # type: ignore
import json

import pokemon_ptcg_kr
import energy_ptcg_kr
import trainers_ptcg_kr

def to_three_digit(x):
    if x >= 100 :
        return str(x)
    elif x >= 10 :
        return "0" + str(x)
    else :
        return "00" + str(x)

def build_url(head, category, year, ver, num):
    url = head + category
    if year == 0:
        url += '000'
    else:
        url += str(year)
    url += to_three_digit(ver)
    url += to_three_digit(num)

    return url

def check_success(soup):
    # Search <script> tags directly to check for "card data not found" error message
    script_tag = soup.find('script', text=lambda t: t and '없는 카드데이터 입니다.' in t)

    # If the script tag contains the warning message, return False
    if script_tag:
        return False

    # No warning message found, return True
    return True

def log_error_message(where, url):
    print(f'ERROR! {where}')
    print(f'URL : {url}')

    error_csv_dir = './data_cleansing/error/'
    error_csv_path = './data_cleansing/error/error_m.csv'

    # Create directory if it does not exist
    if not os.path.exists(error_csv_dir):
        os.makedirs(error_csv_dir)

    with open(error_csv_path, mode='a', encoding='utf-8') as f:
        f.write(where + ',' + url + '\n')

def scrape_ptcg_kr(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    # Return fail if URL is invalid
    if not check_success(soup):
        return None, "fail"

    # Valid URL: begin scraping
    data = {}
    card_type = soup.find('div', class_ = 'pokemon-info').get_text()

    TRAINERS_KEYWORDS = ['아이템', '포켓몬의 도구', '서포트', '서포터', '스타디움']
    POKEMON_KEYWORDS = ['포켓몬', '복원','V-UNION','레벨업']
    ENERGY_KEYWORDS = ['기본 에너지', '특수 에너지']

    if any(keyword in card_type for keyword in TRAINERS_KEYWORDS):
        data = trainers_ptcg_kr.parse(soup, url)
    elif any(keyword in card_type for keyword in ENERGY_KEYWORDS):
        data = energy_ptcg_kr.parse(soup, url)
    elif any(keyword in card_type for keyword in  POKEMON_KEYWORDS):
        data = pokemon_ptcg_kr.parse(soup, url)
    else:
        log_error_message('invalid card type', url)
        data['supertype'] = card_type
        data['info'] = str(soup.find('div', class_='container', id='heaer_top'))
        data['cardPageURL'] = url

    return data, "success"

if __name__ == "__main__":
    url_head = "https://pokemoncard.co.kr/cards/detail/"
    parsing_start_time = time.time()
    parsed_files = 0
    parsed_cards = 0

    # If num == 1 for a given ver and an error page is returned,
    # check 10 more before terminating
    VER_TERMI_COUNT = 10

    # Full range to scrape
    #category_list = ["BS", "ST", "SVP", "SP", "SMP", "PR"]
    category_list = ["BS", "ST"]  # Promo cards use a different method
    year_list = list(range(2010, datetime.now().year + 1)) + [0000]
    start_ver = 0

    for category in category_list:  # loop category
        for year in year_list:  # loop year
            # The num-th card of the ver-th product in the given year
            ver = start_ver
            num = 1
            ver_flag = True
            ver_error_count = 0

            if category == 'BS' and year < 2019 and year > 2000:
                continue

            while ver_flag:  # loop ver
                ver_start_time = time.time()

                num = 1
                num_flag = True
                parsed_cards_num = 0
                data_json = []

                while num_flag:  # loop num
                    url = build_url(url_head, category, year, ver, num)

                    if num == 1 or num % 5 == 0:
                        print(url)

                    card_data, state = scrape_ptcg_kr(url)

                    if state == "success":
                        data_json.append(card_data)
                        num += 1
                        parsed_cards += 1
                        parsed_cards_num += 1
                        ver_error_count = 0  # Reset error count on success
                    elif state == "fail":
                        num_flag = False


                # If the first card of a ver returns an error, that ver does not exist.
                # If errors continue for 5+ consecutive vers, stop for this year.
                # If a valid ver is found within 2-3 tries, continue.
                if (num_flag == False and num == 1):
                    print(f"invalid ver{ver}")
                    if ver_error_count < VER_TERMI_COUNT:
                        print(f"error count {ver_error_count}, continue searching]")
                        ver_error_count += 1
                        ver += 1
                    else:
                        print(f"error count {ver_error_count}, stop searching")
                        ver_flag = False
                        ver_error_count = 0

                elif data_json == []:
                    # Nothing to save, skip
                    pass

                # Save path: ../ptcg_kr_card_data/{category}/str(year)/
                # File name: {category}_str(year)_str(to_three_digit(ver))_str(to_three_digit(num-1))
                else:  # After checking the card after the last card of each ver, save to file
                    json_path = '../ptcg_kr_card_data/' + category + '/' + str(year) + '/'
                    json_file_name = category + '_' + str(year) + '_' + str(to_three_digit(ver)) + '_' + str(to_three_digit(parsed_cards_num)) + '.json'
                    json_file_path = json_path + json_file_name

                    if not os.path.exists(json_path):
                        os.makedirs(json_path)

                    with open(json_file_path, 'w', encoding='utf-8') as f:
                        json.dump(data_json, f, ensure_ascii=False, indent=4)
                    ver += 1
                    parsed_files += 1

                    ver_end_time = time.time()

                    print(f"Data has been successfully saved to {json_file_path}")
                    print(f"It takes {ver_end_time - ver_start_time} seconds")
                    print(f"{parsed_cards_num} cards saved")

    print("Finish parsing ptcg-kr data")
    print(f"Created files : {parsed_files}")
    print(f"Parsed cards : {parsed_cards}")
    print(f"Total time : {round(time.time() - parsing_start_time, 2)} secs")
