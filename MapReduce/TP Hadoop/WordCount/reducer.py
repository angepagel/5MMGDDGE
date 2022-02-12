import sys

if __name__ == '__main__':
    mapperOutput = sys.stdin
    word_count = 0

    for line in mapperOutput:
        line = line.strip()
        word, count = line.split('\t', 1)
        try:
            count = int(count)
            word_count += count
        except:
            pass

    print(word_count)
