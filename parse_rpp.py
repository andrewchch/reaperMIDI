import os
import argparse

def parse_rpp(file_path):
    media_items = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        if 'SOURCE WAVE' in lines[i]:  # We found a WAVE media item
            i += 1  # Increment to the next line
            if i < len(lines) and 'FILE' in lines[i]:  # Check if FILE is in the next line
                # Extract the file path from the line
                item_path = lines[i].split('"')[1]  # The path is enclosed in double quotes
                if 'reaper media' in item_path.lower():
                    media_items.append(item_path)
        i += 1

    return media_items

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError:
        return "File not found"

def main(target_dir):
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.rpp'):
                rpp_path = os.path.join(root, file)
                media_items = parse_rpp(rpp_path)
                for item in media_items:
                    item_path = os.path.join(root, item) if not os.path.isabs(item) else item
                    size = get_file_size(item_path)
                    print(f'{rpp_path},{item},{size}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process RPP files in target directory.')
    parser.add_argument('dir', type=str, help='Target directory to process')
    args = parser.parse_args()
    main(args.dir)
