import os
import json

CARDDATA_ROOT = '../ptcg_kr_card_data/'
OUTPUT_FILE = 'all_card_data.json'

def combine_json_files():
    base_directory = CARDDATA_ROOT
    all_data = []

    # Walk all subdirectories and load every JSON file
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

    # Save all combined data to a single JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_file:
        json.dump(all_data, out_file, ensure_ascii=False, indent=4)
    print(f"Total number of Korean PTCG cards released so far: {len(all_data)}")

if __name__ == "__main__":
    combine_json_files()
