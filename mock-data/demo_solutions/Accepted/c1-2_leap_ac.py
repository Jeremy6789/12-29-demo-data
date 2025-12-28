import sys
line = sys.stdin.read().strip()
if line:
    y = int(line)
    if (y % 400 == 0) or (y % 4 == 0 and y % 100 != 0):
        print("Leap Year")
    else:
        print("Common Year")