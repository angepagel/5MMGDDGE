import sys

if __name__ == '__main__':
    file = sys.stdin
    for line in file:
        for word in line:
            print(f'{word}\t{1}')
