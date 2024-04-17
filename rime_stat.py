import os, sys
import re
from typing import List, Tuple, Dict, Optional

def parse_file(filename: str) -> List[Tuple[str, int]]:
    """Parses the file and extracts words and their counts."""
    entries = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if 'c=' in line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    word = parts[1].strip()
                    count_match = re.search(r'c=(\d+)', parts[2])
                    if count_match:
                        count = int(count_match.group(1))
                        entries.append((word, count))
    return entries

def aggregate_counts(entries: List[Tuple[str, int]]) -> Dict[str, int]:
    """Aggregates counts, accounting for containment of one word in another."""
    word_counts = {}
    for word, count in entries:
        if word not in word_counts:
            word_counts[word] = count
        else:
            word_counts[word] += count

    # Check for containment and update counts
    for base_word, base_count in entries:
        for check_word, check_count in entries:
            if base_word != check_word:
                if base_word in check_word:
                    word_counts[base_word] += check_count

    return word_counts

def rank_words(word_counts: Dict[str, int], min_len: Optional[int], max_len: Optional[int]) -> List[Tuple[str, int]]:
    """Sorts the words by frequency and applies length filtering for the output."""
    filtered_words = [(word, count) for word, count in word_counts.items()
                      if (min_len is None or len(word) >= min_len) and (max_len is None or len(word) <= max_len)]
    return sorted(filtered_words, key=lambda item: item[1], reverse=True)

def rime_stat(filename: str, min_len: Optional[int], max_len: Optional[int]) -> None:
    """Main function to parse the file, aggregate counts, and rank words."""
    entries = parse_file(filename)
    word_counts = aggregate_counts(entries)
    ranked_words = rank_words(word_counts, min_len, max_len)
    for word, count in ranked_words:
        print(f"{word}: {count}")


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('Usage: ' + os.path.basename(sys.executable) + ' ' + os.path.basename(__file__) + ' <filename> [<min_len> <max_len>]')
        sys.exit(1)
    filename = sys.argv[1]
    min_len = int(sys.argv[2]) if len(sys.argv) > 2 else None
    max_len = int(sys.argv[3]) if len(sys.argv) > 3 else None
    rime_stat(filename, min_len, max_len)
