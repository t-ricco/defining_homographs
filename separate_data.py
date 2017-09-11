
import random
import sys
import math



# Get number of line in the file.
with open('abstract_scraper/full2.json') as f:
    number_of_lines = len(f.readlines())

# number of line to get.
NUM_LINES_GET = int(math.floor(0.25*number_of_lines))
print NUM_LINES_GET

if NUM_LINES_GET > number_of_lines:
     print "are you crazy !!!!"
     sys.exit(1)

test = open('test_data.json', 'wb')
train = open('train_data.json', 'wb')

# Choose a random number of a line from the file.
sample =  random.sample(range(1,  number_of_lines+1), NUM_LINES_GET)

f = open('abstract_scraper/full2.json')

for i in range(1,  number_of_lines+1):
	if i in sample:
		test.write(f.readline())
	else:
		train.write(f.readline())

f.close()
