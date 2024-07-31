import os
import json

#CARDDATA_ROOT = '../ptcg_kr_card_data/'
CARDDATA_ROOT = '../ptcg_kr_card_data/'
OUTPUT_FILE = 'all_card_data.json'

def combine_json_files():
    base_directory = CARDDATA_ROOT
    all_data = []

    # 하위 폴더를 포함하여 모든 JSON 파일에 접근
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                        all_data.extend(data)
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # 통합된 데이터를 하나의 JSON 파일로 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(all_data, out_file, ensure_ascii=False, indent=4)
    print(f"여태까지 발매된 한글판 카드의 총 매수는 {len(all_data)}장 입니다.")

if __name__ == "__main__":
    combine_json_files()
