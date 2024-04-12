import os
import re
from warnings import filterwarnings
from collections import defaultdict

filterwarnings("ignore", category=FutureWarning)

def extract_regex_from_files(folder_path):
    regex_patterns = []
    file_regex_map = defaultdict(list)
    files = os.listdir(folder_path)
    for filename in files:
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            print(f"Reading file: {filename}")
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:
                        regex_patterns.append(line)
                        file_regex_map[line].append(filename)
                        print(f"Added regex pattern: {line}")
    print(f"Added {len(regex_patterns)} regex patterns from {len(files)} files")
    return regex_patterns, file_regex_map

def check_word_against_regex(word, regex_patterns):
    triggered_patterns = []
    for pattern in regex_patterns:
        if re.search(pattern, word):
            triggered_patterns.append(pattern)
    return triggered_patterns


def main():
    print("Enter the folder path containing the .txt files. Type . to check files in current folder")
    folder_path = input("input: ")
    regex_patterns, file_regex_map = extract_regex_from_files(folder_path)

    while True:
        print("Enter a word to check against the regex patterns. Type 'exit' to exit")
        word = input("input: ")
        if word == 'exit':
            break
            
        triggered_patterns = check_word_against_regex(word, regex_patterns)

        if triggered_patterns:
            print(f"The word '{word}' triggers {len(triggered_patterns)} patterns")
            print(f"{'Regex Pattern'.ljust(50)}{'Files Found'.ljust(30)}")
            for pattern in triggered_patterns:
                files_found = ', '.join(file_regex_map[pattern])
                print(f"{pattern.ljust(50)}{files_found.ljust(30)}")
        else:
            print(f"The word '{word}' does not trigger any of the regex patterns.")
        print()

if __name__ == "__main__":
    main()
