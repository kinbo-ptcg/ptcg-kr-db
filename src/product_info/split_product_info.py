import json

DIR_PROD = './product_info_ori.json'
DIR_CARD = './product_info_cards.json'
DIR_SUPP = './product_info_supp.json'

def filter_non_card():
    with open(DIR_PROD,mode='r',encoding='utf-8') as f:
        data = json.load(f)
            
    card_data = []
    supp_data = []
    
    for item in data:
        if item['type'] != 'supply':
            card_data.append(item)
        else:
            supp_data.append(item)
            
    with open(DIR_CARD, 'w', encoding='utf-8') as json_file:
        json.dump(card_data, json_file, ensure_ascii=False, indent=4)
        
    with open(DIR_SUPP, 'w', encoding='utf-8') as json_file:
        json.dump(supp_data, json_file, ensure_ascii=False, indent=4)
        
def change_prod_name():
    with open(DIR_CARD,mode='r',encoding='utf-8') as f:
        data = json.load(f)
            
    json_data = []
    
    change_list = [
        ["썬&문 확장팩 제6탄「금단의 빛」","썬&문 확장팩 제6탄 「금단의 빛」"],
        ["썬&문 확장팩 제7탄「창공의 카리스마」","썬&문 확장팩 제7탄 「창공의 카리스마」"],
        ["포켓몬 카드 게임 BW 「배틀 체인지덱 비크티니 덱」","BW 「배틀 체인지덱 비크티니 덱」"],
        ["포켓몬 카드 게임 BW 「플라스마단 파워 덱」","BW 「플라스마단 파워 덱」"],
        ["포켓몬 카드 게임 BW 최강 폭류 60장 덱 「거북왕 + 큐레무 EX」","BW 최강 폭류 60장 덱 「거북왕 + 큐레무 EX」"],
        ["포켓몬 카드 게임 BW 확장팩 「EX 배틀 부스트」","BW 확장팩 「EX 배틀 부스트」"],
        ["포켓몬 카드 게임 BW 확장팩 「드래곤 컬렉션」","BW 확장팩 「드래곤 컬렉션」"],
        ["포켓몬 카드 게임 BW 확장팩 「샤이니 컬렉션」","BW 확장팩 「샤이니 컬렉션」"],
        ["포켓몬 카드 게임 BW 확장팩 제2탄 「레드 컬렉션」","BW 확장팩 제2탄 「레드 컬렉션」"],
        ["포켓몬 카드 게임 BW 확장팩 제4탄 「다크러시」","BW 확장팩 제4탄 「다크러시」"],
        ["포켓몬 카드 게임 BW 확장팩 제7탄 「플라스마게일」","BW 확장팩 제7탄 「플라스마게일」"],
        ["포켓몬 카드 게임 BW 확장팩 제9탄 「메갈로캐논」","BW 확장팩 제9탄 「메갈로캐논」"],
        ["포켓몬 카드 게임 썬&문 30장 덱 대전 세트「지우vs로켓단」","썬&문 30장 덱 대전 세트 「지우 VS 로켓단」"],
        ["포켓몬 카드 게임 썬&문 스타터세트 3종", "썬&문 스타터세트"],
        ["확장팩 BASE PACK 20th Anniversary", "XY BREAK 확장팩 BASE PACK 20th Anniversary"],
        ["포켓몬 카드 게임 XY 「퍼스트 세트 - 도치마론의 진화·푸호꼬의 진화·개구마르의 진화」",["XY 퍼스트세트 「개구마르의 진화」","XY 퍼스트세트 「도치마론의 진화」","XY 퍼스트세트 「푸호꼬의 진화」"]],
        ["포켓몬 카드 게임 BW 확장팩 제1탄 「블랙 컬렉션」「화이트 컬렉션」",["BW 확장팩 제1탄 「블랙 컬렉션」","BW 확장팩 제1탄 「화이트 컬렉션」"]],
        ["포켓몬 카드 게임 BW 확장팩 제3탄 「사이코 드라이브」「헤일 블리자드」",["BW 확장팩 제3탄 「사이코 드라이브」","BW 확장팩 제3탄 「헤일 블리자드」"]],
        ["포켓몬 카드 게임 BW 확장팩 제5탄 「드래곤 블라스트」「드래곤 블레이드」",["BW 확장팩 제5탄 「드래곤 블라스트」","BW 확장팩 제5탄 「드래곤 블레이드」"]],
        ["포켓몬 카드 게임 BW 확장팩 제6탄 「프리즈볼트」「콜드플레어」",["BW 확장팩 제6탄 「콜드플레어」","BW 확장팩 제6탄 「프리즈볼트」"]],
        ["포켓몬 카드 게임 BW 확장팩 제8탄 「스파이럴포스」「볼트너클」",["BW 확장팩 제8탄 「볼트너클」","BW 확장팩 제8탄 「스파이럴포스」"]],
        ["포켓몬 카드 게임 BW 「배틀 강화 60장 덱 - 레시라무 EX·제크로무 EX」",["BW 「배틀 강화 60장 덱 - 레시라무 EX」","BW 「배틀 강화 60장 덱 - 제크로무 EX」"]],
        ["포켓몬 카드 게임 BW 「배틀 강화 60장 덱 - 블랙큐레무 EX·화이트큐레무 EX」",["BW 「배틀 강화 60장 덱 - 블랙큐레무 EX」","BW 「배틀 강화 60장 덱 - 화이트큐레무 EX」"]],
        ["포켓몬 카드 게임 BW 「배틀 강화덱 - 비리디온 덱·테라키온 덱·코바르온 덱」",["BW 「배틀 강화덱 - 비리디온 덱」","BW 「배틀 강화덱 - 테라키온 덱」","BW 「배틀 강화덱 - 코바르온 덱」"]],
        ["포켓몬 카드 게임 BW 「볼트로스 덱」「토네로스 덱」",["BW 「볼트로스 덱」","BW 「토네로스 덱」"]],
        ["포켓몬 카드 게임 BW 「삼삼드래 덱」「한카리아스 덱」",["BW 「삼삼드래 덱」","BW 「한카리아스 덱」"]],
        ["포켓몬 카드 게임 BW 「퍼스트 세트 - 풀의 진화·불꽃의 진화·물의 진화」",["BW 「퍼스트 세트 - 물의 진화」","BW 「퍼스트 세트 - 불꽃의 진화」","BW 「퍼스트 세트 - 풀의 진화」"]],
        ["썬&문 확장팩 제1탄 「썬 컬렉션」 「문 컬렉션」",["썬&문 확장팩 제1탄 「문 컬렉션」","썬&문 확장팩 제1탄 「썬 컬렉션」"]],
        ["썬&문 확장팩 제2탄 「알로라의 햇빛」 「알로라의 달빛」",["썬&문 확장팩 제2탄 「알로라의 달빛」","썬&문 확장팩 제2탄 「알로라의 햇빛」"]],
        ["썬&문 확장팩 제3탄 「어둠을 밝힌 무지개」 「빛을 삼킨 어둠」",["썬&문 확장팩 제3탄 「빛을 삼킨 어둠」","썬&문 확장팩 제3탄 「어둠을 밝힌 무지개」"]],
        ["썬&문 확장팩 제4탄 「각성의 용사」 「초차원의 침략자」",["썬&문 확장팩 제4탄 「각성의 용사」","썬&문 확장팩 제4탄 「초차원의 침략자」"]],
        ["썬&문 확장팩 제5탄 「울트라썬」 「울트라문」",["썬&문 확장팩 제5탄 「울트라문」","썬&문 확장팩 제5탄 「울트라썬」"]],
        ["스칼렛&바이올렛 확장팩 「바이올렛 ex」","포켓몬 카드 게임 스칼렛&바이올렛 확장팩 「바이올렛 ex」"],
        ["스칼렛&바이올렛 확장팩 「스칼렛 ex」","포켓몬 카드 게임 스칼렛&바이올렛 확장팩 「스칼렛 ex」"],
        ["썬&문  하이클래스팩「GX 배틀부스트」","썬&문 강화 확장팩 「GX 배틀부스트」"],
        ["썬&문 강화 확장팩 「GX배틀부스트 REMASTER」","썬&문 강화 확장팩 「GX 배틀부스트 REMASTER」"],
        ["썬&문 강화 확장팩「드래곤스톰」","썬&문 강화 확장팩 「드래곤스톰」"],
        ["썬&문 강화 확장팩「울트라포스」","썬&문 강화 확장팩 「울트라포스」"],
        ["썬&문 강화 확장팩「챔피언로드」","썬&문 강화 확장팩 「챔피언로드」"],
        ["썬&문 전격 스타터 세트「라이코 GX」","썬&문 전격 스타터 세트 「라이코 GX」"],
        ["썬&문 전설 스타터 세트 「솔가레오 GX 루나아라 GX」","썬&문 전설 스타터 세트 「솔가레오 GX ･ 루나아라 GX」"],
        ["썬&문 확장팩 「미라클트윈」","썬&문 확장팩 제11탄 「미라클트윈」"],
        ["썬&문 확장팩 「얼터제네시스」","썬&문 확장팩 제12탄 「얼터제네시스」"],
        ["썬&문 스타터 세트 TAG TEAM GX「에브이&테오키스 GX」「블래키&다크라이 GX」",["썬&문 스타터 세트 TAG TEAM GX 「블래키&다크라이 GX」","썬&문 스타터 세트 TAG TEAM GX 「에브이&테오키스 GX」"]],
        ["썬&문 스타터 세트 「불꽃의 부스터 GX」, 「물의 샤미드 GX」, 「번개의 쥬피썬더 GX」",["썬&문 스타터 세트 「물의 샤미드 GX」","썬&문 스타터 세트 「번개의 쥬피썬더 GX」","썬&문 스타터 세트 「불꽃의 부스터 GX」"]],
        ["썬&문 스타터 세트 격투「롱스톤 GX」 물「아쿠스타 GX」",["썬&문 스타터 세트 격투 「롱스톤 GX」","썬&문 스타터 세트 물 「아쿠스타 GX」"]],
        ["XY 30장 덱 대전 세트「염무왕 EX vs 토게키스 EX」","XY 30장 덱 대전 세트 「염무왕 EX vs 토게키스 EX」"],
        ["XY BREAK 콤보 60장 덱 「골덕 BREAK + 펄기아 EX」","XY BREAK 콤보 60장 덱 「골덕 BREAK +펄기아 EX」"],
        ["XY BREAK 확장팩 「환상・전설 드림 컬렉션」","XY BREAK 확장팩 「환상 전설 드림 컬렉션」"],
        ["XY 확장팩「레전드 컬렉션」","XY 확장팩 「레전드 컬렉션」"],
        ["XY 확장팩「마그마단vs아쿠아단 더블크라이시스」","XY 확장팩 「마그마단vs아쿠아단 더블크라이시스」"],
        ["강화 확장팩「썬&문」","썬&문 강화 확장팩 「썬&문」"],
        ["소드&실드 강화 확장팩「VMAX라이징」","소드&실드 강화 확장팩 「VMAX라이징」"],
        ["소드&실드 스타트 덱 100 「피카츄 V & 이브이 V」","소드&실드 「스타트 덱 100 피카츄 V & 이브이 V」"],
        ["소드&실드 스페셜 덱 세트 「자시안 · 자마젠타 VS 무한다이노」","소드&실드 스페셜 덱 세트 「자시안·자마젠타 VS 무한다이노」"],
        ["소드&실드 하이클래스 덱 「인텔리레온 VMAX」","소드&실드 하이클래스 덱 「인텔리레온  VMAX 」"],
        ["소드&실드 하이클래스 덱 「팬텀 VMAX」","소드&실드 하이클래스 덱  「팬텀  VMAX 」"],
        ["소드&실드 하이클래스 덱 더블 BOX 「팬텀 VMAX&인텔리레온 VMAX」","소드&실드 하이클레스 덱 더블 BOX 「팬텀 VMAX&인텔리레온 VMAX」"],
        ["스칼렛&바이올렛 ex 스타트 덱 8종","스칼렛&바이올렛 ex 스타트 덱"],
        ["스칼렛&바이올렛 강화 확장팩 「트리플렛비트」","포켓몬 카드 게임 스칼렛&바이올렛 강화 확장팩 「트리플렛비트」"],
        ["스칼렛&바이올렛 스타터 세트 ex 피카츄 스페셜 세트","포켓몬 카드 게임 스칼렛&바이올렛 스타터 세트 ex 피카츄 스페셜 세트"],
        ["소드&실드 스타터 세트 VMAX 「리자몽」「오롱털」",["소드&실드 스타터 세트 VMAX 리자몽","소드&실드 스타터 세트 VMAX 오롱털"]],
        ["소드&실드 스타터 세트 VMAX 「이상해꽃」「거북왕」",["소드&실드 스타터 세트 VMAX 「거북왕」","소드&실드 스타터 세트 VMAX 「이상해꽃」"]],
        ["소드&실드 확장팩「소드」「실드」",["소드&실드 확장팩 「소드」","소드&실드 확장팩 「실드」"]],
        ["소드&실드 스타터 세트 V 5종",["소드&실드 스타터 세트 V 격투","소드&실드 스타터 세트 V 물","소드&실드 스타터 세트 V 번개","소드&실드 스타터 세트 V 불꽃","소드&실드 스타터 세트 V 풀"]],
        ["XY「제르네아스 덱」「이벨타르 덱」",["XY 「이벨타르 덱」","XY 「제르네아스 덱」"]],
        ["XY 확장팩 제1탄 「X컬렉션」「Y컬렉션」",["XY 확장팩 제1탄 「X컬렉션」","XY 확장팩 제1탄 「Y컬렉션」"]],
        ["XY 확장팩 제5탄 「가이아 볼케이노」「타이달스톰」",["XY 확장팩 제5탄 「가이아 볼케이노」","XY 확장팩 제5탄 「타이달스톰」"]],
        ["XY BREAK 확장팩 제11탄 「타오르는 투사」「냉혹한 반역자」",["XY BREAK 확장팩 제11탄 「냉혹한 반역자」","XY BREAK 확장팩 제11탄 「타오르는 투사」"]],
        ["XY BREAK 확장팩 제8탄 「푸른 충격」「붉은 섬광」",["XY BREAK 확장팩 제8탄 「붉은 섬광」","XY BREAK 확장팩 제8탄 「푸른 충격」"]],
        ["XY BREAK 30장 덱 「라이츄 BREAK」「음번 BREAK」",["XY BREAK 30장 덱 「라이츄 BREAK」","XY BREAK 30장 덱 「음번 BREAK」"]],
        ["썬&문 「패밀리 포켓몬 카드 게임」",["패밀리 포켓몬 카드 게임 「라이츄 GX 덱」","패밀리 포켓몬 카드 게임 「리자몽 GX 덱」","패밀리 포켓몬 카드 게임 「뮤츠 GX 덱」"]]
    ]
    
    for change_item in change_list:
        before = change_item[0]
        after = change_item[1]
        if isinstance(after,list):
            #리스트일때는 분리
            for item in data:
                if item['name'] == before:
                    for after_item in after:
                        item_cp = item.copy()
                        item_cp['name'] = after_item
                        data.append(item_cp)
                    item['delete'] = True
                        
        else:
            for item in data:
                if item['name'] == before:
                    item['name'] = after
    
    for item in data:
        if 'delete' not in item:
            json_data.append(item)
            
    json_data = sorted(json_data, key=lambda x:x['id'])
    json_data = sorted(json_data, key=lambda x:x['type'])

    with open(DIR_CARD, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    filter_non_card()
    change_prod_name()