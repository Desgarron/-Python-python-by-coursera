import sys


digit_string = sys.argv[1]
total = 0
for i in digit_string:
    total += int(i)
print(total)

