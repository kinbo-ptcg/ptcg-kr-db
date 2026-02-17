import json
import time
import os
from datetime import datetime

import do_scraping

# 몇몇 하이클래스팩은 URL구조가 예외적이라 따로 접근한다
# THE BEST OF XY
# https://pokemoncard.co.kr/cards/detail/BS201707001
# https://pokemoncard.co.kr/cards/detail/BS201707186
# 울트라샤이니의 프로모카드 5장
# https://pokemoncard.co.kr/cards/detail/BS2019014244
# https://pokemoncard.co.kr/cards/detail/BS2019014245
# https://pokemoncard.co.kr/cards/detail/BS2019014246
# https://pokemoncard.co.kr/cards/detail/BS2019014247
# https://pokemoncard.co.kr/cards/detail/BS2019014248

def parse_bestxy():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS201707'
    num_list = list(range(1,187))
    GET_IMG = False
    
    data_json = []
    
    for num in num_list:
        url = url_head + do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
            
        card_data, state = do_scraping.scrape_ptcg_kr(url, get_img=GET_IMG)
        
        if state == "success":
            data_json.append(card_data)
        elif state == "fail":
            pass
    
    json_file_path = '../ptcg_kr_card_data/BS/2017/BS_2017_07_186.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
            
def parse_GX_ulti():
    url_list = [
        'https://pokemoncard.co.kr/cards/detail/BS2019014244',
        'https://pokemoncard.co.kr/cards/detail/BS2019014245',
        'https://pokemoncard.co.kr/cards/detail/BS2019014246',
        'https://pokemoncard.co.kr/cards/detail/BS2019014247',
        'https://pokemoncard.co.kr/cards/detail/BS2019014248'
    ]
    data_json = []
    
    for url in url_list:
        card_data, state = do_scraping.scrape_ptcg_kr(url)
        
        if state == "success":
            data_json.append(card_data)
        elif state == "fail":
            pass
    
    json_file_path = '../ptcg_kr_card_data/BS/2019/GX_ulti.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
        
'''
https://pokemoncard.co.kr/cards/detail/SVP002023003        "2023 코리안리그 시즌2 4강 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023001        "2023 코리안리그 시즌2 우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023002        "2023 코리안리그 시즌2 준우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023006        "2023 코리안리그 시즌3 4강 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023004        "2023 코리안리그 시즌3 우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023005        "2023 코리안리그 시즌3 준우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023009        "2023 코리안리그 시즌4 4강 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023007        "2023 코리안리그 시즌4 우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023008        "2023 코리안리그 시즌4 준우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023012        "2023 코리안리그 파이널 시즌 4강 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023010        "2023 코리안리그 파이널 시즌 우승 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023013        "2023 코리안리그 파이널 시즌 입상 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023014         "2023 코리안리그 파이널 시즌 입상 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002023011        "2023 코리안리그 파이널 시즌 준우승 프로모",
        "2024 코리안리그 시즌1 4강 프로모",
https://pokemoncard.co.kr/cards/detail/SVP002024001        "2024 코리안리그 시즌1 우승 프로모",
        "2024 코리안리그 시즌1 준우승 프로모",
        "2024 코리안리그 시즌2 4강 프로모",
        "2024 코리안리그 시즌2 우승 프로모",
        "2024 코리안리그 시즌2 준우승 프로모",
        "2024 코리안리그 시즌3 4강 프로모",
        "2024 코리안리그 시즌3 우승 프로모",
        "2024 코리안리그 시즌3 준우승 프로모",
        "2024 코리안리그 파이널 4강 프로모",
        "2024 코리안리그 파이널 우승 프로모",
        "2024 코리안리그 파이널 준우승 프로모",
'''
def parse_win_medal():
    data_json = []
    
    url_head = 'https://pokemoncard.co.kr/cards/detail/SVP00'
    years = [2023,2024]
    
    for year in years:
        num = 1
        num_flag = True
        while num_flag:
            url = url_head+str(year)+do_scraping.to_three_digit(num)
            
            card_data, state = do_scraping.scrape_ptcg_kr(url)
        
            if state == "success":
                data_json.append(card_data)
            elif state == "fail":
                pass
                        
            num += 1
            if year == 2023 and num > 20:
                num_flag = False
            elif year == 2024 and num > 12:
                num_flag = False
    
    json_file_path = '../ptcg_kr_card_data/SVP/0/win_medals.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
# 포켓몬 카드 게임 BW 「퍼스트 세트 - 풀의 진화·불꽃의 진화·물의 진화
# 풀 : https://pokemoncard.co.kr/cards/detail/ST2011001001 ~ https://pokemoncard.co.kr/cards/detail/ST2011001034
# 불꽃 : https://pokemoncard.co.kr/cards/detail/ST2011002004 ~ https://pokemoncard.co.kr/cards/detail/ST2011002034
# 물 : https://pokemoncard.co.kr/cards/detail/ST2011003009 ~ https://pokemoncard.co.kr/cards/detail/ST2011003034

def parse_bw_first():    
    url_head = 'https://pokemoncard.co.kr/cards/detail/ST2011'
    vers = [1,2,3]
    nums = list(range(35))
    
    for ver in vers:
        parsed_card_num = 0
        data_json = []
        for num in nums:
            url = url_head+do_scraping.to_three_digit(ver)+do_scraping.to_three_digit(num)
            if num == 1 or num % 5 == 0:
                print(url)
            
            card_data, state = do_scraping.scrape_ptcg_kr(url)
        
            if state == "success":
                data_json.append(card_data)
                parsed_card_num += 1
            elif state == "fail":
                pass
             
        json_file_path = '../ptcg_kr_card_data/ST/2011/ST_2011_'+do_scraping.to_three_digit(ver)+'_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
        with open(json_file_path,mode='w',encoding='utf-8') as file:
            json.dump(data_json,file,ensure_ascii=False, indent=4)
            
# "XY 확장팩 제1탄 「Y컬렉션」"
# https://pokemoncard.co.kr/cards/detail/BS2014501001 ~ https://pokemoncard.co.kr/cards/detail/BS2014501063

def parse_ycollection():    
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2014501'
    vers = [0]
    nums = list(range(64))
    
    for ver in vers:
        parsed_card_num = 0
        data_json = []
        for num in nums:
            url = url_head+do_scraping.to_three_digit(num)
            if num == 1 or num % 5 == 0:
                print(url)
            
            card_data, state = do_scraping.scrape_ptcg_kr(url)
        
            if state == "success":
                data_json.append(card_data)
                parsed_card_num += 1
            elif state == "fail":
                pass
             
        json_file_path = '../ptcg_kr_card_data/BS/2014/BS_2014_501_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
        with open(json_file_path,mode='w',encoding='utf-8') as file:
            json.dump(data_json,file,ensure_ascii=False, indent=4)

'''
https://pokemoncard.co.kr/cards/detail/SP000000000202208        "포켓몬 월드챔피언십2022 개최 기념 참가 프로모 카드",
https://pokemoncard.co.kr/cards/detail/SVP002023000        "포켓몬 월드챔피언십2023 개최 기념 참가 프로모 카드"
https://pokemoncard.co.kr/cards/detail/SMP0000000022
https://pokemoncard.co.kr/cards/detail/SMP0000000023
https://pokemoncard.co.kr/cards/detail/SMP0000000021
https://pokemoncard.co.kr/cards/detail/SMP0000000020
https://pokemoncard.co.kr/cards/detail/SMP0000000019     "썬&문 프로모 카드 포켓몬 월드챔피언십2017 대한민국 대표 선발전 개최 기념 프로모 팩",
https://pokemoncard.co.kr/cards/detail/SMP0000000027        "썬&문 프로모 카드 포켓몬 월드챔피언십2017 개최 기념 참가 프로모 카드",
https://pokemoncard.co.kr/cards/detail/SMP0000000026     "썬&문 프로모 카드 포켓몬 월드챔피언십2017 대한민국 대표 선발전 카드 게임 부문 4강 진출자 선물",
https://pokemoncard.co.kr/cards/detail/SMP0000000024        "썬&문 프로모 카드 포켓몬 월드챔피언십2017 대한민국 대표 선발전 카드 게임 부문 우승자 선물",
https://pokemoncard.co.kr/cards/detail/SMP0000000025        "썬&문 프로모 카드 포켓몬 월드챔피언십2017 대한민국 대표 선발전 카드 게임 부문 준우승자 선물",
'''
def parse_worlds():
    url_list = [
        'https://pokemoncard.co.kr/cards/detail/SP000000000202208',
        'https://pokemoncard.co.kr/cards/detail/SVP002023000',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000022',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000023',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000021',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000020',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000019',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000027',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000026',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000024',
        'https://pokemoncard.co.kr/cards/detail/SMP0000000025'
    ]
    data_json = []
    
    for url in url_list:
        card_data, state = do_scraping.scrape_ptcg_kr(url)
        
        if state == "success":
            data_json.append(card_data)
        elif state == "fail":
            pass
             
    json_file_path = '../ptcg_kr_card_data/SVP/0/win_medals2.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
              
# 썬문 프로모에는 
# https://pokemoncard.co.kr/cards/detail/SMP0000000001 같이
# SMP 0000 000 001 ~ nnn 의 형식도 존재한다
# 일단 nnn = 100 까지 해보자
def parse_SM_promos():
    url_head = 'https://pokemoncard.co.kr/cards/detail/SMP0000000'
    vers = [0]
    nums = list(range(105))
    
    for ver in vers:
        parsed_card_num = 0
        data_json = []
        for num in nums:
            url = url_head+do_scraping.to_three_digit(num)
            if num == 1 or num % 5 == 0:
                print(url)
            
            card_data, state = do_scraping.scrape_ptcg_kr(url)
        
            if state == "success":
                data_json.append(card_data)
                parsed_card_num += 1
            elif state == "fail":
                print(f"FAIL : {url}")
                pass
             
        json_file_path = '../ptcg_kr_card_data/SMP/0/SMP_0_0000_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
        with open(json_file_path,mode='w',encoding='utf-8') as file:
            json.dump(data_json,file,ensure_ascii=False, indent=4)
            
# 프로모 한장
# https://pokemoncard.co.kr/cards/detail/SMP0000000957
def parse_a_medal():
    url = 'https://pokemoncard.co.kr/cards/detail/SMP0000000957'
    data_json = []
    card_data, _ = do_scraping.scrape_ptcg_kr(url)
    data_json.append(card_data)
    
    json_file_path = './last_medal.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
    
# 중간에 url하나가 건너뛰어져있음
# 109번까지 봐야한다

def parse_ultra_force():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2018003'
    nums = list(range(110))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2018/BS_2018_003_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
# 알로라의 햇빛 확팩 중간에 url끊겨있음
def parse_alola():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2017004'
    nums = list(range(56))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2017/BS_2017_004_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
#소드&실드 하이클래스팩 「VMAX 클라이맥스」277에 에너지8종까지. 56-59를 모르페코vunion이 차지해서 60번 보질 못함. 285까지 볼것
# https://pokemoncard.co.kr/cards/detail/BS2022001257
# 226 ~ 229 행방불명 -> 모르페코 Vunion
def parse_VMAXCLIMAX():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2022001'
    nums = list(range(286))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2022/BS_2022_001_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)

#소드&실드 확장팩 「창공스트림」 67까지는 BS2021012xxx를 따르다가 68~79에서 BS2021009xxx를 따름. 이건 인텔vmax덱인데 다행히 충돌은 없음
# https://pokemoncard.co.kr/cards/detail/BS2021012050
def parse_ChangGong():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2021012'
    nums = list(range(68))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
        
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2021009'
    nums = list(range(68,80))
    
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2021/BS_2021_012_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
#소드&실드 확장팩 「마천퍼펙트」창공스트림과 동일. 67까지는 BS2021011xxx를 따르다가 68~79에서 BS2021008xxx를 따름. 이건 팬텀vmax덱인데 다행히 충돌은 없음
#https://pokemoncard.co.kr/cards/detail/BS2021011050
def parse_MaCheon():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2021011'
    nums = list(range(68))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
        
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2021008'
    nums = list(range(68,80))
    
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2021/BS_2021_011_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)

#소드&실드 하이클래스팩 「VSTAR 유니버스」173에서 링크가 끊김. 250까지 있고, 에너지 8종도 있음. 258까지 볼것
#https://pokemoncard.co.kr/cards/detail/BS2023001245
def parse_VSTARUni():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2023001'
    nums = list(range(260))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2023/BS_2023_001_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
# 끝에있는 UR들
def parse_VSTARUni2():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2023001'
    nums = list(range(255,270))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = './'+'uni.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)

#소드&실드 확장팩 「25th ANNIVERSARY COLLECTION」25가 피카츄vunion.  38까지 있음
#https://pokemoncard.co.kr/cards/detail/BS2021015020
def parse_25th():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2021015'
    nums = list(range(40))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2021/BS_2021_015_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)

#스칼렛&바이올렛 확장팩 「변환의 가면」	133까지 다시보기
#https://pokemoncard.co.kr/cards/detail/BS2024008025
def parse_Mask():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2024008'
    nums = list(range(134))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2024/BS_2024_008_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)

#스칼렛&바이올렛 확장팩 「나이트 원더러」	64까지 BS2024011064
def parse_Night():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2024011'
    nums = list(range(65))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2024/BS_2024_011_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
# SV 확팩들이 묘하게 UR만! 없다
# 뒤에 번호들 파싱해야함.
# prodNum이 50넘는걸 팩이라 간주하고 이것들의 끝번호부터 시작해서 파싱
def parse_SV_Rares():
    url_head_ori = 'https://pokemoncard.co.kr/cards/detail/BS'
    years = [str(y) for y in range(2023, datetime.now().year + 1)]
    vers = list(range(1,24))
    
    for year in years:
        for ver in vers:
            url_head = url_head_ori + year + do_scraping.to_three_digit(ver)
            
            # 일단 하나 봐서 전체 몇개인지 체크
            url_test = url_head + '010'
            card_data, state = do_scraping.scrape_ptcg_kr(url_test)
            test_rst = True
    
            if state == "success":
                if int(card_data['prodNumber']) < 56:
                    test_rst = False
            elif state == "fail":
                test_rst = False
                
            if not test_rst:
                continue
            
            # 끝번호부터 40개 파싱
            lastNum = int(card_data['prodNumber'])
            parsed_card_num = 0
            data_json = []
            for num in range(1,41):
                url = url_head+do_scraping.to_three_digit(lastNum + num)
                if num == 1 or num % 5 == 0:
                    print(url)
        
                card_data, state = do_scraping.scrape_ptcg_kr(url)
    
                if state == "success":
                    data_json.append(card_data)
                    parsed_card_num += 1
                elif state == "fail":
                    pass
            
            if parsed_card_num > 1:
                json_file_path = '../ptcg_kr_card_data/BS/'+year+'/BS_'+year +'_'+do_scraping.to_three_digit(ver)+'_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
                with open(json_file_path,mode='w',encoding='utf-8') as file:
                    json.dump(data_json,file,ensure_ascii=False, indent=4)
                    
#스칼렛&바이올렛 확장팩 「포켓몬 카드 151」	240까지 BS2023014240
def parse_151():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2023014'
    nums = list(range(241))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2023/BBS_2024_014_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
#스칼렛&바이올렛 확장팩 「샤트」	400 까지 BS2024001400
def parse_ShinyTrea():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2024001'
    nums = list(range(401))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2024/BBS_2024_001_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
def parse_banditUR():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2015005'
    nums = list(range(90,100))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = './'+'uni.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
def parse_stella():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2024012'
    nums = list(range(110))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2024/BS_2024_012_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
def parse_Night2():
    url_head = 'https://pokemoncard.co.kr/cards/detail/BS2024011'
    nums = list(range(100))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/BS/2024/BS_2024_011_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)
        
def parse_Parukia():
    url_head = 'https://pokemoncard.co.kr/cards/detail/ST2015006'
    nums = list(range(80))
    
    parsed_card_num = 0
    data_json = []
    for num in nums:
        url = url_head+do_scraping.to_three_digit(num)
        if num == 1 or num % 5 == 0:
            print(url)
        
        card_data, state = do_scraping.scrape_ptcg_kr(url)
    
        if state == "success":
            data_json.append(card_data)
            parsed_card_num += 1
        elif state == "fail":
            pass
         
    json_file_path = '../ptcg_kr_card_data/ST/2015/ST_2015_006_'+do_scraping.to_three_digit(parsed_card_num)+'.json'
    with open(json_file_path,mode='w',encoding='utf-8') as file:
        json.dump(data_json,file,ensure_ascii=False, indent=4)

if __name__ == "__main__":
    #parse_bestxy()
    #parse_GX_ulti()
    #parse_win_medal()
    #parse_bw_first()
    #parse_ycollection()
    #parse_worlds()
    #parse_SM_promos()
    #parse_a_medal()
    #parse_ultra_force()
    #parse_alola()
    
    # ver 1.1을 위해
    #parse_VMAXCLIMAX()
    #parse_ChangGong()
    #parse_MaCheon()
    #parse_25th()
    #parse_Mask()
    #parse_Night()
    #parse_VSTARUni()
    
    # ver 1.2 위해
    #parse_SV_Rares()
    #parse_151()
    #parse_ShinyTrea()
    #parse_VSTARUni2()
    #parse_banditUR()
    
    # ver 2.0 위해
    #스텔라미라클 카드정보 추가
    parse_stella()
    #나이트 원더러 고레어 카드 추가
    parse_Night2()
    #누락 데이터 추가
    parse_Parukia()
    