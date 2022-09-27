import re

def grep(reg, filename):
#reg = input('Regular expression:')
#filename = input('File:')
    file = open(filename)
    count = 0

    for line in file:
        stuff = re.findall(reg, line)
        if len(stuff) > 0:
            count += 1
   
    print(filename, ' had ', count, ' lines that matched ', reg)
    return count
    
grep('^Author', 'mbox.txt')

def extractor(filename):
    file = open(filename)
    sum_of_revision = 0
    count = 0
    for line in file:
        revision = re.findall('^New .* ([0-9]+)', line)
        if len(revision) > 0:
            sum_of_revision += int(revision[0])
            count += 1
    average = sum_of_revision/count
    print(int(average))
    return average

extractor('mbox.txt')

def summer(filename):
    file = open(filename)
    sum_of_numbers = 0
    count = 0
    for line in file:
        integer = re.findall('[0-9]+', line)
        if len(integer) > 0:
            for number in integer:
                sum_of_numbers += int(number)
                count += 1
    print(int(sum_of_numbers))
    return sum_of_numbers

summer('regex_sum_1362952.txt')