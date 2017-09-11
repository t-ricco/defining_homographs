
import random
import sys
import math



# Get number of line in the file.
with open('data/test_data.json') as f:
    number_of_lines = len(f.readlines())

# number of line to get.
NUM_LINES_GET = int(math.floor(0.5*number_of_lines))
print(NUM_LINES_GET)

if NUM_LINES_GET > number_of_lines:
     print("are you crazy !!!!")
     sys.exit(1)

test = open('data/testing_data.json', 'w')
train = open('data/validation_data.json', 'w')

# Choose a random number of a line from the file.
sample =  random.sample(range(1,  number_of_lines+1), NUM_LINES_GET)

f = open('data/test_data.json')

for i in range(1,  number_of_lines+1):
	if i in sample:
		test.write(f.readline())
	else:
		train.write(f.readline())

f.close()
