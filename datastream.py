import csv
import xlsxwriter
p = 123457
BUCKET_SIZE = 10000
buckets = [0] * BUCKET_SIZE
a = [3, 17, 38, 61, 78]
b = [1561, 277, 394, 13, 246]
totalSum = 0
#calculate the relative error
def calcError(minimum, count):
    return (minimum - count)/ count
#hash function
def hash(x):
    for i in range(5):
        y = x % p 
        hash_val = ((a[i] * y + b[i]) % p) % BUCKET_SIZE
        buckets[hash_val] += 1
#get the minimum value
def getMin(x):
    temp = 0
    tempSet = False
    for i in range(5):
        y = x % p 
        hash_val = ((a[i] * y + b[i]) % p) % BUCKET_SIZE
        if(tempSet == False):
            temp = buckets[hash_val]
            tempSet = True
        else:
            if(temp>buckets[hash_val]):
                temp=buckets[hash_val]
    min = temp
    return min
#read every line of the datastream file
f = open('data_stream.txt')
for line in f.readlines():
    hash(int(line))
f.close()
f = open('counts.txt')
#find total actual sum
for line in f.readlines():
    line = line.split()
    totalSum += int(line[1])
f.close()
f = open('counts.txt')
row_num = 0
first_col = 0
second_col = 1
#write rows and columns to excel
workbook = xlsxwriter.Workbook('graph.xlsx')
worksheet = workbook.add_worksheet()
for line in f.readlines():
    line = line.split()
    value = int(line[0])
    count = int(line[1])
    minimum = getMin(value)
    err = calcError(minimum, count)
    actual_freq = count/totalSum
    worksheet.write(row_num, first_col, err)
    worksheet.write(row_num, second_col, actual_freq)
    row_num += 1
workbook.close()
f.close()