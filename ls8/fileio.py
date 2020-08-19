import sys

if len(sys.argv) != 2:
    print("Usage: fileio.py filename")

try:
    with open("somefile.abc") as f:
        for line in f:
            comment_split = line.split("#")
            n = comment_split[0].strip()

            if n == '':
                continue
            x = int(n, 2)
            print(f"{x:08b}: {x:d}")
except:
    print("Can't find it!")