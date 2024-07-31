import do_scraping as ds
from bs4 import BeautifulSoup
import re
import os
import json
import requests
import pprint

'''
디버그, 테스트를 위한 파일.
각 테스트를 함수로 정의해서 맨 밑에서 하나만 실행
'''

'''
에러 메세지들
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015001001
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015001040
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015001074
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021001011
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021001036
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021001037
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021001074
해결, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021001075
해결불가, 홈페이지 특성마크 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2024001006
해결불가, 홈페이지 특성마크 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2024001007
해결불가, 홈페이지 특성마크 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2024001196
해결불가, 홈페이지 특성마크 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2024001197
해결, 카드번호 없음, card num,https://pokemoncard.co.kr/cards/detail/ST2015001019
'''
def test_1():
    # 덩쿠리 가 덩구리 로 POKEDEX에 있었음
    # test_url = 'https://pokemoncard.co.kr/cards/detail/BS2015001001'
    
    # 원시그란돈 EX 의 '원시' 를 지워야한다
    # test_url = 'https://pokemoncard.co.kr/cards/detail/BS2015001040'
    # test_url = 'https://pokemoncard.co.kr/cards/detail/BS2015001074'
    
    # 차오꿀 이 챠오꿀 로 POKEDEX에 있었음
    # test_url = 'https://pokemoncard.co.kr/cards/detail/BS2021001011'
    
    # 일격, 연격을 이름에서 지워야함
    #test_urls = ['https://pokemoncard.co.kr/cards/detail/BS2021001036',
    #    'https://pokemoncard.co.kr/cards/detail/BS2021001037',
    #    'https://pokemoncard.co.kr/cards/detail/BS2021001074',
    #    'https://pokemoncard.co.kr/cards/detail/BS2021001075']
    #for test_url in test_urls:
    #    data, _ = ds.scrape_ptcg_kr(test_url)
    #
    #    pprint.pprint(data)
    
    # 카드번호 없는카드의 예외처리
    test_url = 'https://pokemoncard.co.kr/cards/detail/ST2015001019'
    data, _ = ds.scrape_ptcg_kr(test_url)
    
    pprint.pprint(data)
    
'''
해결, 도감이름문제, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2012003028
해결, 도감이름문제, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2012003057
해결, 접두사 블랙, check pokemons, https://pokemoncard.co.kr/cards/detail/BS2012008045
해결, 접두사 블랙, check pokemons, https://pokemoncard.co.kr/cards/detail/BS2012008062
해결, 도감이름문제, check pokemons, https://pokemoncard.co.kr/cards/detail/BS2012009022
해결, 접두사 화이트, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2012009041
해결, 접두사 화이트, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2012009062
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002033
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002035
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002037
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002038
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002039
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002041
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002042
해결, 홈페이지 에너지표시 없음, 룰에 넘어가있음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002044
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002045
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002046
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002047
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002048
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002049
해결, 홈페이지 에너지표시 없음, 룰에 넘어가있음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002050
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002051
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002052
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002053
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002054
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002055
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002056
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002057
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002058
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002059
해결, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/BS2015002072
'''
def test_2():
    #test_urls = [
    #        'https://pokemoncard.co.kr/cards/detail/BS2012003028',
    #        'https://pokemoncard.co.kr/cards/detail/BS2012003057',
    #        'https://pokemoncard.co.kr/cards/detail/BS2012008045',
    #        'https://pokemoncard.co.kr/cards/detail/BS2012008062',
    #        'https://pokemoncard.co.kr/cards/detail/BS2012009022',
    #        'https://pokemoncard.co.kr/cards/detail/BS2012009041',
    #        'https://pokemoncard.co.kr/cards/detail/BS2012009062']
    #
    #for test_url in test_urls:
    #    data, _ = ds.scrape_ptcg_kr(test_url)
    #    pprint.pprint(data)
        
    #test_urls = [
    #        'https://pokemoncard.co.kr/cards/detail/BS2015002033',
    #        'https://pokemoncard.co.kr/cards/detail/BS2015002035',
    #        'https://pokemoncard.co.kr/cards/detail/BS2015002037',
    #        'https://pokemoncard.co.kr/cards/detail/BS2015002038']
    #
    #for test_url in test_urls:
    #    data, _ = ds.scrape_ptcg_kr(test_url)
    #    pprint.pprint(data)
    
    test_urls = [
            'https://pokemoncard.co.kr/cards/detail/BS2015002039',
            'https://pokemoncard.co.kr/cards/detail/BS2015002041',
            'https://pokemoncard.co.kr/cards/detail/BS2015002042',
            'https://pokemoncard.co.kr/cards/detail/BS2015002044',
            'https://pokemoncard.co.kr/cards/detail/BS2015002045',
            'https://pokemoncard.co.kr/cards/detail/BS2015002046',
            'https://pokemoncard.co.kr/cards/detail/BS2015002047',
            'https://pokemoncard.co.kr/cards/detail/BS2015002048',
            'https://pokemoncard.co.kr/cards/detail/BS2015002049',
            'https://pokemoncard.co.kr/cards/detail/BS2015002050',
            'https://pokemoncard.co.kr/cards/detail/BS2015002051',
            'https://pokemoncard.co.kr/cards/detail/BS2015002052',
            'https://pokemoncard.co.kr/cards/detail/BS2015002053',
            'https://pokemoncard.co.kr/cards/detail/BS2015002054',
            'https://pokemoncard.co.kr/cards/detail/BS2015002055',
            'https://pokemoncard.co.kr/cards/detail/BS2015002056',
            'https://pokemoncard.co.kr/cards/detail/BS2015002057',
            'https://pokemoncard.co.kr/cards/detail/BS2015002058',
            'https://pokemoncard.co.kr/cards/detail/BS2015002059',
            'https://pokemoncard.co.kr/cards/detail/BS2015002072']
    
    for test_url in test_urls:
        data, _ = ds.scrape_ptcg_kr(test_url)
        pprint.pprint(data)
    
'''
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003001
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003002
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003003
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003004
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003005
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003006
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003007
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003008
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003009
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003010
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003011
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003012
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003013
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003014
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003015
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003016
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003017
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003018
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003019
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003020
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003021
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015003022
해결불가, attack tool,https://pokemoncard.co.kr/cards/detail/BS2015003025
해결불가, attack tool,https://pokemoncard.co.kr/cards/detail/BS2015003026
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015008020
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2015008021
해결, 일러레 정보 없음, artist info,https://pokemoncard.co.kr/cards/detail/BS2018003060

'''
def test_3():
    # test_urls =[
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003001',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003002',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003003',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003004',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003005',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003006',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003007',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003008',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003009',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003010',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003011',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003012',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003013',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003014',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003015',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003016',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003017',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003018',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003019',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003020',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003021',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015003022',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015008020',
    #     'https://pokemoncard.co.kr/cards/detail/BS2015008021'
    # ]
    
    #test_urls = [
    #    'https://pokemoncard.co.kr/cards/detail/BS2015003025',
    #    'https://pokemoncard.co.kr/cards/detail/BS2015003026'
    #]
    
    #for test_url in test_urls:
    #    data, _ = ds.scrape_ptcg_kr(test_url)
    #    pprint.pprint(data)
    
    test_url = 'https://pokemoncard.co.kr/cards/detail/BS2018003066'
    data,_ = ds.scrape_ptcg_kr(test_url)
    
    pprint.pprint(data)

'''
해결,저항 몇인지 없,resi value,https://pokemoncard.co.kr/cards/detail/BS2018004033
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021004027
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021004028
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021004072
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021004073
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021005036
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021005037
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021005075
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021005076
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021006001
해결,접두사 백마흑마,check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021006002
해결,기본에너지 레규,https://pokemoncard.co.kr/cards/detail/BS2021009023
해결불가, 아이템 공격 설명 이상함,https://pokemoncard.co.kr/cards/detail/BS2021011061
해결불가, 아이템 공격 설명 이상함,https://pokemoncard.co.kr/cards/detail/BS2021012061
해결,V-UNION, invalid card type,https://pokemoncard.co.kr/cards/detail/BS2021014001
해결,V-UNION, invalid card type,https://pokemoncard.co.kr/cards/detail/BS2021014002
해결,V-UNION, invalid card type,https://pokemoncard.co.kr/cards/detail/BS2021014003
해결, 피카츄, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021015021
해결, 피카츄, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021015022
해결, 피카츄, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021015023
해결, 피카츄, check pokemons,https://pokemoncard.co.kr/cards/detail/BS2021015024
해결,V-UNION, invalid card type,https://pokemoncard.co.kr/cards/detail/BS2021015025
해결, 봉인석, attack tool,https://pokemoncard.co.kr/cards/detail/BS2024002035
해결불가, 일러레 정보없음, artist info,https://pokemoncard.co.kr/cards/detail/BS2021015025
해결, 기본에너지 상품정보 없음,https://pokemoncard.co.kr/cards/detail/BS2024002054
포켓몬에 아이템룰 텍스트 있음,https://pokemoncard.co.kr/cards/detail/ST2012001001
해결, 슈륙챙이,https://pokemoncard.co.kr/cards/detail/BS2024008024
해결불가, 찬자몽 텍스트에러, https://pokemoncard.co.kr/cards/detail/BS2024009003
해결불가, 찬개닌 텍스트에러, https://pokemoncard.co.kr/cards/detail/BS2024010003
해결, 레규 없는 아이템, https://pokemoncard.co.kr/cards/detail/PR2012001001
해결, 일러레 정보 없음, https://pokemoncard.co.kr/cards/detail/PR2015001038
'''
def test_4():
    # test_urls = [
    #     'https://pokemoncard.co.kr/cards/detail/BS2021014001',
    #     'https://pokemoncard.co.kr/cards/detail/BS2021014002',
    #     'https://pokemoncard.co.kr/cards/detail/BS2021014003'
    # ]
    
    test_urls = [
        'https://pokemoncard.co.kr/cards/detail/BS2021015021',
        'https://pokemoncard.co.kr/cards/detail/BS2021015022',
        'https://pokemoncard.co.kr/cards/detail/BS2021015023',
        'https://pokemoncard.co.kr/cards/detail/BS2021015024',
        'https://pokemoncard.co.kr/cards/detail/BS2021015025'
    ]
    for test_url in test_urls:
        data, _ = ds.scrape_ptcg_kr(test_url)
        pprint.pprint(data)
        
'''
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/ST2010001008
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/ST2010003003
해결불가, 홈페이지 에너지표시 없음, card text,https://pokemoncard.co.kr/cards/detail/ST2010001008
해결불가, 포켓몬인데 아이템 룰 있음, card text,https://pokemoncard.co.kr/cards/detail/ST2011007001
해결불가, 포켓몬인데 아이템 룰 있음, card text,https://pokemoncard.co.kr/cards/detail/ST2013001001
해결,저항 몇인지 없,resi value,https://pokemoncard.co.kr/cards/detail/ST2013005005
해결, 접미사 사이에 띄어쓰기 없음, check pokemons,https://pokemoncard.co.kr/cards/detail/ST2013005006
루챠불,check pokemons,https://pokemoncard.co.kr/cards/detail/ST2016003006
접두사 로켓단의, check pokemons,https://pokemoncard.co.kr/cards/detail/ST2017004010
?? SVP 하나도 발견 안된
?? ver_start = 0 도 의미 없어
!! 프로모는 년도가 아니라 000
?? SMP 하나도 없다
https://pokemoncard.co.kr/cards/detail/SMP000000192
!! SMP 는 번호가 뜨문뜨문
!! SVP, SP 도 혹시 모른다
!! num = 000 ~ 999까지 전부 체크해보기
해결불가, 포켓몬 아이템룰, card text,https://pokemoncard.co.kr/cards/detail/ST2014001001
해결불가, 이름 잘못됨 루챠불, check pokemons,https://pokemoncard.co.kr/cards/detail/ST2016003006
해결, 접두어, check pokemons,https://pokemoncard.co.kr/cards/detail/ST2017004010
해결불가, 기술 에너지 피해 없, card text,https://pokemoncard.co.kr/cards/detail/PR2010001005
해결, 레벨업, invalid card type,https://pokemoncard.co.kr/cards/detail/PR2010001006
해결, 레벨업, invalid card type,https://pokemoncard.co.kr/cards/detail/PR2010001012
해결불가, 기술 에너지 피해 없, card text,https://pokemoncard.co.kr/cards/detail/SVP000000061
해결불가, 체력 없, no hp_num,https://pokemoncard.co.kr/cards/detail/SVP000000081
해결, 접두어, check pokemons,https://pokemoncard.co.kr/cards/detail/SP000000087
해결, 접두어, check pokemons,https://pokemoncard.co.kr/cards/detail/SP000000092
해결, 코코 포켓몬, check pokemons,https://pokemoncard.co.kr/cards/detail/SP000000118
해결불가, 기술 에너지 피해 없, card text,https://pokemoncard.co.kr/cards/detail/SMP000000120
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000130
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000131
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000132
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000133
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000134
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000135
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000136
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000137
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000138
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000139
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000141
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000142
해결, 저항값 없음, resi value,https://pokemoncard.co.kr/cards/detail/SMP000000149
해결, 접두사 울트라, check pokemons,https://pokemoncard.co.kr/cards/detail/SMP000000156
해결불가, 상품정보 없음, prod_name,https://pokemoncard.co.kr/cards/detail/SMP000000157
해결불가, 일러레, artist info,https://pokemoncard.co.kr/cards/detail/SMP000000161
'''
def test_5():
    test_urls = [
        'https://pokemoncard.co.kr/cards/detail/BS2021015021',
        'https://pokemoncard.co.kr/cards/detail/BS2021015022',
        'https://pokemoncard.co.kr/cards/detail/BS2021015023',
        'https://pokemoncard.co.kr/cards/detail/BS2021015024',
        'https://pokemoncard.co.kr/cards/detail/BS2021015025'
    ]
    
    for test_url in test_urls:
        data, _ = ds.scrape_ptcg_kr(test_url)
        pprint.pprint(data)   

'''
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/SMP000000164
해결, 원래 없음, artist info,https://pokemoncard.co.kr/cards/detail/SMP000000194
해결불가, 따로 해야됨, attack tool,https://pokemoncard.co.kr/cards/detail/SMP000000243
해결, 접두사, check pokemons,https://pokemoncard.co.kr/cards/detail/SMP000000269
약점 아이콘만 있음,https://pokemoncard.co.kr/cards/detail/BS2018009017
'''
def test_6():
    test_urls = [
    ]
    for test_url in test_urls:
        data, _ = ds.scrape_ptcg_kr(test_url)
        pprint.pprint(data)   

def test_single():
    test_url = 'https://pokemoncard.co.kr/cards/detail/BS2019017033'
    data, _ = ds.scrape_ptcg_kr(test_url)
    
    pprint.pprint(data)

if __name__ == '__main__':
    #test_1()
    test_single()