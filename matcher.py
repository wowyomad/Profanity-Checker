import os
import re
import argparse
from warnings import filterwarnings
from collections import defaultdict
from sys import argv, exit

filterwarnings("ignore", category=FutureWarning)


def process_files(folder_path, pattern_set, pattern_type, file_regex_map):
    files = os.listdir(folder_path)
    for filename in files:
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"Reading file: {filename}")
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        pattern = re.compile(r'\b' + line + r'\b')
                        pattern_set.add(pattern)
                        file_regex_map[pattern.pattern][pattern_type] = filename
def extract_regex_from_files(dirty_folder_path, clean_folder_path, no_clean):
    dirty_regex_patterns = set()
    clean_regex_patterns = set()
    file_regex_map = defaultdict(dict)

    process_files(dirty_folder_path, dirty_regex_patterns, 'dirty', file_regex_map)

    if not no_clean and clean_folder_path:
        process_files(clean_folder_path, clean_regex_patterns, 'clean', file_regex_map)

    print(f"Added {len(clean_regex_patterns)} clean and {len(dirty_regex_patterns)} dirty regex patterns.")
    return dirty_regex_patterns, clean_regex_patterns, file_regex_map

def check_word_against_regex(word, regex_patterns):
    triggered_patterns = {'dirty': [], 'clean': []}
    for pattern in regex_patterns['dirty']:
        if pattern.search(word):
            triggered_patterns['dirty'].append(pattern)

    if triggered_patterns['dirty']:
        for pattern in regex_patterns['clean']:
            if pattern.search(word):
                triggered_patterns['clean'].append(pattern)

    return triggered_patterns


def get_folder_path():
    folder_path = None

    if len(argv) < 2:
        dirty_folder = "./dirty"
        clean_folder = "./clean"
        if not os.path.exists(clean_folder):
            os.makedirs(clean_folder)
        if not os.path.exists(dirty_folder):
            os.makedirs(dirty_folder)
    else:
        dirty_folder = argv[1]
        clean_folder = argv[2]

    if not os.path.isdir(clean_folder) or not os.path.isdir(dirty_folder):
        print("Invalid folder path.")
        print("Please provide a valid folder path containing the .txt files.")
        return None

    return dirty_folder, clean_folder


def main():
    parser = argparse.ArgumentParser(description='Process some paths.')
    parser.add_argument('-d', '--dirty', default='./dirty', help='Path to dirty folder')
    parser.add_argument('-c', '--clean', default='./clean', help='Path to clean folder')
    parser.add_argument('-no-clean', action='store_true', default=False, help='Do not check clean files')
    args = parser.parse_args()

    dirty_folder, clean_folder = args.dirty, args.clean
    no_clean = args.no_clean

    regex_patterns = {"dirty": set(), "clean": set()}
    regex_patterns['dirty'], regex_patterns['clean'], file_regex_map = extract_regex_from_files(dirty_folder, clean_folder, no_clean)

    while True:
        print("Enter a word to check against the regex patterns. Type 'exit' to exit.")
        word = input("Input: ")

        if word == 'exit':
            break

        triggered_patterns = check_word_against_regex(word, regex_patterns)

        if triggered_patterns['dirty']:
            print(f"The word '{word}' triggers {len(triggered_patterns['dirty'])} dirty pattern(s)")
            print(f"{'Dirty Pattern'.ljust(50)}{'Files Found'.ljust(30)}")
            for pattern in triggered_patterns['dirty']:
                files_found = (file_regex_map[pattern.pattern]['dirty'])
                print(f"{pattern.pattern.ljust(50)}{files_found.ljust(30)}")

        if triggered_patterns['clean']:
            print(f"The word '{word}' triggers {len(triggered_patterns['clean'])} clean pattern(s)")
            print(f"{'Clean Pattern'.ljust(50)}{'Files Found'.ljust(30)}")
            for pattern in triggered_patterns['clean']:
                files_found = (file_regex_map[pattern.pattern]['clean'])
                print(f"{pattern.pattern.ljust(50)}{files_found.ljust(30)}")

        if not triggered_patterns['dirty'] and not triggered_patterns['clean']:
            print(f"The word '{word}' does not trigger any of the dirty patterns.")
        print()


if __name__ == "__main__":
    main()
