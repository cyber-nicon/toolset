# csv_diff.py
# Author: nicon
# Last updated: 07/18/2026
# this is a tool which takes a diff out of two input files

# to run this code simply give two arguments
# filenames of first and second file 
# please put the bigger file first 

# this is intended to differ between ip adrresses 
# used delimeter ","

import csv
import sys

extended_check = True

first_file=[]
second_file=[]

print(str(sys.argv[1]))
print(str(sys.argv[2]))

filename_1 = str(sys.argv[1])
#with open("ipv4_output_withoutMS.csv", 'r') as file1:
with open(filename_1, 'r') as file1:
    csvreader = csv.reader(file1)
    for row in csvreader:
        first_file = row

filename_2 = str(sys.argv[2])
with open(filename_2, 'r') as file2:
#with open("ipv4_output.csv", 'r') as file2:
    csvreader2 = csv.reader(file2)
    for row in csvreader2:
        second_file = row


len1 = len(first_file)
len2 = len(second_file)
diff = len1 - len2
print("Length 1: " + str(len1))
print("Length 2: " + str(len2))
print("Diff: " + str(diff))

same = []
only_in_one = []
only_in_two = []


if(len1 >= len2):
    for element in first_file:
        found = False
        counter = 0
        #print(element)
        while(not found):
            if(counter < len(second_file)):
                #print(second_file[counter])
                if(element == second_file[counter]):
                    same.append(element)
                    second_file.pop(counter)
                    found = True
                else:
                    counter = counter + 1
            else:
                only_in_one.append(element)
                found = True


if(extended_check):
    print("starting extended check")
    for element in second_file:
        found = False
        counter = 0
        while(not found):
            if(counter < len(second_file)):
                if(element == first_file[counter]):
                    print("something went wrong")
                    exit()
                else:
                    counter = counter + 1
            else:
                only_in_two.append(element)
                found = True
else:
    for element in second_file:
        only_in_two.append(element)


print("################")
print("finished")
print("Length 1: " + str(len1))
print("Length 2: " + str(len2))
print("Diff: " + str(diff))
print("Second file " + str(len(second_file)))
print ("Same: " + str(len(same)))
print ("Only in 1: " + str(len(only_in_one)))
print ("Only in 2: " + str(len(only_in_two)))

storage = input("Do you want me to store the results? (y/n)")
if(storage == "y"):
    with open("same.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(same)
    with open("only_in_1.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(only_in_one)
    with open("only_in_2.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(only_in_two)
    


    
    